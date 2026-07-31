from pathlib import Path
import shutil

print("[install] Starting SC2 package installation")

startup = Path("startup")
outputs = Path("outputs")
startup.mkdir(exist_ok=True)
outputs.mkdir(exist_ok=True)

# Persistence Setup
(startup / "sc2_autostart.conf").write_text(
    "command=outputs/installed_payload.txt\n"
)
print("[install] Persistence configuration created")

# Payload Installation
shutil.copy2(
    "package/benign_payload.txt",
    outputs / "installed_payload.txt"
)
print("[install] Benign payload installed")

print("[install] Installation finished")
