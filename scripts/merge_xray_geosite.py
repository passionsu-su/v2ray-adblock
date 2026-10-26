#!/usr/bin/env python3
"""Merge our ad domains into a full Xray/V2Ray geosite.dat (for v2rayNG and
its forks, e.g. "Shadowrocket for Android", that read geosite.dat directly).

Base: Loyalsoldier/v2ray-rules-dat (the app's default Geo source).
CATEGORY-ADS-ALL := original domains + our ad domains (deduplicated);
ADS := the same list as a short alias. Every other tag is kept byte-for-byte.
Output: geosite-out/geosite.dat
Usage in routing:  geosite:category-ads-all   or   geosite:ads
"""
from __future__ import annotations
import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "geosite-out"
BASE_URL = "https://github.com/Loyalsoldier/v2ray-rules-dat/releases/latest/download/geosite.dat"
TARGET, ALIAS = "CATEGORY-ADS-ALL", "ADS"
ROOT_DOMAIN = 2


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


def field(num, data):
    return varint((num << 3) | 2) + varint(len(data)) + data


def fields(buf):
    """Yield (field_no, wire_type, value, raw_bytes) for one protobuf message."""
    pos = 0
    while pos < len(buf):
        start = pos
        key, pos = uvarint(buf, pos)
        fn, wt = key >> 3, key & 7
        if wt == 0:
            val, pos = uvarint(buf, pos)
        elif wt == 2:
            ln, pos = uvarint(buf, pos)
            val = buf[pos:pos + ln]; pos += ln
        elif wt == 5:
            val = buf[pos:pos + 4]; pos += 4
        elif wt == 1:
            val = buf[pos:pos + 8]; pos += 8
        else:
            raise ValueError(f"wire type {wt}")
        yield fn, wt, val, buf[start:pos]


def domain_key(dom: bytes):
    typ, value = 0, ""
    for fn, wt, val, _ in fields(dom):
        if fn == 1 and wt == 0:
            typ = val
        elif fn == 2 and wt == 2:
            value = val.decode()
    return typ, value


def encode_domain(d):
    return field(2, varint(1 << 3) + varint(ROOT_DOMAIN) + field(2, d.encode()))


def merge(base: bytes, ad_domains) -> bytes:
    entries, target_body = [], None
    for fn, wt, val, raw in fields(base):
        if fn != 1 or wt != 2:
            continue
        code = next((v.decode() for f, w, v, _ in fields(val) if f == 1), "").upper()
        if code == ALIAS:
            continue
        if code == TARGET:
            target_body = val
            entries.append(None)  # placeholder keeps original order
        else:
            entries.append(raw)
    if target_body is None:
        raise SystemExit(f"{TARGET} not found in base geosite.dat")

    seen, have_root = set(), set()
    for fn, wt, val, _ in fields(target_body):
        if fn == 2:
            k = domain_key(val); seen.add(k)
            if k[0] == ROOT_DOMAIN:
                have_root.add(k[1])
    added = bytearray(); n = 0
    for d in ad_domains:
        parts = d.split(".")
        # skip if this domain or a parent is already a RootDomain in the list
        if any(".".join(parts[i:]) in have_root for i in range(len(parts) - 1)):
            continue
        added += encode_domain(d); n += 1
    merged_body = bytes(target_body) + bytes(added)
    alias_body = field(1, ALIAS.encode()) + b"".join(
        raw for f, w, v, raw in fields(merged_body) if f == 2)

    out = bytearray()
    for raw in entries:
        out += field(1, merged_body) if raw is None else raw
    out += field(1, alias_body)
    print(f"{TARGET}: +{n} domains")
    return bytes(out)


def main(ad_list_path):
    ads = [l.strip() for l in open(ad_list_path) if l.strip()]
    req = Request(BASE_URL, headers={"User-Agent": "passionsu-su-v2ray-adblock"})
    base = urlopen(req, timeout=120).read()
    data = merge(base, ads)
    OUT.mkdir(exist_ok=True)
    (OUT / "geosite.dat").write_bytes(data)
    print(f"geosite.dat {len(data)/1048576:.1f} MiB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(OUT / "ads-domains.txt"))
