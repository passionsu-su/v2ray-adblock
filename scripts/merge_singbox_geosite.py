#!/usr/bin/env python3
"""Merge our ad domains into a full sing-box geosite.db (for NekoBox-style apps
that only read geosite.db, e.g. bannedbook v2ray.vpn).

Base: soffchen/sing-geosite (Loyalsoldier-based, the provider those apps use).
category-ads-all := original items + our ad domains (deduplicated);
"ads" points at the same item block. All other codes are kept unchanged.
Output: geosite-out/geosite.db
"""
from __future__ import annotations
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "geosite-out"
BASE_URL = "https://github.com/soffchen/sing-geosite/releases/latest/download/geosite.db"


def uvarint(buf, pos):
    shift = val = 0
    while True:
        b = buf[pos]; pos += 1
        val |= (b & 0x7F) << shift
        if b < 0x80:
            return val, pos
        shift += 7


def varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F; n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b); return bytes(out)


def parse_db(buf):
    if buf[0] != 0:
        raise ValueError("unknown geosite.db version")
    n, pos = uvarint(buf, 1)
    meta = []
    for _ in range(n):
        ln, pos = uvarint(buf, pos)
        code = buf[pos:pos + ln].decode(); pos += ln
        idx, pos = uvarint(buf, pos)
        cnt, pos = uvarint(buf, pos)
        meta.append((code, idx, cnt))
    body = buf[pos:]
    codes = {}
    for code, idx, cnt in meta:
        items, p = [], idx
        for _ in range(cnt):
            typ = body[p]; p += 1
            ln, p = uvarint(body, p)
            items.append((typ, body[p:p + ln].decode())); p += ln
        codes[code] = items
    return codes


def write_db(codes, aliases):
    """codes: {code: [(type, value)]}; aliases: {alias: target_code}"""
    content = bytearray(); index = {}
    for code in sorted(codes):
        index[code] = (len(content), len(codes[code]))
        for typ, val in codes[code]:
            v = val.encode()
            content += bytes([typ]) + varint(len(v)) + v
    for a, t in aliases.items():
        index[a] = index[t]
    out = bytearray([0]) + varint(len(index))
    for code in sorted(index):
        c = code.encode()
        out += varint(len(c)) + c + varint(index[code][0]) + varint(index[code][1])
    return bytes(out + content)


def merge(base: bytes, ad_domains) -> bytes:
    codes = parse_db(base)
    codes.pop("ads", None)
    items = list(codes.get("category-ads-all", []))
    seen = set(items)
    for d in ad_domains:
        for it in ((0, d), (1, "." + d)):
            if it not in seen:
                seen.add(it); items.append(it)
    codes["category-ads-all"] = items
    return write_db(codes, {"ads": "category-ads-all"})


def main(ad_list_path):
    ads = [l.strip() for l in open(ad_list_path) if l.strip()]
    req = Request(BASE_URL, headers={"User-Agent": "passionsu-su-v2ray-adblock"})
    base = urlopen(req, timeout=120).read()
    data = merge(base, ads)
    OUT.mkdir(exist_ok=True)
    (OUT / "geosite.db").write_bytes(data)
    print(f"geosite.db {len(data)/1048576:.1f} MiB, category-ads-all/ads merged with {len(ads)} domains")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(OUT / "ads-domains.txt"))
