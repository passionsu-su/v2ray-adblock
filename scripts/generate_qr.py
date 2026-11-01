#!/usr/bin/env python3
"""Generate v2rayNG-importable routing ruleset QR codes.

v2rayNG「从二维码导入规则集」/「从剪贴板导入规则集」只接受二维码/剪贴板里
直接就是规则 JSON 数组（Array<RulesetItem>），不会下载 URL。
域名列表 JSON 动辄几百 KB~几十 MB，远超二维码约 2.9 KB 的容量，
所以这里的规则只引用 geosite-adblock.dat / geosite.dat 中的分类，
体积很小，可直接扫码或复制导入。
Output: qr-codes/<name>.png + qr-codes/<name>.json（同内容，便于复制）
"""
from pathlib import Path
import json
import qrcode

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "qr-codes"


def rule(remarks, outbound, **kw):
    item = {"remarks": remarks, "outboundTag": outbound}
    item.update(kw)
    item["enabled"] = True
    return item


CN_DNS_IP = ["223.5.5.5", "223.6.6.6", "2400:3200::1", "2400:3200:baba::1", "119.29.29.29",
             "1.12.12.12", "120.53.53.53", "2402:4e00::", "2402:4e00:1::", "180.76.76.76",
             "2400:da00::6666", "114.114.114.114", "114.114.115.115"]

WHITELIST_TAIL = [
    rule("代理Google", "proxy", domain=["geosite:google"]),
    rule("绕过局域网IP", "direct", ip=["geoip:private"]),
    rule("绕过局域网域名", "direct", domain=["geosite:private"]),
    rule("绕过中国公共DNS IP", "direct", ip=CN_DNS_IP),
    rule("绕过中国公共DNS域名", "direct", domain=["domain:alidns.com", "domain:doh.pub", "domain:dot.pub", "domain:360.cn", "domain:onedns.net"]),
    rule("绕过中国IP", "direct", ip=["geoip:cn"]),
    rule("绕过中国域名", "direct", domain=["geosite:cn"]),
]

RULESETS = {
    # 需要在 v2rayNG「资源文件」里添加 geosite-adblock.dat
    "adblock-all": [rule("去广告-全部", "block", domain=["ext:geosite-adblock.dat:ads"])],
    "adblock-cn": [rule("去广告-国内", "block", domain=["ext:geosite-adblock.dat:ads-cn"])],
    "adblock-global": [rule("去广告-国外", "block", domain=["ext:geosite-adblock.dat:ads-global"])],
    "adblock-all-cn-whitelist": [
        rule("阻断udp443", "block", port="443", network="udp"),
        rule("去广告-全部", "block", domain=["ext:geosite-adblock.dat:ads"]),
    ] + WHITELIST_TAIL,
    # 只需把 v2rayNG 的 geosite.dat 换成本仓库的完整版（无需额外资源文件）
    "geosite-ads": [rule("去广告", "block", domain=["geosite:category-ads-all"])],
    "geosite-ads-cn-whitelist": [
        rule("阻断udp443", "block", port="443", network="udp"),
        rule("去广告", "block", domain=["geosite:category-ads-all"]),
    ] + WHITELIST_TAIL,
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for path in list(OUT.glob("*.png")) + list(OUT.glob("*.json")):
        path.unlink()
    for name, rules in RULESETS.items():
        text = json.dumps(rules, ensure_ascii=False, separators=(",", ":"))
        if len(text.encode("utf-8")) > 2800:
            raise SystemExit(f"{name}: {len(text)} bytes, too large for a QR code")
        (OUT / f"{name}.json").write_text(text + "\n", encoding="utf-8")
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=8, border=4)
        qr.add_data(text.encode("utf-8"))
        qr.make(fit=True)
        qr.make_image(fill_color="black", back_color="white").save(OUT / f"{name}.png")
    print(f"Generated {len(RULESETS)} ruleset QR codes.")


if __name__ == "__main__":
    main()
