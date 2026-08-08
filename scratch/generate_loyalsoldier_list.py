import urllib.request
import os
import ssl
import datetime
import re

ssl._create_default_https_context = ssl._create_unverified_context

# 切换为 clash-rules 原生 YAML 规则源
SOURCES = {
    "gfw": "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/gfw.txt",
    "direct": "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/direct.txt",
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
        # 必须是 - 开头的行，过滤掉 payload: 等 YAML 头部
        if not line_stripped.startswith("-"):
            continue
            
        # 提取 - 后面的值，剥离可能的单双引号和首尾空格
        val = line_stripped[1:].strip().strip("'").strip('"').lower()
        if not val:
            continue
            
        # 自动判定域名与 IP，添加正确前缀
        # 1. 检测是否为 IP 地址或网段 (包含 / 或是纯数字组成的 IPv4)
        if "/" in val or re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', val):
            if ":" in val:  # IPv6 网段
                rules.append(f"IP-CIDR6,{val}")
            else:           # IPv4 网段或单 IP
                rules.append(f"IP-CIDR,{val}")
        # 2. 检测是否为域名
        else:
            # 剥离泛域名通配符前缀 +. 或者是 .
            if val.startswith("+."):
                val = val[2:]
            elif val.startswith("."):
                val = val[1:]
            
            rules.append(f"DOMAIN-SUFFIX,{val}")
            
    return rules

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 计算北京时间
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
        
        # 输出为标准的 .list 通用格式
        output_path = os.path.join(script_dir, f"{name}.list")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# 自动更新时间: {beijing_time_str}\n")
            f.write(f"# 来源: {url}\n\n")
            for rule in rules:
                f.write(rule + "\n")
                
        print(f"Successfully generated {name}.list with {len(rules)} rules at: {output_path}")

if __name__ == "__main__":
    main()
