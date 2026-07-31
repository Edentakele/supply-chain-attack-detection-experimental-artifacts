from pathlib import Path
import shutil

print("[install] Starting SC5 software installer")

source = Path("package/resources/embedded_payload.bin")
destination = Path("payload/payload.bin")
destination.parent.mkdir(exist_ok=True)

shutil.copy2(source, destination)

print("[install] Embedded payload deployed")
print("[install] Installation phase finished")
