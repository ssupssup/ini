#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPSTREAM_URL = "https://raw.githubusercontent.com/CFJaychow526/apple-intelligence-in-Loon/refs/heads/main/AppleAI_relay.list"
OUTPUT_FILE = os.path.join(BASE_DIR, "apple_ai.list")

EXCLUDE_DOMAINS = ["apps.mzstatic.com"]
STATIC_CUSTOM_RULES = [
    "DOMAIN,captive.apple.com"
]

def main():
    print("🚀 开始抓取并清洗 Apple AI 规则集...")
    rules = set()

    # 1. 纯粹从上游 Loon 源抓取
    try:
        req = urllib.request.Request(UPSTREAM_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            for line in content.splitlines():
                line_str = line.strip()
                if not line_str or line_str.startswith("#") or line_str.startswith(";"):
                    continue
                # 剔除误杀黑名单
                if any(ex in line_str for ex in EXCLUDE_DOMAINS):
                    print(f"   ✂️ 已剔除黑名单误杀规则: {line_str}")
                    continue
                rules.add(line_str)
        print("   🟢 上游 AppleAI_relay.list 抓取并过滤成功")
    except Exception as e:
        print(f"   ⚠️ 上游抓取失败: {e}")

    # 2. 追加用户自定义静态精细化强代理规则
    for sr in STATIC_CUSTOM_RULES:
        rules.add(sr)
        print(f"   ➕ 成功静态编译追加精细化代理规则: {sr}")

    # 3. 排序与输出
    sorted_rules = sorted(list(rules))
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 🍎 苹果 AI 专属分流规则集 (自用自动清洗版)\n")
        f.write("# 来源: 上游 Loon 权威源 (已剔除 apps.mzstatic.com)\n")
        f.write(f"# 总计规则条数: {len(sorted_rules)}\n\n")
        for r in sorted_rules:
            f.write(f"{r}\n")

    print(f"✅ 生成 [apple_ai.list] 成功！共计 {len(sorted_rules)} 条精细化规则。")

if __name__ == "__main__":
    main()
