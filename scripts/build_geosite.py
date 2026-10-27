#!/usr/bin/env python3
"""Build geosite-adblock.dat for v2rayNG / Xray / V2Ray.

Sources: 217heidai DNS Full, anti-AD AdGuard, HaGeZi Pro, Loyalsoldier reject list.
Tag inside the dat:
  ads   all four sources merged, parent-domain deduplicated
Usage in a routing rule:  "domain": ["ext:geosite-adblock.dat:ads"]
Also writes geosite-adblock.db (sing-box geosite format, code "ads").
"""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import parse, fetch, custom  # reuse the existing parser

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "geosite-out"
SOURCES = [
    ("217heidai", "https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/adblockdns.txt"),
    ("anti-ad", "https://raw.githubusercontent.com/privacy-protection-tools/anti-AD/master/anti-ad-adguard.txt"),
    ("hagezi", "https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/pro.txt"),
    ("loyalsoldier", "https://raw.githubusercontent.com/Loyalsoldier/v2ray-rules-dat/release/reject-list.txt"),
]
MIN_DOMAINS = 50000
ROOT_DOMAIN = 2  # v2ray Domain.Type.RootDomain ("domain:")


def varint(n: int) -> bytes:
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def field_bytes(num: int, data: bytes) -> bytes:
    return varint((num << 3) | 2) + varint(len(data)) + data


def encode_geosite(tag: str, domains) -> bytes:
    body = bytearray(field_bytes(1, tag.upper().encode()))
    for d in domains:
        dom = varint((1 << 3) | 0) + varint(ROOT_DOMAIN) + field_bytes(2, d.encode())
        body += field_bytes(2, dom)
    return field_bytes(1, bytes(body))  # one entry of GeoSiteList


def encode_singbox_db(code: str, domains) -> bytes:
    """sing-box geosite.db (version 0). RootDomain -> Domain + DomainSuffix('.x'), as sing-geosite does."""
    items = bytearray()
    count = 0
    for d in domains:
        for typ, val in ((0, d), (1, "." + d)):
            v = val.encode()
            items += bytes([typ]) + varint(len(v)) + v
            count += 1
    c = code.encode()
    header = bytes([0]) + varint(1) + varint(len(c)) + c + varint(0) + varint(count)
    return header + bytes(items)


def dedup_parents(domains):
    s = set(domains)
    keep = []
    for d in s:
        parts = d.split(".")
        if not any(".".join(parts[i:]) in s for i in range(1, len(parts) - 1)):
            keep.append(d)
    return sorted(keep)


def main():
    allow = custom("allowlist.txt")
    forced = custom("blocklist.txt")
    per, merged, report = {}, set(), []
    for tag, url in SOURCES:
        try:
            got = parse(fetch(url)) - allow
            if len(got) < 1000:
                raise ValueError(f"only {len(got)} domains")
            per[tag] = got
            merged |= got
            report.append({"tag": tag, "url": url, "status": "ok", "domains": len(got)})
        except Exception as exc:
            report.append({"tag": tag, "url": url, "status": "error", "error": str(exc)})
            print(f"[WARN] {tag}: {exc}", file=sys.stderr)
    merged |= forced
    merged -= allow
    ads = dedup_parents(merged)
    if len(per) < 3 or len(ads) < MIN_DOMAINS:
        raise SystemExit(f"Refusing publish: {len(per)} sources, {len(ads)} domains")

    data = bytearray(encode_geosite("ads", ads))
    OUT.mkdir(exist_ok=True)
    (OUT / "geosite-adblock.dat").write_bytes(bytes(data))
    (OUT / "geosite-adblock.db").write_bytes(encode_singbox_db("ads", ads))
    (OUT / "ads-domains.txt").write_text("\n".join(ads) + "\n", encoding="utf-8")
    # mihomo 源文件（+. 前缀 = 含子域名），由工作流转换成 .mrs
    src = OUT / "mrs-src"; src.mkdir(exist_ok=True)
    def plus(lst): return "".join("+." + d + "\n" for d in lst)
    (src / "ads.txt").write_text(plus(ads), encoding="utf-8")
    for tag, name in (("hagezi", "hagezi-pro"), ("217heidai", "heidai-adblockdns")):
        if tag in per:
            (src / f"{name}.txt").write_text(plus(dedup_parents(per[tag])), encoding="utf-8")
    (OUT / "geosite-report.json").write_text(json.dumps({
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "ads_domains": len(ads),
        "sources": report,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ads={len(ads)} size={len(data)/1048576:.1f} MiB")


if __name__ == "__main__":
    main()
