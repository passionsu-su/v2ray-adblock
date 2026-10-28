# v2rayNG AdBlock Rules

聚合 DNS、Hosts、AdGuard/ABP、Clash、Surge、Shadowrocket 等公开域名规则源，提取可转换的域名拦截规则，生成 v2rayNG 自定义路由规则 JSON。

## 输出文件

- `dist/v2rayng-adblock.json`：v2rayNG 可导入的 JSON 规则数组
- `dist/v2rayng-adblock.min.json`：紧凑版
- `dist/domains.txt`：去重域名
- `dist/sources-report.json`：逐来源抓取状态、解析数量和错误原因
- `dist/sources/*.json`：每个成功转换的来源单独生成一个 v2rayNG JSON；下方表格自动列出下载地址

首次 Actions 构建成功后，固定 Raw 地址为：
```
https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/v2rayng-adblock.json
https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/v2rayng-adblock.min.json
https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/domains.txt
https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources-report.json
```

## 完整 geosite.dat（Xray / V2Ray / Clash Meta / mihomo）

基于 Loyalsoldier 原版，保留全部分类（`cn`、`gfw`、`google`、`private`、`geolocation-!cn` 等），并新增广告分类 `category-ads-all` 和别名 `ads`（合并 217heidai、anti-AD、HaGeZi Pro、Loyalsoldier reject）。约 24 MB，Actions 每 12 小时随规则一起更新，发布在 `geosite` 分支。

```
https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/geosite/geosite.dat
```

国内直连慢可用镜像（jsDelivr 对超过 20 MB 的文件返回 403，不能用）：

```
https://ghfast.top/https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/geosite/geosite.dat
```

用法：

- 导入或替换时文件名必须保持 `geosite.dat`。
- Xray / v2rayNG 路由：`geosite:ads`（或 `geosite:category-ads-all`）→ block；`geosite:cn` → direct。
- Clash Meta for Android：「Meta 特性 → 导入 GeoSite 数据库」选择下载好的 `geosite.dat`，保持 Geodata 模式启用；DNS 可用 `geosite:cn,private`、`geosite:gfw`，规则可写 `GEOSITE,ads,REJECT`。

其他产物同在 `geosite` 分支：`geosite-adblock.dat`（仅广告分类）、`geosite.db` / `geosite-adblock.db`（sing-box）、`ads.mrs`、`heidai-adblockdns.mrs`、`hagezi-pro.mrs`（mihomo 规则集）。

## 各来源独立 JSON

每个成功解析的来源都会单独输出一个 JSON，域名只来自该来源，并应用 `custom/allowlist.txt` 排除项。该文件不会混入其他来源的域名；`custom/blocklist.txt` 仅用于原有汇总 JSON。表格由 Actions 构建自动更新。

<!-- SOURCE_JSON_TABLE_START -->
| 来源 | 状态 | 域名数 | 独立 JSON |
|---|---:|---:|---|
| 217heidai DNS Full | 成功 | 240932 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/01-217heidai-dns-full.json) |
| 217heidai DNS Lite | 成功 | 8488 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/02-217heidai-dns-lite.json) |
| anti-AD AdGuard | 成功 | 104521 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/03-anti-ad-adguard.json) |
| anti-AD EasyList | 成功 | 98833 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/04-anti-ad-easylist.json) |
| HaGeZi Pro | 成功 | 210731 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/05-hagezi-pro.json) |
| HaGeZi Ultimate (aggressive; disabled by default) | 未启用 | — | 未生成 |
| OISD Big | 成功 | 234269 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/07-oisd-big.json) |
| OISD Small (alternative) | 未启用 | — | 未生成 |
| AdGuard DNS filter | 成功 | 184036 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/09-adguard-dns-filter.json) |
| AdGuard Chinese filter | 成功 | 8791 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/10-adguard-chinese-filter.json) |
| AdGuard Base filter | 成功 | 16409 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/11-adguard-base-filter.json) |
| StevenBlack hosts | 成功 | 75953 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/12-stevenblack-hosts.json) |
| blackmatrix7 Advertising AdGuard | 成功 | 290184 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/13-blackmatrix7-advertising-adguard.json) |
| blackmatrix7 Advertising Clash YAML | 失败 | — | 未生成 |
| blackmatrix7 Advertising Shadowrocket | 失败 | — | 未生成 |
| Cats-Team AdRules DNS | 成功 | 204313 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/16-cats-team-adrules-dns.json) |
| Cats-Team AdRules ABP | 成功 | 220089 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/17-cats-team-adrules-abp.json) |
| Cats-Team AdRules Surge | 成功 | 204294 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/18-cats-team-adrules-surge.json) |
| GOODBYEADS DNS | 成功 | 121771 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/19-goodbyeads-dns.json) |
| GOODBYEADS ABP | 成功 | 139841 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/20-goodbyeads-abp.json) |
| NEO DEV HOST | 成功 | 116537 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/21-neo-dev-host.json) |
| 1Hosts Lite | 成功 | 102241 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/22-1hosts-lite.json) |
| 1Hosts Xtra (aggressive; disabled by default) | 未启用 | — | 未生成 |
| hBlock hosts | 成功 | 478706 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/24-hblock-hosts.json) |
| yhosts | 成功 | 6715 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/25-yhosts.json) |
| AWAvenue Ads Rule | 成功 | 969 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/26-awavenue-ads-rule.json) |
| REIJI007 DNS Lite | 成功 | 739489 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/27-reiji007-dns-lite.json) |
| REIJI007 Clash YAML | 失败 | — | 未生成 |
| DandelionSprout Anti-Malware | 成功 | 11602 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/29-dandelionsprout-anti-malware.json) |
| NoCoin | 成功 | 198 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/30-nocoin.json) |
| EasyList China + EasyList | 成功 | 54029 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/31-easylist-china-easylist.json) |
| CJX Annoyance List | 成功 | 522 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/32-cjx-annoyance-list.json) |
| 乘风 Adblock Plus Rule | 成功 | 270 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/33-adblock-plus-rule.json) |
| DandelionSprout adfilt | 成功 | 387 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/34-dandelionsprout-adfilt.json) |
| Loyalsoldier reject list | 成功 | 193578 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/35-loyalsoldier-reject-list.json) |
| Loyalsoldier Surge reject | 成功 | 193578 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/36-loyalsoldier-surge-reject.json) |
| Sukka non-IP reject | 成功 | 160 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/37-sukka-non-ip-reject.json) |
| Sukka domainset reject | 成功 | 1155 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/38-sukka-domainset-reject.json) |
| Sukka Shadowrocket domainset | 成功 | 145392 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/39-sukka-shadowrocket-domainset.json) |
| Sukka Shadowrocket non-IP reject | 成功 | 160 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/40-sukka-shadowrocket-non-ip-reject.json) |
| ACL4SSR BanAD | 成功 | 563 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/41-acl4ssr-banad.json) |
| ACL4SSR BanProgramAD | 成功 | 989 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/42-acl4ssr-banprogramad.json) |
| ACL4SSR BanEasyListChina | 成功 | 5045 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/43-acl4ssr-baneasylistchina.json) |
| Surfboard AdBlock | 成功 | 32129 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/44-surfboard-adblock.json) |
| xkww3n Rules reject | 成功 | 863 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/45-xkww3n-rules-reject.json) |
| neodevpro Clash | 成功 | 116537 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/46-neodevpro-clash.json) |
| xndeye rule-merger YAML | 失败 | — | 未生成 |
| AyraHikari AdGuard block | 失败 | — | 未生成 |
| DustinWin ads | 失败 | — | 未生成 |
| MetaCubeX category-ads-all text | 成功 | 159 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/50-metacubex-category-ads-all-text.json) |
| 217heidai Full AdGuard/ABP | 成功 | 11139 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/51-217heidai-full-adguard-abp.json) |
| 217heidai Surge Full | 成功 | 240932 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/52-217heidai-surge-full.json) |
| 217heidai Surge Lite | 未启用 | — | 未生成 |
| anti-AD Surge Domain Set | 成功 | 105192 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/54-anti-ad-surge-domain-set.json) |
| anti-AD Surge Rules | 成功 | 105192 | [下载 JSON](https://raw.githubusercontent.com/passionsu-su/v2ray-adblock/main/dist/sources/55-anti-ad-surge-rules.json) |
| blackmatrix7 AdvertisingLite Shadowrocket | 未启用 | — | 未生成 |
| blackmatrix7 Privacy Shadowrocket | 未启用 | — | 未生成 |
| Sukka extra domainset | 未启用 | — | 未生成 |
| Sukka reject-drop | 未启用 | — | 未生成 |
| Sukka reject-no-drop | 未启用 | — | 未生成 |
| Sukka Sogou input | 未启用 | — | 未生成 |
| Cats-Team AdRules Surge Domain Set | 未启用 | — | 未生成 |
| AWAvenue Surge RULE-SET | 未启用 | — | 未生成 |
| blackmatrix7 Privacy Clash YAML | 未启用 | — | 未生成 |
| blackmatrix7 AdvertisingLite Clash YAML | 未启用 | — | 未生成 |
<!-- SOURCE_JSON_TABLE_END -->

## 上游来源

当前 sources.json 收录 65 个入口，覆盖原 [passionsu-su/adblock](https://github.com/passionsu-su/adblock) 仓库中 Clash、Shadowrocket、AdGuard 配置列出的主要域名规则源，并增加 DNS/Hosts/ABP 原生文本入口。来源包括 217heidai、anti-AD、HaGeZi、OISD、AdGuard、StevenBlack、blackmatrix7、Cats-Team AdRules、GOODBYEADS、NEO DEV HOST、1Hosts、hBlock、yhosts、AWAvenue、REIJI007、DandelionSprout、NoCoin、EasyList China、CJX、乘风、Loyalsoldier、Sukka、ACL4SSR、Surfboard、xkww3n、xndeye、AyraHikari、DustinWin、MetaCubeX。并补齐 217heidai Surge/ABP、anti-AD Surge、blackmatrix7 AdvertisingLite/Privacy、Sukka extra/drop/no-drop/Sogou、Cats-Team 域名集和 AWAvenue Surge 等原仓库中的可转换来源。

每条来源的名称、原始 URL、声明格式及启用状态以 [sources.json](sources.json) 为准。

## 转换支持与限制

| 上游格式 | 转换方式 | 状态 |
|---|---|---|
| Hosts | 识别 0.0.0.0、127.0.0.1、::1 映射 | 支持 |
| DNS/纯域名 | 识别纯域名、domain:、full: | 支持 |
| AdGuard/ABP | 提取 `||example.com^`、URL 锚定规则主机名 | 部分支持 |
| V2Ray domain | 提取 `domain:example.com` | 支持 |
| Clash/Surge/Shadowrocket | 仅提取 DOMAIN、DOMAIN-SUFFIX | 部分支持 |
| YAML payload | 解析可识别的域名条目 | 部分支持 |

不能无损转换的内容会跳过：DOMAIN-KEYWORD、正则/复杂匹配、IP-CIDR、AdGuard 元素隐藏/CSS/脚本/重写、ABP 例外规则 `@@`、资源类型上下文规则、`.mrs` 二进制规则、RULE-SET/DOMAIN-SET 引用语句；Shadowrocket 模块（如 GMOogway、limbopro）和整份客户端配置（如 Johnshall）也不是可直接转换的纯域名列表。报告会保留逐来源状态。对于二进制规则，优先寻找同项目 YAML/TXT/AdGuard 等价源。

因此产物是**域名级拦截子集**，并不等价于完整 AdGuard/uBlock/Clash/Surge 过滤能力。共享域名广告、网页元素广告和 IP 直连广告可能无法拦截。

## v2rayNG 导入

1. 等待首次 GitHub Actions 构建成功。
2. 下载上方 Raw JSON 文件，或复制 JSON 全文。
3. 在 v2rayNG「路由设置」中使用从文件/剪贴板导入规则功能（菜单随版本变化）。
4. 确认出站标签为 `block`，并将广告规则放在可能先匹配的宽泛规则之前。

JSON 结构遵循 v2rayNG 自定义路由规则数组格式（domain、outboundTag、enabled、remarks 等字段）。本项目自动更新 GitHub 文件；客户端是否支持通过 URL 定期拉取，取决于所用版本，不能仅凭 Raw URL 保证自动订阅。

## 自动更新

GitHub Actions 每 12 小时执行一次，也支持手动触发。仅在产物变化时提交。单个来源失败会记入报告；成功来源数量或最终域名数量低于安全阈值时构建失败，不覆盖旧产物。

## 自定义规则

- `custom/allowlist.txt`：每行一个域名，从聚合结果排除。
- `custom/blocklist.txt`：每行一个域名，强制加入拦截。

## 版权与责任

各上游规则版权、许可证及使用条款归各原作者所有，请遵守其要求。本项目保留来源名称和 URL，仅做格式转换、规范化与去重。规则可能误拦截；如登录、支付、推送或 CDN 异常，优先排查并使用白名单。
