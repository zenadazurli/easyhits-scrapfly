from scrapfly import ScrapflyClient, ScrapeConfig
import json
import os

API_KEY = os.environ.get("SCRAPFLY_API_KEY", "scp-live-dc9220813c2944c49af55e5857eb2992")
EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"

# usa js_scenario, NON javascript_scenario
js_scenario = [
    {"wait": 3000},
    {"fill": {"selector": "input[name='username']", "value": EMAIL}},
    {"fill": {"selector": "input[name='password']", "value": PASSWORD}},
    {"click": {"selector": "button.btn_green"}},
    {"wait": 5000},
    {"click": {"selector": "button.btn_green"}},
    {"wait_for_navigation": {"timeout": 10000}}  # max 10 secondi
]

print("🚀 Avvio login con Scrapfly...")

try:
    client = ScrapflyClient(key=API_KEY)
    
    result = client.scrape(ScrapeConfig(
        url="https://www.easyhits4u.com/logon/",
        render_js=True,
        asp=True,
        proxy_pool="public_residential_pool",
        country="it",
        js_scenario=js_scenario,          # <-- PARAMETRO CORRETTO
        session="easyhits_final",
        rendering_wait=5000,
    ))
    
    print(f"URL finale: {result.scrape_result['url']}")
    
    cookies = result.scrape_result.get('cookies', [])
    cookie_dict = {c['name']: c['value'] for c in cookies}
    
    sesids = cookie_dict.get('sesids')
    user_id = cookie_dict.get('user_id')
    
    if sesids and user_id:
        print(f"\n🎉 SUCCESSO!")
        print(f"   sesids = {sesids}")
        print(f"   user_id = {user_id}")
        
        with open("cookies.json", "w") as f:
            json.dump(cookie_dict, f, indent=2)
        print("\n✅ Cookie salvati in cookies.json")
    else:
        print(f"\n❌ Cookie non trovati")
        print(f"Cookie ricevuti: {list(cookie_dict.keys())}")
        
except Exception as e:
    print(f"❌ Errore: {e}")
