import urllib.request
import re
import sys
import os
import ssl
import datetime

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Target AI sources from BlackMatrix7
AI_SOURCES = {
    "OpenAI": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OpenAI/OpenAI.yaml",
    "Claude": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Claude/Claude.yaml",
    "Gemini_List": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Gemini/Gemini.list",
    "Gemini_Yaml": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Gemini/Gemini.yaml",
    "Copilot": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Copilot/Copilot.yaml"
}

POLLUTION_DOMAINS = [
    "google.com", "microsoft.com", "bing.com", "live.com", "x.com", "twitter.com", "apple.com"
]

ALLOWED_SUBDOMAINS = [
    "gemini.google.com", "generativelanguage.googleapis.com", "notebooklm.google.com", "alkalimira-pa.clients6.google.com",
    "copilot.microsoft.com", "sydney.bing.com", "edgeservices.bing.com",
    "guzzoni.apple.com", "smoot.apple.com", "gspe1-ssl.ls.apple.com",
    "generativeai.google", "deepmind.google", "deepmind.com", "ai.google.dev",
    "makersuite.google.com", "alkalimakersuite-pa.clients6.google.com", "proactivebackend-pa.googleapis.com",
    "bard.google.com"
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

def is_polluted(domain):
    domain_lower = domain.lower().strip('.')
    for allowed in ALLOWED_SUBDOMAINS:
        if domain_lower == allowed or domain_lower.endswith('.' + allowed):
            return False
    for polluted in POLLUTION_DOMAINS:
        if domain_lower == polluted or domain_lower.endswith('.' + polluted):
            return True
    return False

def parse_clash_rules(content):
    rules = []
    lines = content.splitlines()
    payload_section = False
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("#"):
            continue
            
        if line_stripped.startswith("payload:"):
            payload_section = True
            continue
            
        # Parse YAML item (- TYPE,VALUE) or plain list item (TYPE,VALUE)
        match = re.search(r'^(?:-\s+)?([^,]+),([^,]+)(?:,.+)?', line_stripped)
        if match:
            rule_type = match.group(1).strip().upper()
            value = match.group(2).strip().lower()
            
            if rule_type in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"):
                if is_polluted(value):
                    continue
                    
            formatted_rule = f"{rule_type},{value}"
            rules.append(formatted_rule)
                
    return rules

def main():
    compiled_rules = []
    
    for service, url in AI_SOURCES.items():
        content = download_url(url)
        if not content:
            print(f"Warning: Failed to fetch rules for {service}")
            continue
            
        print(f"Parsing Clash rules for {service}...")
        parsed = parse_clash_rules(content)
        compiled_rules.extend(parsed)
        print(f" - Found {len(parsed)} clean rules for {service}")
        
    final_rules = []
    seen = set()
    
    custom_rules_path = os.path.join(BASE_DIR, "custom_static_ai.list")
    if os.path.exists(custom_rules_path):
        print(f"Reading local static custom rules: {custom_rules_path}")
        with open(custom_rules_path, "r", encoding="utf-8") as f:
            custom_content = f.read()
        for line in custom_content.splitlines():
            line_stripped = line.strip()
            if line_stripped:
                if not line_stripped.startswith("#"):
                    norm = line_stripped.replace(" ", "").lower()
                    if norm not in seen:
                        seen.add(norm)
                        final_rules.append(line_stripped)
                else:
                    final_rules.append(line_stripped)
    else:
        print(f"Warning: {custom_rules_path} not found!")
                
    final_rules.append("\n# === Compiled AI & Subdomain Rules ===")
    for rule in compiled_rules:
        norm = rule.replace(" ", "").lower()
        if norm not in seen:
            seen.add(norm)
            final_rules.append(rule)
            
    output_path = os.path.join(BASE_DIR, "ai.list")
    
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    beijing_time_str = beijing_now.strftime('%Y-%m-%d %H:%M:%S')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# 自动更新时间: {beijing_time_str}\n\n")
        for rule in final_rules:
            f.write(rule + "\n")
            
    print(f"\nSuccessfully generated AI Clash list with {len(seen)} unique rules at: {output_path}")

if __name__ == "__main__":
    main()
