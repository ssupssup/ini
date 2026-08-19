import urllib.request
import os
import ssl
import datetime
import re

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SOURCES = {
        "telegramcidr": "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/telegramcidr.txt"
}

def download_url(url):
    print(f"Downloading: {url}")
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Quantumult X/1.4.3'}
        )
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

def parse_clash_rules(content):
    rules = []
    lines = content.splitlines()
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped.startswith("-"):
            continue
            
        val = line_stripped[1:].strip().strip("'").strip('"').lower()
        if not val:
            continue
            
        if "/" in val or re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', val):
            if ":" in val:
                rules.append(f"IP-CIDR6,{val}")
            else:
                rules.append(f"IP-CIDR,{val}")
        else:
            if val.startswith("+."):
                val = val[2:]
            elif val.startswith("."):
                val = val[1:]
            
            rules.append(f"DOMAIN-SUFFIX,{val}")
            
    return rules

def main():
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    beijing_time_str = beijing_now.strftime('%Y-%m-%d %H:%M:%S')
    
    for name, url in SOURCES.items():
        content = download_url(url)
        if not content:
            print(f"Error: Failed to fetch rules for {name}")
            continue
            
        print(f"Parsing Clash YAML rules for {name}...")
        rules = parse_clash_rules(content)
        
        output_path = os.path.join(BASE_DIR, f"{name}.list")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# 自动更新时间: {beijing_time_str}\n")
            f.write(f"# 来源: {url}\n\n")
            for rule in rules:
                f.write(rule + "\n")
                
        print(f"Successfully generated {name}.list with {len(rules)} rules at: {output_path}")

        # 如果处理的是 telegramcidr，则自动与 custom_static_telegram_proxy.list 融合生成每日更新的 telegram_proxy.list
        if name == "telegramcidr":
            print("\n=== Generating Combined telegram_proxy.list ===")
            combined_rules = []
            seen = set()
            
            custom_static_path = os.path.join(BASE_DIR, "custom_static_telegram_proxy.list")
            if os.path.exists(custom_static_path):
                print(f"Reading static Telegram custom rules: {custom_static_path}")
                with open(custom_static_path, "r", encoding="utf-8") as f:
                    static_content = f.read()
                for line in static_content.splitlines():
                    line_stripped = line.strip()
                    if line_stripped and not line_stripped.startswith("#"):
                        norm = line_stripped.replace(" ", "").lower()
                        if norm not in seen:
                            seen.add(norm)
                            combined_rules.append(line_stripped)
            
            for rule in rules:
                rule_with_no_resolve = f"{rule},no-resolve" if not rule.endswith(",no-resolve") else rule
                norm = rule_with_no_resolve.replace(" ", "").lower()
                if norm not in seen:
                    seen.add(norm)
                    combined_rules.append(rule_with_no_resolve)
                    
            telegram_proxy_path = os.path.join(BASE_DIR, "telegram_proxy.list")
            with open(telegram_proxy_path, "w", encoding="utf-8") as f:
                f.write(f"# 自动更新时间: {beijing_time_str}\n")
                f.write("# === Telegram 动态整合 CDN 域名与 CIDR 规则集 ===\n\n")
                for rule in combined_rules:
                    f.write(rule + "\n")
            print(f"Successfully generated combined telegram_proxy.list with {len(combined_rules)} rules at: {telegram_proxy_path}")

if __name__ == "__main__":
    main()
