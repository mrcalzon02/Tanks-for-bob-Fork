#!/usr/bin/env python3
"""Create a reproducible installable ZIP from the current versioned source."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

from validate_mod import select_mod


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    source, metadata = select_mod()
    args.output.mkdir(parents=True, exist_ok=True)
    target = args.output / (source.name + '.zip')
    if target.exists():
        raise FileExistsError('Refusing to overwrite an existing package: ' + str(target))
    files = sorted(p for p in source.rglob('*') if p.is_file())
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in files:
            member = zipfile.ZipInfo(source.name + '/' + path.relative_to(source).as_posix(),
                                     date_time=(1980, 1, 1, 0, 0, 0))
            member.compress_type = zipfile.ZIP_DEFLATED
            member.external_attr = 0o100644 << 16
            archive.writestr(member, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=6)
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None, 'Corrupt package'
        assert json.loads(archive.read(source.name + '/info.json')) == metadata
        for path in files:
            assert archive.read(source.name + '/' + path.relative_to(source).as_posix()) == path.read_bytes()
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    checksum = target.with_suffix(target.suffix + '.sha256')
    checksum.write_text(digest + '  ' + target.name + '\n')
    print(json.dumps({'package': str(target.resolve()), 'sha256': digest,
                      'files': len(files), 'version': metadata['version'],
                      'factorio_version': metadata['factorio_version']}, indent=2))


if __name__ == '__main__':
    main()
