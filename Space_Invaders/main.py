import pygame
from pathlib import Path
import math

altura = 800
largura = 725

ASSETS_DIR = Path(__file__).resolve().parent / 'asteroidsPics'

pygame.init()

fundo = pygame.image.load(str(ASSETS_DIR / 'starbg.png'))
imagemAlienigena = pygame.image.load(str(ASSETS_DIR / 'alienShip.png'))
fogueteJogador = pygame.image.load(str(ASSETS_DIR / 'spaceRocket.png'))
estrela = pygame.image.load(str(ASSETS_DIR / 'star.png'))
asteroide50 = pygame.image.load(str(ASSETS_DIR / 'asteroid50.png'))
asteroide100 = pygame.image.load(str(ASSETS_DIR / 'asteroid100.png'))
asteroide150 = pygame.image.load(str(ASSETS_DIR / 'asteroid150.png'))

pygame.display.set_caption('Asteroids')
tela = pygame.display.set_mode((altura, largura))


relogio = pygame.time.Clock()


fimDeJogo = False

class Jogador(object):
    def __init__(self):
        # Redimensiona o foguete para 80% do tamanho original
        tamanho_original_largura = fogueteJogador.get_width()
        tamanho_original_altura = fogueteJogador.get_height()
        self.imagem = pygame.transform.scale(fogueteJogador, (int(tamanho_original_largura * 0.7), int(tamanho_original_altura * 0.7)))
        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()
        self.x = largura//2
        self.y = altura//2
        self.angulo = 0
        self.superficieRotacionada = pygame.transform.rotate(self.imagem,self.angulo)
        self.retanguloRotacionado = self.superficieRotacionada.get_rect()
        self.retanguloRotacionado.center = (int(self.x), int(self.y))
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.cabeca = (int(self.x + self.cosseno * self.largura // 2), int(self.y - self.seno * self.altura // 2))

    def desenho(self,tela):
        tela.blit(self.superficieRotacionada,self.retanguloRotacionado)
    
    def virarEsquerda(self):
        self.angulo += 5
        self.superficieRotacionada = pygame.transform.rotate(self.imagem,self.angulo)
        self.retanguloRotacionado = self.superficieRotacionada.get_rect()
        self.retanguloRotacionado.center = (int(self.x), int(self.y))
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.cabeca = (int(self.x + self.cosseno * self.largura // 2), int(self.y - self.seno * self.altura // 2))

    def virarDireita(self):
        self.angulo -= 5
        self.superficieRotacionada = pygame.transform.rotate(self.imagem,self.angulo)
        self.retanguloRotacionado = self.superficieRotacionada.get_rect()
        self.retanguloRotacionado.center = (int(self.x), int(self.y))
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.cabeca = (int(self.x + self.cosseno * self.largura // 2), int(self.y - self.seno * self.altura // 2))
    
    def mover(self):
        self.x += self.cosseno * 6.0
        self.y -= self.seno * 6.0
        self.superficieRotacionada = pygame.transform.rotate(self.imagem,self.angulo)
        self.retanguloRotacionado = self.superficieRotacionada.get_rect()
        self.retanguloRotacionado.center = (int(self.x), int(self.y))
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.cabeca = (int(self.x + self.cosseno * self.largura // 2), int(self.y - self.seno * self.altura // 2))

    def verificarLocalizacao(self):
        if self.x > largura + 50:
            self.x = 0
        elif self.x < 0 - self.largura:
            self.x = largura
        elif self.y < - 50:
            self.y = altura
        elif self.y > altura + 50:
            self.y = 0

class Tiro(object):
    def __init__(self):
        self.ponto = jogador.cabeca
        self.x,self.y = self.ponto
        self.largura = 4
        self.altura = 4
        self.cos = jogador.cosseno
        self.sen = jogador.seno
        self.velocidadeX = self.cos * 10
        self.velocidadeY = self.sen * 10

    def movimenta(self):
        self.x += self.velocidadeX
        self.y -= self.velocidadeY
    
    def desenho(self,tela):
        pygame.draw.rect(tela,(255,255,255),[self.x,self.y,self.largura,self.altura])

    def verificarForaDaTela(self):
        if self.x < -50 or self.x > largura or self.y > altura or self.y < 50:
            return True

def redesenharJogo():
    tela.blit(fundo,(0,0))
    jogador.desenho(tela)
    for b in tirosDoJogador:
        b.desenho(tela)
    pygame.display.update()

jogador = Jogador()
tirosDoJogador = []
rodando = True
while rodando:
    relogio.tick(68)
    if not fimDeJogo:
        jogador.verificarLocalizacao()
        for b in tirosDoJogador:
            b.movimenta()
            if b.verificarForaDaTela():
                tirosDoJogador.pop(tirosDoJogador.index(b))

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jogador.virarEsquerda()
        if teclas[pygame.K_RIGHT]:
            jogador.virarDireita()
        if teclas[pygame.K_UP]:
            jogador.mover()

    for eventos in pygame.event.get():
        if eventos.type == pygame.QUIT:
            rodando = False
        if eventos.type == pygame.KEYDOWN:
            if eventos.key == pygame.K_SPACE:
                if not fimDeJogo:
                    tirosDoJogador.append(Tiro())

    redesenharJogo()

pygame.quit()
    