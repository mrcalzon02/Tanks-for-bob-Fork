#!/usr/bin/env python3
"""Verify real private Factorio dedicated-server startup without joining it."""
import argparse
import re
import subprocess
import sys
import time
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    for field in ("binary", "mods", "save", "settings"):
        p.add_argument("--" + field, required=True)
    p.add_argument("--log", type=Path, required=True)
    p.add_argument("--timeout", type=int, default=90)
    a = p.parse_args()
    a.log.parent.mkdir(parents=True, exist_ok=True)
    command = [a.binary, "--mod-directory", a.mods, "--start-server", a.save,
               "--server-settings", a.settings, "--port", "34197"]
    ready, problem = False, None
    with a.log.open("w", encoding="utf-8") as log:
        proc = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT)
        try:
            deadline = time.monotonic() + a.timeout
            while time.monotonic() < deadline:
                if proc.poll() is not None:
                    problem = f"Server stopped with exit code {proc.returncode}"
                    break
                text = a.log.read_text(encoding="utf-8", errors="replace")
                if re.search(r"Hosting game (?:at|on)\b", text, re.I):
                    ready = True
                    break
                time.sleep(1)
            if not ready and not problem:
                problem = "Dedicated server did not report hosting-ready state in time"
        finally:
            if proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
    output = a.log.read_text(encoding="utf-8", errors="replace")
    if re.search(r"Error while loading|Failed to load|Error while running|stack traceback", output, re.I):
        problem = "Factorio reported a startup error"
    if problem:
        print("TANKS-CI SERVER FAIL:", problem, file=sys.stderr)
        print("\n".join(output.splitlines()[-100:]), file=sys.stderr)
        return 1
    print("TANKS-CI SERVER_PASS private dedicated server hosting-ready")
    return 0

if __name__ == "__main__":
    sys.exit(main())
