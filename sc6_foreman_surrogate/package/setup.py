from pathlib import Path
import zipfile

print("[build] Starting SC6 build process")

config = Path("source/build_config.py")
config.write_text('BUILD_MODE = "instrumented"\n')
print("[build] Build configuration modified")

artifact = Path("artifact/build_artifact.zip")
artifact.parent.mkdir(exist_ok=True)

with zipfile.ZipFile(artifact, "w", zipfile.ZIP_DEFLATED) as archive:
    archive.write(config, arcname="build_config.py")

print("[build] Artifact package created")
print("[build] Build process finished")
