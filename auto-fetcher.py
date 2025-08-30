import requests, time, os
from datetime import datetime
from zoneinfo import ZoneInfo

# Configurations
URLS = {
    # Format is like this: 
    # "file name to show up in the webhook and in the output_folder": "http(s)://url_to_your_data_api.io",
    "Google": "https://google.com", # Remove this, its only for testing purposes
    "PlayedUsers.json": "http://xxx.xxx.xxx.xx:7182/?apiKey=Vo4djssEVIwCkSDPyxt2EWdTnGr50M7z&data=playedusers.json",
    "RegisteredMembers.json": "http://xxx.xxx.xxx.xx:7182/?apiKey=Vo4djssEVIwCkSDPyxt2EWdTnGr50M7z&data=registeredmembers.json"
}
HTTP_PROXIES = [
    "http://yvxj9uh2tr7h2q6-country-any:InstantName123Proxyyy@proxy.instantname.io:7331",
]
HTTPS_PROXIES = [
    "https://USER:PASSWORD@PROXY_IP:PORT",
    "https://USER:PASSWORD@PROXY_IP:PORT"
]
USE_PROXY_TYPE = "http"   # "http", "https", or "none"
SAFETY_MODE = False        # Force proxies? (Won't work without working proxies)
OUTPUT_FOLDER = "./"
WAITING_TIME = 3 * 60 * 60 # Default amount is set to 3 hours
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1412222222222228/nxxxxxxxxxxxxxxILLfR81xxxxxxxxxxxxB" # Your Discord webhook ofc
CURRENT_TIME = datetime.now(ZoneInfo("Europe/Amsterdam")) # Your timezone
footer_text = CURRENT_TIME.strftime("%H:%M")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
def send_discord_message(title, description, color=0x3498db):
    footer_text = CURRENT_TIME.strftime("%H:%M")
    embed = {
        "title": title,
        "description": description,
        "color": color,
        "footer": {"text": f"Executed at: {footer_text}"}
    }
    payload = {"embeds": [embed]}
    try:
        r = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"[Discord] Failed to send webhook: {e}")

def get_proxy_list():
    if USE_PROXY_TYPE == "http":
        return HTTP_PROXIES
    elif USE_PROXY_TYPE == "https":
        return HTTPS_PROXIES
    return []

def fetch_page(name, url):
    proxies_list = get_proxy_list()
    if SAFETY_MODE and not proxies_list:
        msg = f"`{name}` • SAFETY_MODE is enabled but no proxies are available!"
        print(f"• {name} - SAFETY_MODE is enabled but no proxies are available!")
        send_discord_message("⚠ Proxy Error", msg, color=0xe67e22)
        return

    proxy_failed = False
    for proxy in (proxies_list if proxies_list else [None]):
        proxies = {"http": proxy, "https": proxy} if proxy else None
        try:
            if proxies:
                print(f"• {name} - Trying proxy {proxy}")
            else:
                print(f"• {name} - No proxy used")

            response = requests.get(url, proxies=proxies, timeout=30)
            response.raise_for_status()

            filename = os.path.join(OUTPUT_FOLDER, name)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)

            size_kb = len(response.text) / 1024
            msg = f"`{name}` • Data saved successfully ({size_kb:.2f} KB)."
            print(f"• {name} - Data saved successfully ({size_kb:.2f} KB).")
            send_discord_message("✅ List saved", msg, color=0x2ecc71)
            return
        except requests.exceptions.ProxyError as e:
            proxy_failed = True
            msg = f"`{name}` • Proxy connection failed: ```{e}```"
            print(f"• {name} - Proxy connection failed: {e}")
            send_discord_message("❌ Proxy error", msg, color=0xe74c3c)
        except requests.exceptions.ConnectTimeout as e:
            proxy_failed = True
            msg = f"`{name}` • Proxy timeout: ```{e}```"
            print(f"• {name} - Proxy timeout: {e}")
            send_discord_message("⏳ Proxy timeout", msg, color=0xf1c40f)
        except requests.exceptions.RequestException as e:
            msg = f"`{name}` • Request failed: ```{e}```"
            print(f"• {name} - Request failed: {e}")
            send_discord_message("❌ Request error", msg, color=0xe67e22)
            return

    if SAFETY_MODE and proxy_failed:
        msg = f"`{name}` • All proxies failed, skipping due to SAFETY_MODE."
        print(f"• {name} - All proxies failed, skipping due to SAFETY_MODE.")
        send_discord_message("⛔ Proxy failed", msg, color=0xc0392b)

def main():
    while True:
        for name, url in URLS.items():
            fetch_page(name, url)
        print(f"Sleeping for {WAITING_TIME/3600:.2f} hours...")
        time.sleep(WAITING_TIME)

if __name__ == "__main__":
    main()
