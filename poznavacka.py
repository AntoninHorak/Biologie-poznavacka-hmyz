import pygame
import random
import os

# Inicializace
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poznávačka Vzdušnicovců - Systematické drcení")

# Fonty
font_title = pygame.font.SysFont("segoeui", 42, bold=True)
font_main = pygame.font.SysFont("segoeui", 36, bold=True)
font_info = pygame.font.SysFont("segoeui", 26)
font_hint = pygame.font.SysFont("segoeui", 20, italic=True)
font_counter = pygame.font.SysFont("consolas", 24, bold=True) # Font pro počítadlo

# Barvy
BG_COLOR = (30, 33, 36)
CARD_COLOR = (44, 47, 51)
TEXT_LIGHT = (255, 255, 255)
TEXT_ACCENT = (114, 137, 218)
TEXT_CORRECT = (67, 181, 129)
SHADOW = (15, 15, 15)

# Biologická databáze (stejná jako minule)
biology_data = {
    "mnohonožka": {"trida": "Mnohonožky", "rad": "Mnohonožky", "promena": "Vývoj přímý"},
    "stonožka": {"trida": "Stonožky", "rad": "Stonožky", "promena": "Vývoj přímý"},
    "rybenka": {"trida": "Hmyz", "rad": "Rybenky", "promena": "Bez proměny (Ametabolie)"},
    "jepice": {"trida": "Hmyz", "rad": "Jepice", "promena": "Nedokonalá"},
    "vážka": {"trida": "Hmyz", "rad": "Vážky", "promena": "Nedokonalá"},
    "motýlice": {"trida": "Hmyz", "rad": "Vážky", "promena": "Nedokonalá"},
    "šidélko": {"trida": "Hmyz", "rad": "Vážky", "promena": "Nedokonalá"},
    "šváb": {"trida": "Hmyz", "rad": "Švábi", "promena": "Nedokonalá"},
    "termit": {"trida": "Hmyz", "rad": "Švábi", "promena": "Nedokonalá"},
    "škvor": {"trida": "Hmyz", "rad": "Škvoři", "promena": "Nedokonalá"},
    "kudlanka": {"trida": "Hmyz", "rad": "Kudlanky", "promena": "Nedokonalá"},
    "kobylka": {"trida": "Hmyz", "rad": "Rovnokřídlí", "promena": "Nedokonalá"},
    "cvrček": {"trida": "Hmyz", "rad": "Rovnokřídlí", "promena": "Nedokonalá"},
    "saranče": {"trida": "Hmyz", "rad": "Rovnokřídlí", "promena": "Nedokonalá"},
    "krtonožka": {"trida": "Hmyz", "rad": "Rovnokřídlí", "promena": "Nedokonalá"},
    "veš": {"trida": "Hmyz", "rad": "Vši", "promena": "Nedokonalá"},
    "cikáda": {"trida": "Hmyz", "rad": "Polokřídlí", "promena": "Nedokonalá"},
    "pěnodějka": {"trida": "Hmyz", "rad": "Polokřídlí", "promena": "Nedokonalá"},
    "mšice": {"trida": "Hmyz", "rad": "Polokřídlí", "promena": "Nedokonalá"},
    "ruměnice": {"trida": "Hmyz", "rad": "Polokřídlí", "promena": "Nedokonalá"},
    "kněžice": {"trida": "Hmyz", "rad": "Polokřídlí", "promena": "Nedokonalá"},
    "štěnice": {"trida": "Hmyz", "rad": "Polokřídlí", "promena": "Nedokonalá"},
    "vodoměrka": {"trida": "Hmyz", "rad": "Polokřídlí", "promena": "Nedokonalá"},
    "bruslařka": {"trida": "Hmyz", "rad": "Polokřídlí", "promena": "Nedokonalá"},
    "splešťule": {"trida": "Hmyz", "rad": "Polokřídlí", "promena": "Nedokonalá"},
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
    **{b: {"trida": "Hmyz", "rad": "Brouci", "promena": "Dokonalá"} for b in 
       ["střevlík", "svižník", "kovařík", "hrobařík", "potápník", "roháč", "klikoroh", "chrobák", 
        "zlatohlávek", "nosorožík kapucínek", "chroust", "slunéčko", "páteříček", "mandelinka", 
        "tesařík", "lýkožrout smrkový", "rákosníček"]},
    **{d: {"trida": "Hmyz", "rad": "Dvoukřídlí", "promena": "Dokonalá"} for d in 
       ["tiplice", "komár", "pakomár", "moucha", "pestřenka", "octomilka"]},
    **{m: {"trida": "Hmyz", "rad": "Motýli", "promena": "Dokonalá"} for m in 
       ["babočka", "otakárek", "lišaj", "přástevník", "dlouhozobka", "mol", "bekyně mniška", 
        "klíněnka", "martináč"]}
}

def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

class QuizApp:
    def __init__(self):
        # Příprava náhodného seznamu, kde se objeví každý právě jednou
        self.all_insects = list(biology_data.keys())
        random.shuffle(self.all_insects)
        
        self.current_index = 0
        self.total_count = len(self.all_insects)
        self.current_insect = ""
        self.show_answer = False
        self.image = None
        self.finished = False
        
        self.load_insect()

    def load_insect(self):
        if self.current_index < self.total_count:
            self.current_insect = self.all_insects[self.current_index]
            self.show_answer = False
            
            # Načítání obrázku
            img_path_jpg = f"images/{self.current_insect}.jpg"
            img_path_png = f"images/{self.current_insect}.png"
            path = img_path_jpg if os.path.exists(img_path_jpg) else (img_path_png if os.path.exists(img_path_png) else None)

            if path:
                loaded_img = pygame.image.load(path).convert_alpha()
                img_w, img_h = loaded_img.get_size()
                scale = min(500/img_w, 350/img_h)
                self.image = pygame.transform.smoothscale(loaded_img, (int(img_w*scale), int(img_h*scale)))
            else:
                self.image = None
        else:
            self.finished = True

    def draw(self):
        screen.fill(BG_COLOR)
        
        if self.finished:
            msg = font_title.render("Gratuluji! Prošel jsi všechno.", True, TEXT_CORRECT)
            hint = font_info.render("Stiskni ESC pro ukončení", True, TEXT_LIGHT)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 50))
            screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 20))
        else:
            # Počítadlo v rohu
            counter_str = f"{self.current_index + 1} / {self.total_count}"
            counter_surf = font_counter.render(counter_str, True, TEXT_ACCENT)
            screen.blit(counter_surf, (WIDTH - 120, 25))

            # Nadpis
            title_surf = font_title.render("Poznávačka", True, TEXT_LIGHT)
            screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 20))

            # Karta obrázku
            card_rect = pygame.Rect(WIDTH//2 - 300, 90, 600, 400)
            draw_rounded_rect(screen, SHADOW, card_rect.move(5, 5), 15)
            draw_rounded_rect(screen, CARD_COLOR, card_rect, 15)

            if self.image:
                screen.blit(self.image, (WIDTH//2 - self.image.get_width()//2, 90 + (400//2 - self.image.get_height()//2)))

            # Info panel
            info_rect = pygame.Rect(WIDTH//2 - 300, 510, 600, 160)
            draw_rounded_rect(screen, SHADOW, info_rect.move(5, 5), 15)
            draw_rounded_rect(screen, CARD_COLOR, info_rect, 15)

            if self.show_answer:
                name_surf = font_main.render(self.current_insect.upper(), True, TEXT_CORRECT)
                screen.blit(name_surf, (WIDTH//2 - name_surf.get_width()//2, 520))
                
                d = biology_data[self.current_insect]
                txt1 = font_info.render(f"Třída: {d['trida']} | Řád: {d['rad']}", True, TEXT_ACCENT)
                txt2 = font_info.render(f"Proměna: {d['promena']}", True, TEXT_LIGHT)
                screen.blit(txt1, (WIDTH//2 - txt1.get_width()//2, 580))
                screen.blit(txt2, (WIDTH//2 - txt2.get_width()//2, 620))
            else:
                hint_surf = font_main.render("???", True, TEXT_LIGHT)
                screen.blit(hint_surf, (WIDTH//2 - hint_surf.get_width()//2, 560))
                sub_surf = font_hint.render("ENTER pro odhalení", True, TEXT_ACCENT)
                screen.blit(sub_surf, (WIDTH//2 - sub_surf.get_width()//2, 610))

        pygame.display.flip()

def main():
    app = QuizApp()
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key in [pygame.K_RETURN, pygame.K_SPACE] and not app.finished:
                    if not app.show_answer:
                        app.show_answer = True
                    else:
                        app.current_index += 1
                        app.load_insect()

        app.draw()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
