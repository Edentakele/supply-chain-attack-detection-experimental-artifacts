from pathlib import Path
import shutil

print("[install] Starting SC7 package installation")

source = Path("package/model_payload.bin")
destination = Path("service/model_payload.bin")
destination.parent.mkdir(exist_ok=True)

shutil.copy2(source, destination)

print("[install] Model payload deployed")
print("[install] Installation finished")
