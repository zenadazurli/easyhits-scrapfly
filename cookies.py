from scrapfly import ScrapflyClient, ScrapeConfig
import json
import os

# Configurazione
API_KEY = os.environ.get("SCRAPFLY_API_KEY", "scp-live-22b86f07211a42ae977a933e7c525485")
EMAIL = "sandrominori50+ulugarecexisa@gmail.com"
PASSWORD = "DDnmVV45!!"

# JavaScript scenario per gestire il login e il redirect
javascript_scenario = """
    // Attende che il campo username sia presente
    await page.waitForSelector('input[name="username"]', { timeout: 30000 });
    
    // Compila il form
    await page.type('input[name="username"]', 'sandrominori50+ulugarecexisa@gmail.com');
    await page.type('input[name="password"]', 'DDnmVV45!!');
    
    // Tenta il login
    await page.click('button.btn_green');
    
    // Aspetta che la pagina di warning (se presente) sia caricata
    await page.waitForTimeout(5000);
    
    // Se l'URL contiene 'warning', fai un secondo tentativo di click
    if (page.url().includes('warning')) {
        await page.click('button.btn_green');
    }
    
    // Aspetta che la navigazione sia completata e che l'URL finale sia quello della dashboard
    await page.waitForFunction(
        () => window.location.href.includes('/account/'),
        { timeout: 60000, polling: 1000 }
    );
"""

print("🚀 Avvio login con Scrapfly...")

try:
    client = ScrapflyClient(key=API_KEY)
    
    result = client.scrape(ScrapeConfig(
        url="https://www.easyhits4u.com/logon/",
        render_js=True,
        asp=True,
        proxy_pool="public_residential_pool",
        country="it",
        javascript_scenario=javascript_scenario,
        session="easyhits_final_js",
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