"""Build an artifact-name inventory from retained files and archived creation records.

An archived `info.txt` record documents a file that existed during the original
build, even when that generated artifact is absent from the released snapshot.
This does NOT establish malicious behavior, and is NOT independent of Foreman
instrumentation. Provenance is included for every filename match.
"""
from pathlib import Path
import re

_CREATED = re.compile(r"^\S+ created (.+)$")


def collect_artifact_inventory(base_directory, relative_directories, include_archived_creations=True):
    inventory = {}
    for relative_directory in relative_directories:
        directory = (base_directory / relative_directory).resolve()
        if not directory.is_dir():
            raise FileNotFoundError(f"Scenario directory not found: {directory}")
        for item in directory.rglob('*'):
            if item.is_file():
                inventory.setdefault(item.name.lower(), []).append({
                    'kind': 'retained_file', 'source': str(item.relative_to(base_directory.parent))
                })
        if include_archived_creations:
            # `info.txt` is the unfiltered archived file-event record for Foreman;
            # use it solely to establish which *filenames were created*.
            info = directory / 'info.txt'
            if info.is_file():
                for n, line in enumerate(info.read_text(errors='replace').splitlines(), 1):
                    m = _CREATED.match(line.strip())
                    if m:
                        inventory.setdefault(Path(m.group(1)).name.lower(), []).append({
                            'kind': 'archived_creation_record',
                            'source': f'{info.relative_to(base_directory.parent)}:{n}',
                            'record': line.strip(),
                        })
    return inventory


def collect_filenames(base_directory, relative_directories):
    """Backward-compatible retained-file-only collection."""
    return set(collect_artifact_inventory(base_directory, relative_directories, False))
