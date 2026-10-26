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

## 各来源独立 JSON

每个成功解析的来源都会单独输出一个 JSON，域名只来自该来源，并应用 `custom/allowlist.txt` 排除项。该文件不会混入其他来源的域名；`custom/blocklist.txt` 仅用于原有汇总 JSON。表格由 Actions 构建自动更新。

<!-- SOURCE_JSON_TABLE_START -->
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
