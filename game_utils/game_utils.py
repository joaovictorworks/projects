import json
import os
import time

try:
    import pygame
except Exception:
    pygame = None

HS_FILE = os.path.join(os.path.dirname(__file__), '.highscores.json')

def _load_all():
    if not os.path.exists(HS_FILE):
        return {}
    try:
        with open(HS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def _save_all(data):
    try:
        with open(HS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def load_highscore(game_name):
    data = _load_all()
    return data.get(game_name, 0)

def save_highscore(game_name, score):
    data = _load_all()
    if score > data.get(game_name, 0):
        data[game_name] = score
        _save_all(data)

def show_game_over_pygame(screen, width, height, score):
    if pygame is None:
        return
    fonte = pygame.font.SysFont('Helvetica', 36)
    small = pygame.font.SysFont('Helvetica', 24)
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    text = fonte.render('Você colidiu!', True, (255, 255, 255))
    sub = small.render(f'Pontuação: {score}  -  Pressione qualquer tecla', True, (200, 200, 200))
    screen.blit(text, (width//2 - text.get_width()//2, height//2 - 40))
    screen.blit(sub, (width//2 - sub.get_width()//2, height//2 + 10))
    pygame.display.update()
    start = time.time()
    waiting = True
    while waiting and time.time() - start < 5:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                waiting = False
            if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        time.sleep(0.02)

def show_game_over_tk(title, message):
    try:
        import tkinter.messagebox as mb
        mb.showinfo(title, message)
    except Exception:
        pass
