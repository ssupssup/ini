import urllib.request
import os
import ssl
import datetime

ssl._create_default_https_context = ssl._create_unverified_context

SOURCES = {
    "gfw": "https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/gfw.txt",
    "direct": "https://raw.githubusercontent.com/Loyalsoldier/surge-rules/release/direct.txt"
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

def parse_domains(content):
    rules = []
    lines = content.splitlines()
    for line in lines:
        line_stripped = line.strip()
        # Skip empty lines or comments
        if not line_stripped or line_stripped.startswith("#") or line_stripped.startswith("//"):
            continue
        
        # Format domain as DOMAIN-SUFFIX
        domain = line_stripped.lower()
        if domain.startswith("."):
            domain = domain[1:]
        elif domain.startswith("+."):
            domain = domain[2:]
            
        rules.append(f"DOMAIN-SUFFIX,{domain}")
    return rules

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Calculate Beijing time
    utc_now = datetime.datetime.utcnow()
    beijing_now = utc_now + datetime.timedelta(hours=8)
    beijing_time_str = beijing_now.strftime('%Y-%m-%d %H:%M:%S')
    
    for name, url in SOURCES.items():
        content = download_url(url)
        if not content:
            print(f"Error: Failed to fetch rules for {name}")
            continue
            
        print(f"Parsing rules for {name}...")
        rules = parse_domains(content)
        
        # Output list path
        output_path = os.path.join(script_dir, f"{name}.list")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(f"# 自动更新时间: {beijing_time_str}\n")
            f.write(f"# 来源: {url}\n\n")
            for rule in rules:
                f.write(rule + "\n")
                
        print(f"Successfully generated {name}.list with {len(rules)} rules at: {output_path}")

if __name__ == "__main__":
    main()
