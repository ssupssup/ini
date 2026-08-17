import urllib.request
import re
import sys
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

COMMUNITY_RULES_URL = "https://raw.githubusercontent.com/LOWERTOP/Shadowrocket-First/refs/heads/main/Talkatone.sgmodule"

AD_SOURCES = {
    "Unity": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Unity/Unity.yaml",
    "AppLovin": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/AppLovin/AppLovin.yaml"
}

WHITELIST_DOMAINS = [
    "google.com", "youtube.com", "googleapis.com", "gstatic.com",
    "googleusercontent.com", "ggpht.com", "gvt1.com", "1e100.net",
    "amazon.com", "amazonaws.com", "amazonaws.com.cn", "cloudfront.net"
]

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

def is_whitelisted(domain):
    domain_lower = domain.lower().strip('.')
    for white in WHITELIST_DOMAINS:
        if domain_lower == white or domain_lower.endswith('.' + white):
            return True
    return False

def parse_clash_yaml(yaml_content):
    rules = []
    lines = yaml_content.splitlines()
    payload_section = False
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue
            
        if line_stripped.startswith("payload:"):
            payload_section = True
            continue
            
        if payload_section:
            match = re.search(r'^-\s+([^,]+),([^,]+)(?:,.+)?', line_stripped)
            if match:
                rule_type = match.group(1).strip().upper()
                value = match.group(2).strip().lower()
                rules.append((rule_type, value))
                
    return rules

def generate_proxy_list(script_dir):
    print("\n=== Generating Talkatone Proxy List ===")
    community_proxy_rules = []
    community_seen_keys = set()

    community_content = download_url(COMMUNITY_RULES_URL)
    if community_content:
        print("Parsing community Talkatone.sgmodule for PROXY rules...")
        for line in community_content.splitlines():
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith("#"):
                continue
            
            if "REJECT" not in line_stripped and "DIRECT" not in line_stripped:
                match = re.match(r'^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|IP-CIDR|IP-CIDR6),([^,\s]+)', line_stripped, re.IGNORECASE)
                if match:
                    rule_type = match.group(1).upper()
                    value = match.group(2).lower()
                    key = f"{rule_type},{value}"
                    community_seen_keys.add(key)
                    community_proxy_rules.append(key)
        print(f" - Found {len(community_proxy_rules)} PROXY rules in community source.")
    else:
        print("Warning: Failed to fetch community rule file.")

    user_rules_to_add = []
    user_seen = set()
    
    proxy_static_path = os.path.join(script_dir, "custom_static_talkatone_proxy.list")
    if os.path.exists(proxy_static_path):
        print(f"Reading local static proxy rules: {proxy_static_path}")
        with open(proxy_static_path, "r", encoding="utf-8") as f:
            user_content = f.read()
            
        for line in user_content.splitlines():
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith("#"):
                continue
                
            match = re.match(r'^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|IP-CIDR|IP-CIDR6),([^,\s]+)', line_stripped, re.IGNORECASE)
            if match:
                rule_type = match.group(1).upper()
                value = match.group(2).lower()
                key = f"{rule_type},{value}"
                
                if key not in community_seen_keys:
                    if key not in user_seen:
                        user_seen.add(key)
                        user_rules_to_add.append(key)
    else:
        print(f"Warning: {proxy_static_path} not found!")

    list_rules = []
    list_rules.append("# === 1. User Customized & Remapped Rules ===")
    list_rules.extend(user_rules_to_add)
    
    list_rules.append("\n# === 2. Community High-frequency Proxy Rules ===")
    for rule in community_proxy_rules:
        if rule not in user_seen:
            list_rules.append(rule)
            
    import datetime
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    beijing_time_str = beijing_now.strftime('%Y-%m-%d %H:%M:%S')

    output_path = os.path.join(script_dir, "talkatone_proxy.list")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# 自动更新时间: {beijing_time_str}\n\n")
        for rule in list_rules:
            f.write(rule + "\n")
            
    print(f"Successfully generated Talkatone Proxy list at: {output_path}")

def generate_adblock_list(script_dir):
    print("\n=== Generating Talkatone AdBlock List ===")
    adblock_rules = []
    seen = set()

    community_content = download_url(COMMUNITY_RULES_URL)
    if community_content:
        print("Parsing community Talkatone.sgmodule for adblock rules...")
        added_count = 0
        for line in community_content.splitlines():
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith("#"):
                continue
            
            if ",REJECT" in line_stripped:
                match = re.match(r'^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|IP-CIDR|IP-CIDR6),([^,\s]+)', line_stripped, re.IGNORECASE)
                if match:
                    rule_type = match.group(1).upper()
                    value = match.group(2).lower()
                    
                    if rule_type in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"):
                        if is_whitelisted(value):
                            continue
                            
                    norm = f"{rule_type},{value}"
                    if norm not in seen:
                        seen.add(norm)
                        adblock_rules.append(norm)
                        added_count += 1
        print(f" - Parsed and added {added_count} adblock rules from community source.")

    adblock_static_path = os.path.join(script_dir, "custom_static_talkatone_adblock.list")
    if os.path.exists(adblock_static_path):
        print(f"Reading local static adblock rules: {adblock_static_path}")
        with open(adblock_static_path, "r", encoding="utf-8") as f:
            adblock_content = f.read()
            
        added_count = 0
        for line in adblock_content.splitlines():
            line_stripped = line.strip()
            if not line_stripped or line_stripped.startswith("#"):
                continue
                
            match = re.match(r'^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|IP-CIDR|IP-CIDR6),([^,\s]+)', line_stripped, re.IGNORECASE)
            if match:
                rule_type = match.group(1).upper()
                value = match.group(2).lower()
                
                if rule_type in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"):
                    if is_whitelisted(value):
                        continue
                        
                norm = f"{rule_type},{value}"
                if norm not in seen:
                    seen.add(norm)
                    adblock_rules.append(norm)
                    added_count += 1
        print(f" - Parsed and added {added_count} custom static adblock rules.")
    else:
        print(f"Warning: {adblock_static_path} not found!")

    for alliance, url in AD_SOURCES.items():
        content = download_url(url)
        if not content:
            print(f"Warning: Failed to fetch {alliance} rules")
            continue
            
        parsed = parse_clash_yaml(content)
        added_count = 0
        for rule_type, value in parsed:
            if rule_type in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"):
                if is_whitelisted(value):
                    continue
            
            norm = f"{rule_type},{value}"
            if norm not in seen:
                seen.add(norm)
                adblock_rules.append(norm)
                added_count += 1
        print(f" - Parsed {len(parsed)} rules from {alliance}, added {added_count} clean rules.")

    import datetime
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    beijing_time_str = beijing_now.strftime('%Y-%m-%d %H:%M:%S')

    output_path = os.path.join(script_dir, "talkatone_adblock.list")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# 自动更新时间: {beijing_time_str}\n\n")
        f.write("# === Talkatone AdBlock Rules ===\n")
        for rule in adblock_rules:
            f.write(rule + "\n")
            
    print(f"Successfully generated Talkatone AdBlock list at: {output_path}")

def main():
    generate_proxy_list(BASE_DIR)
    generate_adblock_list(BASE_DIR)

if __name__ == "__main__":
    main()
