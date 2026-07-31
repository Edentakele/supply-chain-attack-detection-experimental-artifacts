from pathlib import Path


def collect_filenames(base_directory, relative_directories):
    filenames = set()

    for relative_directory in relative_directories:
        directory = (base_directory / relative_directory).resolve()

        if not directory.exists():
            raise FileNotFoundError(f"Scenario directory not found: {directory}")

        for item in directory.rglob("*"):
            if item.is_file():
                filenames.add(item.name.lower())

    return filenames
