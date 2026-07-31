from pathlib import Path
import platform

print("[install] Starting SC4 package installation")

cache = Path("cache")
exfil = Path("exfil")
cache.mkdir(exist_ok=True)
exfil.mkdir(exist_ok=True)

(cache / "audit-cache").write_text(
    "BENIGN_SC4_CACHE_TOKEN\n"
)
print("[install] Cache token created")

token = (cache / "audit-cache").read_text()

Path("payload.js").write_text(
    "// Benign SC4 payload artifact\n"
    f"const token = {token.strip()!r};\n"
)
print("[install] Payload artifact prepared")

(exfil / "system_info.txt").write_text(
    f"system={platform.system()}\n"
    f"machine={platform.machine()}\n"
)
print("[install] Benign system information collected")

print("[install] Installation finished")
