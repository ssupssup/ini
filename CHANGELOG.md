# Clash 订阅转换模板演进纪要



*   **2026-08-17 (apple-relay.akamaized.net 补齐与 auto_update.yml 自动合并脚本修复)**:
    *   **Apple AI PCC 通道补全**：在 `custom_static_apple_ai.list` 中补充 Akamai 节点的 Apple Private Relay 域名 `DOMAIN-SUFFIX,apple-relay.akamaized.net`，打通 Cloudflare、Fastly、Akamai 三方隐密云代理通道。
    *   **脚本自动合并与工作流修复**：重构 `build_apple_ai_list.py` 实现自动合并静态规则；修正 `auto_update.yml` 中的 Python 脚本调用文件名，彻底解决云端触发构建时上游覆盖抹除自定义域名的问题。
    *   **GitHub 同步**：提交并变基推送至 GitHub 远程仓库 (`ssupssup/ini` Commit `0becaba`) 🟢。

*   **2026-08-16 (iPhone 16 Pro App Store 后台发热掉电排障与 apple_ai.list 通配符清洗)**:
    *   **排障归因**：查明 App Store 前台 3 分钟/后台 21 分钟耗电 18% 根因：上游 Loon 规则库带入过宽通配符 `DOMAIN-SUFFIX,ls.apple.com`，导致 App Store 后台地理位置检索被误连至异地代理节点，引发地区 IP 冲突与高频重试唤醒发热。
    *   **精细清洗**：物理删除 `apple_ai.list` 中泛通配符 `DOMAIN-SUFFIX,ls.apple.com`，完整保留 Apple AI 专属防锁区域名 `DOMAIN-SUFFIX,gspe1-ssl.ls.apple.com` 与 Siri/PCC 中继通道，彻底解除 App Store 误杀并保障 Apple AI 正常使用。
    *   **GitHub 同步**：通过静态自检通过后，提交推送至 GitHub 远程仓库 (`ssupssup/ini`) 🟢。

*   **2026-08-13 (📹 油管视频策略组移动与快捷切组格式对齐)**:
    *   **位置与格式优化**：在 [260623.ini](file:///Users/shizupeng/Documents/antigravity/ini/260623.ini) 中，将 `📹 油管视频` 策略组物理前移至 `🕊️ Twitter(X)` 正上方（紧跟在 `🅢 Spotify` 下方）；格式由具体地区列表优化为 `🇭🇰 香港节点手动选择` + `.*` 标准正则匹配架构。
    *   **5 维校验与 GitHub 同步**：通过 `validate_ini_5d.py` 5 维离线双向映射与死链全量校验通过（0 缺失、0 死链）；已提交推送至 GitHub 远程仓库 (`ssupssup/ini` Commit `355ece3`) 🟢。

*   **2026-08-13 (BlackMatrix7 China 3,700+ 直连规则集挂载与 GitHub 物理同步)**:
    *   **直连防线补齐**：在 [260623.ini](file:///Users/shizupeng/Documents/antigravity/ini/260623.ini) 的 `ChinaDomain` 与 `ChinaCompanyIp` 之间精准插入 `ruleset=🎯 全球直连,blackmatrix7/China.list`。
    *   **决策归因**：物理比对证明该规则集能为现有 ACL4SSR 带来 **87.2%（3,228 条）** 的有效净增域名覆盖（补齐中小型网站、地方门户与二级 CDN），且对 J4125 软路由开销极小。
    *   **GitHub 同步**：通过静态语法自检通过后，提交推送至 GitHub 远程仓库 (`ssupssup/ini` Commit `416e2ae`) 🟢。

*   **2026-08-13 (Twitter/Telegram/LINE/网易音乐缺漏补全、BlackMatrix7源全量升级、SteamCN归口与 UnBan 注释固化及 5维防死链校验关环)**:
    *   **缺漏与新规则补齐**：恢复 `🕊️ Twitter(X)`、`📲 电报消息` (自建静态 CDN 补漏+主源双重架构)、`🎶 网易音乐`；新建 `🟩 LINE` 规则集及专属策略组（采用绿方块图标）。
    *   **策略组顺序与归口优化**：调整 `custom_proxy_group` 顺序，将 `📲 电报消息` 与 `🟩 LINE` 调至 Twitter 正下方并统一快捷切组格式；将 `🍎 苹果AI` 与 `🍎 苹果服务` 调至 `🧠 Ai平台` 正上方，实现 ruleset 与 custom_proxy_group 物理顺序 100% 像素级对齐重叠；将 `SteamCN` 归口改为 `🎮 游戏平台` 并在游戏组末尾就位。
    *   **修复死链与源升级**：排查并修复原 404 死链；将 Twitter、TikTok、油管、奈飞、微软云盘、巴哈姆特、哔哩哔哩(129条)、谷歌 FCM 及游戏全系升级为 BlackMatrix7 权威源。
    *   **双写去重与分析注释**：删除苹果 AI、微软服务、苹果服务的重复 ACL4SSR 规则行；保留 `UnBan.list` 并注入代码分析注释进行物理屏蔽。
    *   **红线制度与 5 维校验资产固化**：在 `.agents/AGENTS.md` 中落盘固化“未经授权绝对禁止删改/删除文件及配置”铁律；在 `clash_conversion_validator` 技能库中落盘 [validate_ini_5d.py](file:///Users/shizupeng/Documents/antigravity/.agents/skills/clash_conversion_validator/scripts/validate_ini_5d.py) 5 维双向 1:1 悬空与 HTTP 200 OK 在线死链诊断工具。

*   **2026-08-10 (Subconverter 架构精简与废弃服务/NVMe 硬盘路径物理清空)**:
    *   **架构分析与直连确认**：确认 OpenClash 订阅转换由原生 `subconverter-meta` 容器 (`25500`) 直接处理，渲染 INI 模板去 GitHub 在线拉取，已彻底废弃 Python 智能网关。
    *   **软路由物理清空**：彻底物理卸载软路由旧系统服务 `/etc/init.d/smart_subconverter`（同步移除 `/etc/rc.d/` 软链接），删除空置无用的 `/mnt/nvme0n1-4/subconverter` 硬盘目录。
    *   **缓存强清脚本精简**：覆写更新 `/root/clear_subconverter_cache.sh`，去除过时的硬盘路径命令，专注双 Docker 容器内部缓存强清；同步更新本地 Skill [subconverter_diagnostic_updater](file:///Users/shizupeng/Documents/antigravity/.agents/skills/subconverter_diagnostic_updater/SKILL.md)。

    *   **Subconverter 原生无壳拉起**：部署 `metacubex/subconverter:latest` 官方原生容器（命名为 `subconverter-meta`，监听 `25500` 端口，0 外壳、0 中间件）。
    *   **保留 tindy2013 备用容器**：建立 `subconverter-tindy` (`tindy2013/subconverter:latest`) 镜像容器并保持已停止状态，方便随时一键无缝切换。
    *   **OpenClash 节点无损补全**：激活 `/etc/openclash/custom/openclash_custom_overwrite.sh` 与 `/etc/openclash/custom/overwrite_engine.rb`，更新订阅时自动无损补回被 C++ 引擎丢弃的 29 个 Hysteria 2 节点，全量保留原生 `fingerprint` 指纹与 `ports` 跳跃端口属性。
    *   **一键强清缓存脚本**：升级 `/root/clear_subconverter_cache.sh`，一键物理清除双容器与固态硬盘 `/mnt/nvme0n1-4/subconverter/cache/` 上的所有历史 `.raw` 缓存快照。
    *   **只读审计与验证**：通过 Mihomo 内核语法校验（`test is successful`）与 RESTful API (`9090`) 实测，局域网设备外网连通性 100% 极速秒开 🟢。

*   **2026-08-08 (Apple AI 与苹果服务 Ruleset 顺序提前优化)**:
    *   **260623.ini 顺序重构**：将 `🍎 苹果AI`、`🍎 苹果服务`（blackmatrix7 与 ACL4SSR）及 `SteamCN 直连` 规则集整体移动至 `🧠 Ai平台` 规则集前方，确保 Apple AI 中继、Siri 智能搜索与苹果基础服务请求优先在顶部第一匹配完成，解决规则抢先截胡与断连问题。

*   **2026-08-08 (App Store CDN 域名顶层直连防护与第三方 AI 规则误杀截胡)**:
    *   **故障归因**：查明 iPhone 16 Pro 不开启小火箭在 iStoreOS 下 App Store 点击“全部更新”转圈退回故障，系第三方开源 AI 规则库 (`apple-intelligence-in-Loon`) 误将 App Store CDN 资源域名 `apps.mzstatic.com` 写入 AI 代理清单，且在订阅转换配置中排在 `direct.list` 之前抢先拦截，因代理节点限制/超时引发 App 切片下载失败。
    *   **顶层防杀覆盖**：在 OpenClash 自定义规则 (`openclash_custom_rules.list`) 顶层植入 `- DOMAIN-SUFFIX,apps.mzstatic.com,DIRECT`，利用自定义规则绝对最高优先级在 2226 行提前打中直连，彻底截胡后方 3748 行第三方 AI 规则的误杀。既保留云端 Apple AI 最新域名的自动跟进，又保障 App Store 满速直连更新 🟢。

*   **2026-08-08 (Telegram 4 大视频 CDN 域名补充与策略组首检红线固化)**:
    *   **电报静态 CDN 补漏**：在 `custom_static_telegram_proxy.list` 中补全 4 大电报视频 CDN 域名（`cdn-telegram.org`、`telegramdownload.com`、`telegram.space`、`telegram.dog`），并在 `260623.ini` 模板中精准放置在 `📲 电报消息` 首位，代码多余空行清除，推送 GitHub 远程仓库 🟢。
    *   **架构反思与规则固化**：厘清策略组仅为逻辑容器的物理本质，彻底纠正“策略组速度差异”的凭空臆测，将“策略组物理节点绑定首检红线”成功固化至 [.agents/AGENTS.md](file:///Users/shizupeng/Documents/antigravity/.agents/AGENTS.md)。

*   **2026-08-04 (Clash Verge 全局扩展脚本动态 TUN 开关代理重构与 4 大场景闭环测试)**:
    *   **动态 TUN 开关代理**：重构 Clash Verge 全局 JS 动态扩展脚本，将 `2. TUN 模块` 从硬编码禁用升级为由 UI 界面动作动态响应（`auto-route: tunEnable`，`stack: 'system'`，`dns-hijack: tunEnable ? ['any:53'] : []`）。
    *   **开即代理，关即无感**：实现勾选开启 TUN 模式自动激活 `utun` 接管代理日本节点；取消勾选 TUN 模式 100% 还原零干预且 53 端口零劫持，将路由完整归还系统与软路由网关。
    *   **4 大场景闭环通过**：经只读终端 `curl` / `scutil` 探测，单开系统代理、单开 TUN、系统代理+TUN 双开（日本 AWS 东京 `54.178.108.197` / `3.112.17.38`）以及两项全关（软路由网关 SG 新加坡 `13.212.156.204`）4 大场景 100.00% 物理测试验证通过 🟢。

*   **2026-08-02 (OpenClash 跨机场节点 Timeout 归因与三部曲全量自愈)**:
    *   **代理嵌套归因**：查明软路由 OpenClash 开启特定机场配置（如 `mitce`）时，网关将异地机场 (`lxy` / `可信`) 节点服务器域名当作常规流量塞入代理通道进行“代理套代理”嵌套转发，导致握手超时。
    *   **REALITY/CDN SNI 嗅探篡改归因与自愈**：查明 Bilibili CDN 伪装节点 (`bilibili-tw.biliimg.com` 等) 被 DNS 嗅探器改写 IP 物理机制，在 `skip-domain` 中追加 `'+.biliimg.com'` 豁免，实测 `台湾专线01` 与 `日本专线02` 100% 恢复秒通 🟢；深查并厘清 Apple SNI (`iosapps.itunes.apple.com`) 因客户端系统级证书钉扎 (Certificate Pinning) 防护物理致错原理，维持原直连决策。
    *   **物理自愈三部曲**：① **自定义直连**：`lxy1015.top`、`liangxin1.xyz`、`ioubha.cn`、`mhlnf.cn`、`tapcloud.icu` 指派 `DIRECT`；② **Real-IP 解析**：`fake-ip-filter` 加入 `+.ioubha.cn` 等；③ **嗅探豁免**：`skip-domain` 加入 `'+.tue.nl'`, `'+.biliimg.com'` 豁免 VLESS/CDN 伪装域名 IP 篡改，实测双端 100% 全量复活 🟢。

*   **2026-08-02 (Subconverter 外壳 GitHub 在线优先 + 0.01s 本地热备 + 纯血原节点无损交付)**:
    *   **双级降级调度**：重构 `smart_subconverter.py` 调度顺序为 GitHub 在线优先 (`https://raw.githubusercontent.com/ssupssup/ini/main/260623.ini`)；若超时或降级为 C++ 内置模板，0.01s 自动无感切回本地 `/base/260623.ini` 热备，彻底绝杀 `🔰 节点选择` 引起的 5 条 OpenClash 启动警告。
    *   **纯血无损交付**：整行无损恢复机场原生节点属性与 Hy2 端口范围 (`ports: 20200-20399`) 交付 OpenClash，实现策略组在线优先更新与全节点属性 100.00% 纯血零差异继承。

*   **2026-08-01 (Clash Verge 全局扩展脚本完成与 OpenClash 全量节点 100% 镜像核验)**:
    *   **Clash Verge 扩展脚本完成**：完成 Clash Verge 全局 JS 动态扩展脚本，实现域名白名单解耦 (`directDomains`, `fakeIpFilterDomains`)、DoH 自动指派与 `fake-ip-filter` 自动化配置，彻底解决 PC 端直连死锁。
    *   **全量节点 100% 镜像核验**：通过 SSH Python 比对脚本，对 `smart_subconverter` 转换后的 `lxy测速.yaml` 全部 51 个节点的全字段 Key-Value 属性（含 `skip-cert-verify`、`fingerprint`、`flow`、`reality-opts`）进行 1:1 物理审查，确认两端节点信息 100.00% 零差异精细对齐。

*   **2026-07-31 (OpenClash 覆写引擎原盘绝对保序与词界防越界重构)**:
    *   **原盘绝对保序**：物理以机场原始订阅 `added_names` 为排序基准，彻底消除 HY2 节点被堆在列表末尾问题，100% 保留机场初始交错次序。
    *   **词界防越界正则**：引入 `\b<CODE>\d*[\-_]?` 匹配模式；精细区分 `🎥 奈飞节点` 与 `🎥 奈飞视频`；剔除 UK 正则中与 `112.86 GB` 流量单位冲突的 `\bGB\b` 关键字，消除误吸收。
    *   **死锁自愈与子组还原**：加入 `sg != gname` 严格断言，彻底消除 `loop is detected in ProxyGroup [🎯 全球直连]` 环形自锁；补全自愈 19 大子策略组引用。三大机场全量 30+ 策略组 100.00% 校验通过！

*   **2026-07-30 (Clash 模板 260623.ini 恢复节点国旗 Emoji 显示)**: 移除 `emoji=false` 行，恢复单体节点前缀鲜艳国旗 Emoji 的高颜值视觉展示。配合底层稳健 Hook 脚本，节点属性与策略组自愈 100.00% 不受干扰。
*   **2026-07-30 (260623.ini 三类策略组精细治理与零信任审计)**:
    *   **三类策略组治理**：① 业务组 (`📲 电报消息` 等) 100% 保持固定子组引用，不乱塞单体节点；② 通配组 (行尾带 `.*` 的全量 15 个组) 展开前置引用 + 全量单体节点；③ 地域组 (`🇭🇰 香港节点` 等) 根据正则精准装载具体单体节点 (含全量 Hy2)。
    *   **全属性 100% 镜像**：原版 `skip-cert-verify: true` 等 Key-Value 属性 100.00% 物理镜像保存，彻底解决 Subconverter 属性篡改降级问题。
    *   **资产固化与零信任**：固化 [openclash_custom_overwrite_guard](file:///Users/shizupeng/Documents/antigravity/.agents/skills/openclash_custom_overwrite_guard/SKILL.md) 技能库；新建 [clash_node_attribute_auditor](file:///Users/shizupeng/Documents/antigravity/.agents/skills/clash_node_attribute_auditor/SKILL.md) 零信任现场在线拉取审计技能。实测 131 个节点数、全 Key-Value 属性及物理出现顺序 100.00% 像素级零差异对齐。
*   **2026-07-30 (Clash 模板 260623.ini 极致精简与 Hook 归口解耦)**: 移除了 `260623.ini` 模板中冗余失效的 `rename` 物理行，仅保留 `emoji=false` 用于节点去国旗 Emoji。将所有非代理提示节点（到期/流量/导航/超时/重置等）的整条物理擦除以及全属性镜像复刻统一交由软路由 OpenClash 动态 Hook 脚本集中处理。
*   **2026-07-30 (Clash 模板 260623.ini 开启 emoji=false 与提示节点物理擦除)**: 模板新增 `emoji=false`（全局擦除国旗 Emoji），实现节点名称清爽规范，静态校验通过并同步推送至 GitHub (`ssupssup/ini`)。

*   **2026-07-27 (Clash 模板 260623.ini 全网统一测速参数 300,50,3000)**: 统一 15 个测速策略组参数为 300,50,3000（5分钟轮询/50ms容差/3000ms超时），消除过短 Timeout 对跨洋优质节点的误杀。

---

> [!TIP]
> 2026-07-25 之前更早的历史变更日志已物理归档至 [history_changelog.md](file:///Users/shizupeng/Documents/antigravity/ini/references/history_changelog.md)。
