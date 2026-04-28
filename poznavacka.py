import pygame
import random
import os

# Inicializace
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poznávačka Vzdušnicovců - Flashcards")

# Moderní fonty (podporující českou diakritiku)
font_title = pygame.font.SysFont("segoeui", 42, bold=True)
font_main = pygame.font.SysFont("segoeui", 36, bold=True)
font_info = pygame.font.SysFont("segoeui", 26)
font_hint = pygame.font.SysFont("segoeui", 20, italic=True)

# Barvy (Dark Mode paleta)
BG_COLOR = (30, 33, 36)          # Tmavé pozadí
CARD_COLOR = (44, 47, 51)        # Barva kartičky
TEXT_LIGHT = (255, 255, 255)     # Bílý text
TEXT_ACCENT = (114, 137, 218)    # Modrofialové zvýraznění
TEXT_CORRECT = (67, 181, 129)    # Zelená pro správnou odpověď
SHADOW = (15, 15, 15)            # Stín

# Biologická databáze vzdušnicovců
# Všichni mají Kmen: Členovci (Arthropoda), Podkmen: Vzdušnicovci (Tracheata)
biology_data = {
    # Stonožkovci (bez proměny)
    "mnohonožka": {"trida": "Mnohonožky", "rad": "Mnohonožky", "promena": "Vývoj přímý"},
    "stonožka": {"trida": "Stonožky", "rad": "Stonožky", "promena": "Vývoj přímý"},
    
    # Hmyz - Bezkřídlí
    "rybenka": {"trida": "Hmyz", "rad": "Rybenky", "promena": "Bez proměny (Ametabolie)"},
    
    # Hmyz - Proměna nedokonalá (Hemimetabolia)
    "jepice": {"trida": "Hmyz", "rad": "Jepice", "promena": "Nedokonalá"},
    "vážka": {"trida": "Hmyz", "rad": "Vážky", "promena": "Nedokonalá"},
    "motýlice": {"trida": "Hmyz", "rad": "Vážky", "promena": "Nedokonalá"},
    "šidélko": {"trida": "Hmyz", "rad": "Vážky", "promena": "Nedokonalá"},
    "šváb": {"trida": "Hmyz", "rad": "Švábi", "promena": "Nedokonalá"},
    "termit": {"trida": "Hmyz", "rad": "Švábi (dříve Termiti)", "promena": "Nedokonalá"},
    "škvor": {"trida": "Hmyz", "rad": "Škvoři", "promena": "Nedokonalá"},
    "kudlanka": {"trida": "Hmyz", "rad": "Kudlanky", "promena": "Nedokonalá"},
    "kobylka": {"trida": "Hmyz", "rad": "Rovnokřídlí", "promena": "Nedokonalá"},
    "cvrček": {"trida": "Hmyz", "rad": "Rovnokřídlí", "promena": "Nedokonalá"},
    "saranče": {"trida": "Hmyz", "rad": "Rovnokřídlí", "promena": "Nedokonalá"},
    "krtonožka": {"trida": "Hmyz", "rad": "Rovnokřídlí", "promena": "Nedokonalá"},
    "veš": {"trida": "Hmyz", "rad": "Vši", "promena": "Nedokonalá"},
    "cikáda": {"trida": "Hmyz", "rad": "Polokřídlí (Křísi)", "promena": "Nedokonalá"},
    "pěnodějka": {"trida": "Hmyz", "rad": "Polokřídlí (Křísi)", "promena": "Nedokonalá"},
    "mšice": {"trida": "Hmyz", "rad": "Polokřídlí (Mšice)", "promena": "Nedokonalá"},
    "ruměnice": {"trida": "Hmyz", "rad": "Polokřídlí (Ploštice)", "promena": "Nedokonalá"},
    "kněžice": {"trida": "Hmyz", "rad": "Polokřídlí (Ploštice)", "promena": "Nedokonalá"},
    "štěnice": {"trida": "Hmyz", "rad": "Polokřídlí (Ploštice)", "promena": "Nedokonalá"},
    "vodoměrka": {"trida": "Hmyz", "rad": "Polokřídlí (Ploštice)", "promena": "Nedokonalá"},
    "bruslařka": {"trida": "Hmyz", "rad": "Polokřídlí (Ploštice)", "promena": "Nedokonalá"},
    "splešťule": {"trida": "Hmyz", "rad": "Polokřídlí (Ploštice)", "promena": "Nedokonalá"},

    # Hmyz - Proměna dokonalá (Holometabolia)
    "dlouhošíjka": {"trida": "Hmyz", "rad": "Dlouhošíjky", "promena": "Dokonalá"},
    "zlatoočka": {"trida": "Hmyz", "rad": "Síťokřídlí", "promena": "Dokonalá"},
    "mravkolev": {"trida": "Hmyz", "rad": "Síťokřídlí", "promena": "Dokonalá"},
    "lumek": {"trida": "Hmyz", "rad": "Blanokřídlí", "promena": "Dokonalá"},
    "včela": {"trida": "Hmyz", "rad": "Blanokřídlí", "promena": "Dokonalá"},
    "vosa": {"trida": "Hmyz", "rad": "Blanokřídlí", "promena": "Dokonalá"},
    "čmelák": {"trida": "Hmyz", "rad": "Blanokřídlí", "promena": "Dokonalá"},
    "mravenec": {"trida": "Hmyz", "rad": "Blanokřídlí", "promena": "Dokonalá"},
    "blecha": {"trida": "Hmyz", "rad": "Blechy", "promena": "Dokonalá"},
    "chrostík": {"trida": "Hmyz", "rad": "Chrostíci", "promena": "Dokonalá"},
    
    # Brouci
    **{b: {"trida": "Hmyz", "rad": "Brouci", "promena": "Dokonalá"} for b in 
       ["střevlík", "svižník", "kovařík", "hrobařík", "potápník", "roháč", "klikoroh", "chrobák", 
        "zlatohlávek", "nosorožík kapucínek", "chroust", "slunéčko", "páteříček", "mandelinka", 
        "tesařík", "lýkožrout smrkový", "rákosníček"]},
    
    # Dvoukřídlí
    **{d: {"trida": "Hmyz", "rad": "Dvoukřídlí", "promena": "Dokonalá"} for d in 
       ["tiplice", "komár", "pakomár", "moucha", "pestřenka", "octomilka"]},
    
    # Motýli
    **{m: {"trida": "Hmyz", "rad": "Motýli", "promena": "Dokonalá"} for m in 
       ["babočka", "otakárek", "lišaj", "přástevník", "dlouhozobka", "mol", "bekyně mniška", 
        "klíněnka", "martináč"]}
}

insect_list = list(biology_data.keys())

# Pomocná funkce pro vykreslení obdélníku se zaoblenými rohy
def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

class QuizApp:
    def __init__(self):
        self.current_insect = ""
        self.show_answer = False
        self.image = None
        self.new_question()

    def new_question(self):
        self.current_insect = random.choice(insect_list)
        self.show_answer = False
        
        # Načtení obrázku s podporou více formátů
        img_path_jpg = f"images/{self.current_insect}.jpg"
        img_path_png = f"images/{self.current_insect}.png"
        
        path_to_load = img_path_jpg if os.path.exists(img_path_jpg) else (img_path_png if os.path.exists(img_path_png) else None)

        if path_to_load:
            loaded_img = pygame.image.load(path_to_load).convert_alpha()
            # Zachování poměru stran
            img_w, img_h = loaded_img.get_size()
            max_w, max_h = 500, 350
            scale = min(max_w/img_w, max_h/img_h)
            new_w, new_h = int(img_w * scale), int(img_h * scale)
            self.image = pygame.transform.smoothscale(loaded_img, (new_w, new_h))
        else:
            self.image = None

    def draw(self):
        screen.fill(BG_COLOR)
        
        # Nadpis
        title_surf = font_title.render("Kdo je na obrázku?", True, TEXT_LIGHT)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 20))

        # Karta pro obrázek
        card_rect = pygame.Rect(WIDTH//2 - 300, 90, 600, 400)
        draw_rounded_rect(screen, SHADOW, card_rect.move(5, 5), 15) # Stín
        draw_rounded_rect(screen, CARD_COLOR, card_rect, 15)

        # Vykreslení obrázku
        if self.image:
            img_x = WIDTH//2 - self.image.get_width()//2
            img_y = 90 + (400//2 - self.image.get_height()//2)
            screen.blit(self.image, (img_x, img_y))
        else:
            txt = font_info.render(f"Obrázek chybí: {self.current_insect}", True, (200, 50, 50))
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 270))

        # Spodní informační sekce
        info_rect = pygame.Rect(WIDTH//2 - 300, 510, 600, 160)
        draw_rounded_rect(screen, SHADOW, info_rect.move(5, 5), 15)
        draw_rounded_rect(screen, CARD_COLOR, info_rect, 15)

        if self.show_answer:
            # Zobrazení jména
            name_surf = font_main.render(self.current_insect.upper(), True, TEXT_CORRECT)
            screen.blit(name_surf, (WIDTH//2 - name_surf.get_width()//2, 520))

            # Zobrazení biologie
            data = biology_data.get(self.current_insect, {"trida": "?", "rad": "?", "promena": "?"})
            
            # Formátovaný text
            kmen_txt = font_info.render(f"Kmen: Členovci | Podkmen: Vzdušnicovci", True, TEXT_LIGHT)
            trida_rad_txt = font_info.render(f"Třída: {data['trida']} | Řád: {data['rad']}", True, TEXT_ACCENT)
            promena_txt = font_info.render(f"Proměna: {data['promena']}", True, TEXT_LIGHT)

            screen.blit(kmen_txt, (WIDTH//2 - kmen_txt.get_width()//2, 570))
            screen.blit(trida_rad_txt, (WIDTH//2 - trida_rad_txt.get_width()//2, 600))
            screen.blit(promena_txt, (WIDTH//2 - promena_txt.get_width()//2, 630))

        else:
            # Výzva k akci před odhalením
            hint_surf = font_main.render("Přemýšlej...", True, TEXT_LIGHT)
            screen.blit(hint_surf, (WIDTH//2 - hint_surf.get_width()//2, 560))
            
            subhint_surf = font_hint.render("Stiskni ENTER nebo MEZERNÍK pro zobrazení odpovědi", True, TEXT_ACCENT)
            screen.blit(subhint_surf, (WIDTH//2 - subhint_surf.get_width()//2, 610))

        pygame.display.flip()

def main():
    app = QuizApp()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Reakce na Enter nebo Mezerník
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if not app.show_answer:
                        app.show_answer = True
                    else:
                        app.new_question()

        app.draw()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
