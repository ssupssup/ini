#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPSTREAM_URL = "https://raw.githubusercontent.com/CFJaychow526/apple-intelligence-in-Loon/refs/heads/main/AppleAI_relay.list"
STATIC_FILE = os.path.join(BASE_DIR, "custom_static_apple_ai.list")
OUTPUT_FILE = os.path.join(BASE_DIR, "apple_ai.list")

EXCLUDE_DOMAINS = ["apps.mzstatic.com"]

def main():
    print("🚀 开始抓取并清洗 Apple AI 规则集...")
    rules = set()

    # 1. 从上游 Loon 源抓取
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
        print(f"   ⚠️ 上游抓取失败，降级使用已有规则: {e}")

    # 2. 读取本地静态补充文件
    if os.path.exists(STATIC_FILE):
        with open(STATIC_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line_str = line.strip()
                if line_str and not line_str.startswith("#") and not line_str.startswith(";"):
                    rules.add(line_str)
        print("   🟢 本地 custom_static_apple_ai.list 叠加成功")

    # 强制确保精细化全域名规则存在
    rules.add("DOMAIN,sequoia.cdn-apple.com")

    # 3. 排序与输出
    sorted_rules = sorted(list(rules))
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("# 🍎 苹果 AI 专属分流规则集 (自用自动清洗合并版)\n")
        f.write("# 包含: 上游 Loon 权威源 (已剔除 apps.mzstatic.com) + 本地 encrypted-tbn 搜索物料补充\n")
        f.write(f"# 总计规则条数: {len(sorted_rules)}\n\n")
        for r in sorted_rules:
            f.write(f"{r}\n")

    print(f"✅ 生成 [apple_ai.list] 成功！共计 {len(sorted_rules)} 条精细化规则。")

if __name__ == "__main__":
    main()
