#!/usr/bin/env python3
"""Generate QR codes for published v2ray-adblock artifacts."""
from pathlib import Path
import qrcode

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qr-codes"
BASE = "https://raw.githubusercontent.com/passionsu-su/v2ray-adblock"
MAIN = BASE + "/main/dist/"
GEO = BASE + "/geosite/"

ARTIFACTS = {
    "aggregate": MAIN + "v2rayng-adblock.json",
    "aggregate-min": MAIN + "v2rayng-adblock.min.json",
    "china": MAIN + "v2rayng-adblock-cn.json",
    "china-min": MAIN + "v2rayng-adblock-cn.min.json",
    "global": MAIN + "v2rayng-adblock-global.json",
    "global-min": MAIN + "v2rayng-adblock-global.min.json",
    "domains": MAIN + "domains.txt",
    "domains-cn": MAIN + "domains-cn.txt",
    "domains-global": MAIN + "domains-global.txt",
    "sources-report": MAIN + "sources-report.json",
    "geosite-dat": GEO + "geosite.dat",
    "geosite-adblock-dat": GEO + "geosite-adblock.dat",
    "geosite-db": GEO + "geosite.db",
    "geosite-adblock-db": GEO + "geosite-adblock.db",
    "ads-mrs": GEO + "ads.mrs",
    "heidai-adblockdns-mrs": GEO + "heidai-adblockdns.mrs",
    "hagezi-pro-mrs": GEO + "hagezi-pro.mrs",
}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for path in OUT.glob("*.png"):
        path.unlink()
    for name, url in ARTIFACTS.items():
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        qr.make_image(fill_color="black", back_color="white").save(OUT / f"{name}.png")

    source_dir = ROOT / "dist" / "sources"
    for file in sorted(source_dir.glob("*.json")):
        url = MAIN + "sources/" + file.name
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        qr.make_image(fill_color="black", back_color="white").save(OUT / f"{file.stem}.png")
    print(f"Generated {len(list(OUT.glob('*.png')))} QR codes.")
if __name__ == "__main__":
    main()
