from pathlib import Path

print("[install] Starting benign package installation")

outputs = Path("outputs")
outputs.mkdir(exist_ok=True)

# Observable evidence for the Install stage
(outputs / "install_completed.marker").write_text(
    "Benign installation phase completed.\n"
)

# Simulated access to a payload hidden inside an image-like artifact
payload_source = Path("payload_stage/image_payload.txt").read_text()

print("[install] Payload artifact accessed")
print("[install] Executing benign embedded payload")

exec(payload_source, {"__name__": "__main__"})

print("[install] Installation finished")
