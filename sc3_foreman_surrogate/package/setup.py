from pathlib import Path
import zipfile

print("[install] Starting SC3 package installation")

source = Path("collected/system_info.txt")
archive = Path("archive/archive.zip")
archive.parent.mkdir(exist_ok=True)

with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as output:
    output.write(source, arcname=source.name)

print("[install] Benign archive created")
print("[install] Installation finished")
