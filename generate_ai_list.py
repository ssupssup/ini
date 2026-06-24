import urllib.request
import re
import sys
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Target AI sources from BlackMatrix7
AI_SOURCES = {
    "OpenAI": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OpenAI/OpenAI.yaml",
    "Claude": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Claude/Claude.yaml",
    "Gemini": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Gemini/Gemini.yaml",
    "Copilot": "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Copilot/Copilot.yaml"
}

# Domains that are too broad and will pollute everyday direct browsing
# We strip/bypass these top-level domains unless they match the allow-subdomains list below
POLLUTION_DOMAINS = [
    "google.com", "microsoft.com", "bing.com", "live.com", "x.com", "twitter.com", "apple.com"
]

# Specifically allowed subdomains/keywords for the above parent domains
ALLOWED_SUBDOMAINS = [
    # Gemini / Google AI
    "gemini.google.com", "generativelanguage.googleapis.com", "notebooklm.google.com", "alkalimira-pa.clients6.google.com",
    # Copilot / Bing AI
    "copilot.microsoft.com", "sydney.bing.com", "edgeservices.bing.com",
    # Apple Intelligence
    "guzzoni.apple.com", "smoot.apple.com", "gspe1-ssl.ls.apple.com"
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
    
    # 1. If it matches one of our explicitly allowed subdomains, it is NOT polluted
    for allowed in ALLOWED_SUBDOMAINS:
        if domain_lower == allowed or domain_lower.endswith('.' + allowed):
            return False
            
    # 2. Check if it matches one of the broad polluted domains
    for polluted in POLLUTION_DOMAINS:
        if domain_lower == polluted or domain_lower.endswith('.' + polluted):
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
                
                # Check for broad pollution domains
                if rule_type in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD"):
                    if is_polluted(value):
                        continue
                
                if rule_type in ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "IP-CIDR", "IP-CIDR6", "GEOIP"):
                    rules.append(f"{rule_type},{value}")
                    
    return rules

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    compiled_rules = []
    
    # Process BM7 sources
    for service, url in AI_SOURCES.items():
        content = download_url(url)
        if not content:
            print(f"Warning: Failed to fetch rules for {service}")
            continue
            
        print(f"Parsing Clash rules for {service}...")
        parsed = parse_clash_yaml(content)
        compiled_rules.extend(parsed)
        print(f" - Found {len(parsed)} clean rules for {service}")
        
    # Deduplicate rules, ensuring custom rules are at the top and preserved
    final_rules = []
    seen = set()
    
    # 1. Add user custom rules first
    custom_rules_path = os.path.join(script_dir, "custom_static_ai.list")
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
                
    # 2. Add compiled rules
    final_rules.append("\n# === Compiled AI & Subdomain Rules ===")
    for rule in compiled_rules:
        norm = rule.replace(" ", "").lower()
        if norm not in seen:
            seen.add(norm)
            final_rules.append(rule)
            
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "ai.list")
    
    with open(output_path, "w", encoding="utf-8") as f:
        for rule in final_rules:
            f.write(rule + "\n")
            
    print(f"\nSuccessfully generated AI Clash list with {len(seen)} unique rules at: {output_path}")

if __name__ == "__main__":
    main()
