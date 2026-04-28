from icrawler.builtin import BingImageCrawler
import os
import shutil

insects = [
    "mnohonožka", "stonožka", "rybenka", "jepice", "vážka", "motýlice", "šidélko",
    "šváb", "škvor", "kudlanka", "kobylka", "cvrček", "saranče", "krtonožka",
    "veš", "cikáda", "pěnodějka", "mšice", "termit", "ruměnice", "kněžice",
    "štěnice", "vodoměrka", "bruslařka", "splešťule", "dlouhošíjka", "zlatoočka",
    "mravkolev", "lumek", "včela", "vosa", "čmelák", "mravenec", "střevlík",
    "svižník", "kovařík", "hrobařík", "potápník", "roháč", "klikoroh", "chrobák",
    "zlatohlávek", "nosorožík kapucínek", "chroust", "slunéčko", "páteříček",
    "mandelinka", "tesařík", "lýkožrout smrkový", "tiplice", "komár", "pakomár",
    "moucha", "pestřenka", "octomilka", "blecha", "chrostík", "babočka",
    "otakárek", "lišaj", "přástevník", "dlouhozobka", "mol", "bekyně mniška",
    "klíněnka", "martináč", "rákosníček"
]

target_dir = "images"
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

print("Startuji stahování přes Bing (icrawler)...")

for insect in insects:
    # Vytvoříme dočasnou složku pro jeden obrázek
    temp_dir = "temp_download"
    
    # Crawler se pokusí najít 1 obrázek
    # Přidáváme "hmyz" pro lepší přesnost (u "mol" nebo "vosa" je to nutnost)
    bing_crawler = BingImageCrawler(storage={'root_dir': temp_dir})
    bing_crawler.crawl(keyword=f"hmyz {insect}", max_num=1)

    # Přesun staženého souboru do 'images' s finálním názvem
    if os.path.exists(temp_dir):
        files = os.listdir(temp_dir)
        if files:
            file_ext = os.path.splitext(files[0])[1]
            source_path = os.path.join(temp_dir, files[0])
            dest_path = os.path.join(target_dir, f"{insect}.jpg") # Ukládáme jako .jpg pro Pygame
            
            # Přesuneme a přejmenujeme (shutil.move umí přepsat, pokud už existuje)
            shutil.move(source_path, dest_path)
            print(f"Hotovo: {insect}")
        
        # Vyčistit temp složku
        shutil.rmtree(temp_dir)

print("\nHotovo! Pokud nějaký obrázek chybí, Bing ho nenašel nebo byl blokován.")
