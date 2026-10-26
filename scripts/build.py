#!/usr/bin/env python3
"""Aggregate compatible domain rules from DNS/Hosts/ABP/Clash/Surge formats."""
from __future__ import annotations
import ipaddress, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"
UA = "passionsu-su-v2ray-adblock/2.1"
MAX_BYTES = 30 * 1024 * 1024
MIN_SUCCESS = 4
MIN_DOMAINS = 5000

def domain_ok(value):
    s = value.strip().lower().rstrip(".")
    for prefix in ("domain:", "full:", "+."):
        if s.startswith(prefix):
            s = s[len(prefix):]
    s = s.lstrip(".")
    if not s or len(s) > 253 or any(c in s for c in "/*^$!@:#?[]{}\\"):
        return None
    try:
        ipaddress.ip_address(s)
        return None
    except ValueError:
        pass
    try:
        s = s.encode("idna").decode("ascii")
    except UnicodeError:
        return None
    parts = s.split(".")
    if len(parts) < 2 or any(
        len(p) > 63 or not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]*[a-z0-9])?", p)
        for p in parts
    ):
        return None
    if parts[-1] in {"local", "localhost", "test", "invalid", "example"}:
        return None
    return s

def add(out, token):
    d = domain_ok(token)
    if d:
        out.add(d)

def parse(text):
    out = set()
    for raw in text.replace("\ufeff", "").splitlines():
        s = raw.strip()
        if not s or s.startswith(("!", "##", "#$#", "#@#", "@@", "[Adblock", "[General", "[Rule", "//", ";")):
            continue
        # Hosts
        m = re.match(r"^(?:0\.0\.0\.0|127\.0\.0\.1|::1|::)\s+(.+)$", s, re.I)
        if m:
            for token in m.group(1).split():
                add(out, token)
            continue
        # AdGuard / ABP domain anchors and URL anchors
        if s.startswith("||"):
            host = re.split(r"[\^/$*|]", s[2:], maxsplit=1)[0]
            add(out, host)
            continue
        if s.startswith("|https://") or s.startswith("|http://"):
            host = re.split(r"[/^|:$]", re.sub(r"^\|https?://", "", s), maxsplit=1)[0]
            add(out, host)
            continue
        # Clash / Surge / Shadowrocket: only exact/suffix domain semantics
        if re.match(r"(?i)^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-SET),", s):
            bits = [x.strip() for x in s.split(",")]
            if len(bits) > 1 and bits[0].upper() in ("DOMAIN", "DOMAIN-SUFFIX"):
                add(out, bits[1])
            continue
        # YAML payload lists and plain domain lists
        if s.startswith("- "):
            s = s[2:].strip().strip("'\"")
        if s.startswith("payload:"):
            continue
        if s.startswith("domain:"):
            add(out, s)
            continue
        if re.fullmatch(r"[A-Za-z0-9.*_-]+\.?", s) and "*" not in s:
            add(out, s)
    return out

def fetch(url):
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/plain,*/*"})
    with urlopen(req, timeout=60) as response:
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("exceeds 30 MiB safety cap")
    return data.decode("utf-8", errors="replace")

def custom(filename):
    path = ROOT / "custom" / filename
    out = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                add(out, line)
    return out

def main():
    sources = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    merged, report, successes = set(), [], 0
    per_source = []
    for index, item in enumerate(sources, 1):
        row = {"name": item["name"], "url": item["url"], "format": item["format"]}
        if not item.get("enabled", True):
            row["status"] = "disabled"
            report.append(row)
            continue
        try:
            parsed = parse(fetch(item["url"]))
            if len(parsed) < 50:
                raise ValueError(f"only {len(parsed)} compatible domains parsed")
            merged.update(parsed)
            safe = re.sub(r"[^a-z0-9]+", "-", item["name"].lower()).strip("-") or f"source-{index:02d}"
            filename = f"{index:02d}-{safe}.json"
            row.update(status="ok", domains=len(parsed), json_file=f"sources/{filename}")
            per_source.append((filename, item["name"], parsed))
            successes += 1
        except Exception as exc:
            row.update(status="error", error=f"{type(exc).__name__}: {exc}")
            print(f"[WARN] {item['name']}: {row['error']}", file=sys.stderr)
        report.append(row)

    allow = custom("allowlist.txt")
    forced = custom("blocklist.txt")
    merged.difference_update(allow)
    merged.update(forced)

    if successes < MIN_SUCCESS:
        raise SystemExit(f"Refusing publish: only {successes} source(s) succeeded")
    if len(merged) < MIN_DOMAINS:
        raise SystemExit(f"Refusing publish: only {len(merged)} unique domains")

    OUT.mkdir(exist_ok=True)
    source_dir = OUT / "sources"
    source_dir.mkdir(exist_ok=True)
    for old_file in source_dir.glob("*.json"):
        old_file.unlink()
    for filename, source_name, source_domains in per_source:
        filtered = source_domains - allow
        source_rules = [{
            "port": "",
            "outboundTag": "block",
            "domain": ["domain:" + d for d in sorted(filtered)],
            "enabled": True,
            "remarks": f"AdBlock - {source_name} ({len(filtered)} domains)"
        }]
        (source_dir / filename).write_text(
            json.dumps(source_rules, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    domains = sorted(merged)
    rules = [{
        "port": "",
        "outboundTag": "block",
        "domain": ["domain:" + d for d in domains],
        "enabled": True,
        "remarks": f"AdBlock merged ({len(domains)} domains)"
    }]
    (OUT / "v2rayng-adblock.json").write_text(
        json.dumps(rules, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "v2rayng-adblock.min.json").write_text(
        json.dumps(rules, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8"
    )
    (OUT / "domains.txt").write_text("\n".join(domains) + "\n", encoding="utf-8")
    report_data = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "unique_domains": len(domains),
        "source_success": successes,
        "source_total": len(sources),
        "allowlist_entries": len(allow),
        "custom_block_entries": len(forced),
        "sources": report
    }
    (OUT / "sources-report.json").write_text(
        json.dumps(report_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    # Keep README links synchronized with successfully generated files.
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    start_marker, end_marker = "<!-- SOURCE_JSON_TABLE_START -->", "<!-- SOURCE_JSON_TABLE_END -->"
    rows = ["| 来源 | 状态 | 域名数 | 独立 JSON |", "|---|---:|---:|---|"]
    for row in report:
        if row.get("status") == "ok":
            url = f"https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/{row['json_file']}"
            state, count, link = "成功", str(row.get("domains", 0)), f"[下载 JSON]({url})"
        elif row.get("status") == "disabled":
            state, count, link = "未启用", "—", "未生成"
        else:
            state, count, link = "失败", "—", "未生成"
        rows.append(f"| {row['name']} | {state} | {count} | {link} |")
    block = start_marker + "\n" + "\n".join(rows) + "\n" + end_marker
    if start_marker in readme and end_marker in readme:
        readme = readme.split(start_marker, 1)[0] + block + readme.split(end_marker, 1)[1]
    else:
        readme += "\n\n## 各来源独立 JSON\n\n" + block + "\n"
    readme_path.write_text(readme, encoding="utf-8")
    print(f"Generated {len(per_source)} per-source JSON files.")
    print(f"Generated {len(domains)} unique aggregate domains; {successes}/{len(sources)} enabled sources succeeded.")

if __name__ == "__main__":
    main()
