import pygame
import random
import os

# 1. Inicialização do Pygame
pygame.init()

# 2. Configurações da Tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo de Tiro Simples - Navinha")
relogio = pygame.time.Clock()

# 3. Cores (RGB)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)

# 4. Configurações do Jogador (Nave)
nave_largura, nave_altura = 50, 40
nave_x = LARGURA // 2 - nave_largura // 2
nave_y = ALTURA - 60
nave_velocidade = 7

# Assets path
assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))

# Tentar carregar sprite do jogador (rocket.png). Se falhar, usar retângulo.
try:
    player_img = pygame.image.load(os.path.join(assets_path, 'rocket.png')).convert_alpha()
    player_img = pygame.transform.scale(player_img, (nave_largura, nave_altura))
    use_player_image = True
except Exception:
    player_img = None
    use_player_image = False

# 5. Configurações dos Tiros
tiros = []
tiro_velocidade = -10

# 6. Configurações dos Inimigos
inimigos = []
inimigo_largura, inimigo_altura = 40, 40
inimigo_velocidade = 3
frequencia_inimigo = 30  # Quanto menor, mais inimigos aparecem
contador_inimigo = 0

# Loop Principal do Jogo
rodando = True
while rodando:
    tela.fill(PRETO)  # Limpa a tela a cada frame
    contador_inimigo += 1

    # --- EVENTOS (Entradas do Usuário) ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        # Atirar quando pressionar ESPAÇO
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                # Cria um tiro saindo do meio da nave
                tiros.append(pygame.Rect(nave_x + nave_largura//2 - 2, nave_y, 5, 10))

    # Movimentação contínua pelas teclas direcionais
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and nave_x > 0:
        nave_x -= nave_velocidade
    if teclas[pygame.K_RIGHT] and nave_x < LARGURA - nave_largura:
        nave_x += nave_velocidade

    # --- LÓGICA DO JOGO ---

    # Criar novos inimigos no topo da tela aleatoriamente
    if contador_inimigo >= frequencia_inimigo:
        x_aleatorio = random.randint(0, LARGURA - inimigo_largura)
        inimigos.append(pygame.Rect(x_aleatorio, -inimigo_altura, inimigo_largura, inimigo_altura))
        contador_inimigo = 0

    # Movimentar os tiros e removê-los se saírem da tela
    for tiro in tiros[:]:
        tiro.y += tiro_velocidade
        if tiro.y < 0:
            tiros.remove(tiro)

    # Movimentar os inimigos
    for inimigo in inimigos[:]:
        inimigo.y += inimigo_velocidade
        if inimigo.y > ALTURA:
            inimigos.remove(inimigo)  # Inimigo passou direto

    # DETECÇÃO DE COLISÃO (Tiro pega no Inimigo)
    for tiro in tiros[:]:
        for inimigo in inimigos[:]:
            if tiro.colliderect(inimigo):  # Função mágica do Pygame para colisão
                if tiro in tiros: tiros.remove(tiro)
                if inimigo in inimigos: inimigos.remove(inimigo)

    # --- DESENHAR NA TELA ---
    
    # Desenhar o Jogador (Nave) - usar imagem se disponível
    if use_player_image and player_img:
        # Desenhar um fundo claro semi-transparente atrás do sprite para melhorar visibilidade
        bg_w, bg_h = nave_largura + 6, nave_altura + 6
        bg_surf = pygame.Surface((bg_w, bg_h), pygame.SRCALPHA)
        bg_surf.fill((255, 255, 255, 180))  # branco semi-transparente
        tela.blit(bg_surf, (nave_x - 3, nave_y - 3))
        tela.blit(player_img, (nave_x, nave_y))
    else:
        # Desenhar retângulo com fundo claro para contorno (melhor visibilidade)
        pygame.draw.rect(tela, (255, 255, 255), (nave_x-1, nave_y-1, nave_largura+2, nave_altura+2))
        pygame.draw.rect(tela, AZUL, (nave_x, nave_y, nave_largura, nave_altura))

    # Desenhar os Tiros
    for tiro in tiros:
        pygame.draw.rect(tela, AMARELO, tiro)

    # Desenhar os Inimigos
    for inimigo in inimigos:
        pygame.draw.rect(tela, VERMELHO, inimigo)

    # Atualiza a tela e trava a taxa de quadros (FPS) em 60
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()