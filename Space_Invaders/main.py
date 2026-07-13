import pygame
from pathlib import Path
import math
import random
pygame.init()
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
vidas = 3
score = 0

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

class Asteroide(object):
    def __init__(self,rank):
        self.rank = rank
        if self.rank == 1:
            self.imagem = asteroide50
        elif self.rank == 2:
            self.imagem = asteroide100
        else:
            self.imagem = asteroide150
        self.largura = 50 * rank
        self.altura = 50 * rank
        self.pontoAleatorio = random.choice([
            (random.randrange(0, largura - self.largura), random.choice([-1*self.altura - 5, altura + 5])),
            (random.choice([-1*self.largura - 5, largura + 5]), random.randrange(0, altura - self.altura))
        ])
        self.x, self.y = self.pontoAleatorio
        if self.x < largura//2:
            self.direcaoX = 1
        else:
            self.direcaoX = -1
        if self.y < altura//2:
            self.direcaoY = 1
        else:
            self.direcaoY = -1
        self.velocidadeX = self.direcaoX * random.randrange(1,3)
        self.velocidadeY = self.direcaoY * random.randrange(1,3)
    
    def desenho(self, tela):
        tela.blit(self.imagem, (self.x, self.y))

def redesenharJogo():
    tela.blit(fundo,(0,0))
    fonte = pygame.font.SysFont('arial',30)
    vidasText = fonte.render('Vidas: ' + str(vidas), 1, (255,255,255))
    playAgainText = fonte.render('Press Space to Play Again', 1, (255,255,255))
    scoreText = fonte.render('Score: ' + str(score), 1, (255,255,255))

    jogador.desenho(tela)
    for a in asteroide:
        a.desenho(tela)
    for b in tirosDoJogador:
        b.desenho(tela)
    if fimDeJogo:
        tela.blit(playAgainText,(largura//2 - playAgainText.get_width()//2, altura//2 - playAgainText.get_height()))
    tela.blit(scoreText,(largura - scoreText.get_width() - 25, 25))
    tela.blit(vidasText,(25,25))
    pygame.display.update()

jogador = Jogador()
tirosDoJogador = []
asteroide = []
conta = 0
rodando = True

while rodando:
    relogio.tick(60)
    conta += 1
    if not fimDeJogo:
        if conta % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroide.append(Asteroide(ran))
        jogador.verificarLocalizacao()
        for b in tirosDoJogador:
            b.movimenta()
            if b.verificarForaDaTela():
                tirosDoJogador.pop(tirosDoJogador.index(b))
        
        for a in asteroide[:]:
            a.x += a.velocidadeX
            a.y += a.velocidadeY

            # colisão jogador com asteroide
            if (jogador.x >= a.x and jogador.x <= a.x + a.largura) or (jogador.x + jogador.largura >= a.x and jogador.x + jogador.largura <= a.x + a.largura):
                if (jogador.y >= a.y and jogador.y <= a.y + a.altura) or (jogador.y + jogador.altura >= a.y and jogador.y + jogador.altura <= a.y + a.altura):
                    vidas -= 1
                    asteroide.pop(asteroide.index(a))
                    break

            # colisão do tiro com asteroide
            for b in tirosDoJogador[:]:
                if ((a.x <= b.x <= a.x + a.largura or a.x <= b.x + b.largura <= a.x + a.largura) and
                    (a.y <= b.y <= a.y + a.altura or a.y <= b.y + b.altura <= a.y + a.altura)):
                    if a.rank == 3:
                        score += 10
                        na1 = Asteroide(2)
                        na2 = Asteroide(2)
                        na1.x = a.x
                        na2.x = a.x
                        na1.y = a.y
                        na2.y = a.y
                        asteroide.append(na1)
                        asteroide.append(na2)
                    elif a.rank == 2:
                        score += 20
                        na1 = Asteroide(1)
                        na2 = Asteroide(1)
                        na1.x = a.x
                        na2.x = a.x
                        na1.y = a.y
                        na2.y = a.y
                        asteroide.append(na1)
                        asteroide.append(na2)
                    else:
                        score += 30
                    asteroide.remove(a)
                    tirosDoJogador.remove(b)
                    break

        if vidas <= 0:
            fimDeJogo = True


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
            if eventos.key == pygame.K_z:
                if not fimDeJogo:
                    tirosDoJogador.append(Tiro())
                else:
                    fimDeJogo = False
                    vidas = 3
                    score = 0
                    asteroide.clear()

    redesenharJogo()

pygame.quit()