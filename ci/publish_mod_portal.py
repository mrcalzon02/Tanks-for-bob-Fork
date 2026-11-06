#!/usr/bin/env python3
"""Idempotently upload an existing Factorio mod release via the official Mod Portal API.

Needs only the ModPortal: Upload Mods scope. Reads its API key from the GitHub
Actions secret FACTORIO_MOD_UPLOAD_KEY, not source or command line arguments.
"""
import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
import zipfile
from pathlib import Path

BASE = "https://mods.factorio.com"
MOD = "tanks_for_bob_fork"


def request(url, data=None, headers=None, attempts=3):
    headers = {"User-Agent": "Tanks-for-Bob-Fork-Release-CI/1.0", **(headers or {})}
    last = None
    for n in range(attempts):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=75) as resp:
                payload = resp.read()
            if not payload:
                raise RuntimeError("API returned empty response")
            return json.loads(payload)
        except urllib.error.HTTPError as err:
            body = err.read(1000).decode("utf-8", "replace")
            # Do not print request headers or the upload URL containing a token.
            last = RuntimeError(f"Mod Portal HTTP {err.code}: {body}")
            if err.code not in (429, 500, 502, 503, 504):
                raise last from None
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as err:
            last = RuntimeError(f"Mod Portal request failed: {type(err).__name__}")
        if n < attempts - 1:
            time.sleep(2 ** n)
    raise last


def portal_versions():
    result = request(BASE + "/api/mods/" + MOD + "/full")
    return {v["version"] for v in result.get("releases", [])}


def upload(archive, version, key):
    if version in portal_versions():
        print(f"[TANKS-PUBLISH] ALREADY_PUBLISHED {MOD} {version}", flush=True)
        return
    form = urllib.parse.urlencode({"mod": MOD}).encode("utf-8")
    response = request(
        BASE + "/api/v2/mods/releases/init_upload",
        data=form,
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/x-www-form-urlencoded"},
    )
    upload_url = response.get("upload_url")
    if not isinstance(upload_url, str) or not upload_url.startswith("https://"):
        raise RuntimeError("Mod Portal did not return a secure upload URL")
    boundary = "tanks-ci-" + uuid.uuid4().hex
    start = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{archive.name}"\r\n'
        "Content-Type: application/zip\r\n\r\n"
    ).encode()
    end = f"\r\n--{boundary}--\r\n".encode()
    body = start + archive.read_bytes() + end
    result = request(upload_url, data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }, attempts=2)
    if result.get("success") is not True:
        # Do not print arbitrary API payloads that may include temporary URLs.
        raise RuntimeError(f"Mod Portal upload did not confirm success: {result.get('error', 'unknown')}")
    print(f"[TANKS-PUBLISH] UPLOAD_ACCEPTED {MOD} {version}", flush=True)
    for n in range(12):
        try:
            if version in portal_versions():
                print(f"[TANKS-PUBLISH] PORTAL_RELEASE_VERIFIED {MOD} {version}", flush=True)
                return
        except RuntimeError:
            pass
        time.sleep(3)
    raise RuntimeError("Upload accepted but release version not yet verified in Mod Portal")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archive", type=Path)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    key = os.environ.get("FACTORIO_MOD_UPLOAD_KEY", "").strip()
    if not key:
        raise SystemExit(
            "Missing GitHub Actions secret FACTORIO_MOD_UPLOAD_KEY: "
            "add the Factorio ModPortal Upload Mods API key in repository Actions secrets."
        )
    expected = f"{MOD}_{args.version}.zip"
    if args.archive.name != expected:
        raise SystemExit(f"Wrong archive name: expected {expected}")
    with zipfile.ZipFile(args.archive) as z:
        assert z.testzip() is None, "Corrupt mod archive"
        root = f"{MOD}_{args.version}/"
        meta = json.loads(z.read(root + "info.json"))
        assert meta["name"] == MOD and meta["version"] == args.version, "Mod identity/version mismatch"
        assert meta["factorio_version"] == "2.0", "Only the verified Factorio 2.0 package is authorized"
    upload(args.archive, args.version, key)


if __name__ == "__main__":
    main()
