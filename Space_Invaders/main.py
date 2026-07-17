import pygame
import math
import random

pygame.init()

largura = 800
altura = 750

fundo = pygame.image.load('asteroidsPics/starbg.png')
imagemAlienigena = pygame.image.load('asteroidsPics/alienShip.png')
fogueteJogador = pygame.image.load('asteroidsPics/spaceRocket.png')
estrela = pygame.image.load('asteroidsPics/star.png')
asteroide50 = pygame.image.load('asteroidsPics/asteroid50.png')
asteroide100 = pygame.image.load('asteroidsPics/asteroid100.png')
asteroide150 = pygame.image.load('asteroidsPics/asteroid150.png')

tiro = pygame.mixer.Sound('sounds/sounds_shoot.wav')
bangGrande = pygame.mixer.Sound('sounds/sounds_bangLarge.wav')
bangPequeno = pygame.mixer.Sound('sounds/sounds_bangSmall.wav')
tiro.set_volume(.25)
bangGrande.set_volume(.25)
bangPequeno.set_volume(.25)

pygame.display.set_caption('Asteroids')
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

fimDeJogo = False
vidas = 3
pontuacao = 0
tiroRapido = False
inicioTiroRapido = -1
somLigado = True
maiorPontuacao = 0


class Jogador(object):
    def __init__(self):
        # Redimensiona o foguete para 70% do tamanho original
        tamanho_original_largura = fogueteJogador.get_width()
        tamanho_original_altura = fogueteJogador.get_height()
        self.img = pygame.transform.scale(fogueteJogador, (int(tamanho_original_largura * 0.7), int(tamanho_original_altura * 0.7)))
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.x = float(largura // 2)
        self.y = float(altura // 2)
        self.angulo = 0
        self.superficieRotacionada = pygame.transform.rotate(self.img, self.angulo)
        self.retanguloRotacionado = self.superficieRotacionada.get_rect()
        self.retanguloRotacionado.center = (int(self.x), int(self.y))
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.cabeca = (int(self.x + self.cosseno * self.largura // 2), int(self.y - self.seno * self.altura // 2))

    def desenhar(self, tela):
        tela.blit(self.superficieRotacionada, self.retanguloRotacionado)

    def virarEsquerda(self):
        self.angulo += 5
        self.superficieRotacionada = pygame.transform.rotate(self.img, self.angulo)
        self.retanguloRotacionado = self.superficieRotacionada.get_rect()
        self.retanguloRotacionado.center = (int(self.x), int(self.y))
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.cabeca = (int(self.x + self.cosseno * self.largura // 2), int(self.y - self.seno * self.altura // 2))

    def virarDireita(self):
        self.angulo -= 5
        self.superficieRotacionada = pygame.transform.rotate(self.img, self.angulo)
        self.retanguloRotacionado = self.superficieRotacionada.get_rect()
        self.retanguloRotacionado.center = (int(self.x), int(self.y))
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.cabeca = (int(self.x + self.cosseno * self.largura // 2), int(self.y - self.seno * self.altura // 2))

    def moverFrente(self):
        self.x += self.cosseno * 8
        self.y -= self.seno * 8
        self.superficieRotacionada = pygame.transform.rotate(self.img, self.angulo)
        self.retanguloRotacionado = self.superficieRotacionada.get_rect()
        self.retanguloRotacionado.center = (int(self.x), int(self.y))
        self.cosseno = math.cos(math.radians(self.angulo + 90))
        self.seno = math.sin(math.radians(self.angulo + 90))
        self.cabeca = (int(self.x + self.cosseno * self.largura // 2), int(self.y - self.seno * self.altura // 2))

    def atualizarLocalizacao(self):
        if self.x > largura + 50:
            self.x = 0
        elif self.x < 0 - self.largura:
            self.x = largura
        elif self.y < -50:
            self.y = altura
        elif self.y > altura + 50:
            self.y = 0


class Tiro(object):
    def __init__(self):
        self.ponto = jogador.cabeca
        self.x, self.y = self.ponto
        self.largura = 4
        self.altura = 4
        self.c = jogador.cosseno
        self.s = jogador.seno
        self.velocidadeX = self.c * 14
        self.velocidadeY = self.s * 14

    def mover(self):
        self.x += self.velocidadeX
        self.y -= self.velocidadeY

    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 255, 255), [self.x, self.y, self.largura, self.altura])

    def verificarForaDaTela(self):
        if self.x < -50 or self.x > largura or self.y > altura or self.y < -50:
            return True


class Asteroide(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.imagem = asteroide50
        elif self.rank == 2:
            self.imagem = asteroide100
        else:
            self.imagem = asteroide150
        self.largura = 50 * rank
        self.altura = 50 * rank
        self.pontoAleatorio = random.choice([(random.randrange(0, largura - self.largura), random.choice([-1 * self.altura - 5, altura + 5])), (random.choice([-1 * self.largura - 5, largura + 5]), random.randrange(0, altura - self.altura))])
        self.x, self.y = self.pontoAleatorio
        if self.x < largura // 2:
            self.direcaoX = 1
        else:
            self.direcaoX = -1
        if self.y < altura // 2:
            self.direcaoY = 1
        else:
            self.direcaoY = -1
        self.velocidadeX = self.direcaoX * random.randrange(2, 4)
        self.velocidadeY = self.direcaoY * random.randrange(2, 4)

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x, self.y))


class Estrela(object):
    def __init__(self):
        # Redimensiona a estrela para 50% do tamanho original
        tamanho_original_largura = estrela.get_width()
        tamanho_original_altura = estrela.get_height()
        self.img = pygame.transform.scale(estrela, (int(tamanho_original_largura * 0.5), int(tamanho_original_altura * 0.5)))
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.pontoAleatorio = random.choice([(random.randrange(0, largura - self.largura), random.choice([-1 * self.altura - 5, altura + 5])),
                                       (random.choice([-1 * self.largura - 5, largura + 5]), random.randrange(0, altura - self.altura))])
        self.x, self.y = self.pontoAleatorio
        if self.x < largura // 2:
            self.direcaoX = 1
        else:
            self.direcaoX = -1
        if self.y < altura // 2:
            self.direcaoY = 1
        else:
            self.direcaoY = -1
        self.velocidadeX = self.direcaoX * 3
        self.velocidadeY = self.direcaoY * 3

    def desenhar(self, tela):
        tela.blit(self.img, (self.x, self.y))


class Alienigena(object):
    def __init__(self):
        self.img = imagemAlienigena
        self.largura = self.img.get_width()
        self.altura = self.img.get_height()
        self.pontoAleatorio = random.choice([(random.randrange(0, largura - self.largura), random.choice([-1 * self.altura - 5, altura + 5])),
                                       (random.choice([-1 * self.largura - 5, largura + 5]), random.randrange(0, altura - self.altura))])
        self.x, self.y = self.pontoAleatorio
        if self.x < largura // 2:
            self.direcaoX = 1
        else:
            self.direcaoX = -1
        if self.y < altura // 2:
            self.direcaoY = 1
        else:
            self.direcaoY = -1
        self.velocidadeX = self.direcaoX * 3
        self.velocidadeY = self.direcaoY * 3

    def desenhar(self, tela):
        tela.blit(self.img, (self.x, self.y))


class TiroAlienigena(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 4
        self.altura = 4
        self.dx, self.dy = jogador.x - self.x, jogador.y - self.y
        self.distancia = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx / self.distancia, self.dy / self.distancia
        self.velocidadeX = self.dx * 7
        self.velocidadeY = self.dy * 7

    def desenhar(self, tela):
        pygame.draw.rect(tela, (255, 255, 255), [self.x, self.y, self.largura, self.altura])


def redesenharJanela():
    tela.blit(fundo, (0, 0))
    fonte = pygame.font.SysFont('arial', 30)
    textoVidas = fonte.render('Vidas: ' + str(vidas), 1, (255, 255, 255))
    textoJogarNovamente = fonte.render('Pressione Tab para Jogar Novamente', 1, (255, 255, 255))
    textoPontuacao = fonte.render('Pontuação: ' + str(pontuacao), 1, (255, 255, 255))
    textoMaiorPontuacao = fonte.render('Maior Pontuação: ' + str(maiorPontuacao), 1, (255, 255, 255))

    jogador.desenhar(tela)
    for a in asteroides:
        a.desenhar(tela)
    for b in tirosJogador:
        b.desenhar(tela)
    for s in estrelas:
        s.desenhar(tela)
    for a in alienigenas:
        a.desenhar(tela)
    for b in tirosAlienigena:
        b.desenhar(tela)

    if tiroRapido:
        pygame.draw.rect(tela, (0, 0, 0), [largura // 2 - 51, 19, 102, 22])
        pygame.draw.rect(tela, (255, 255, 255), [largura // 2 - 50, 20, 100 - 100 * (contagem - inicioTiroRapido) / 500, 20])

    if fimDeJogo:
        tela.blit(textoJogarNovamente, (largura // 2 - textoJogarNovamente.get_width() // 2, altura // 2 - textoJogarNovamente.get_height() // 2))
    tela.blit(textoPontuacao, (largura - textoPontuacao.get_width() - 25, 25))
    tela.blit(textoVidas, (25, 25))
    tela.blit(textoMaiorPontuacao, (largura - textoMaiorPontuacao.get_width() - 25, 35 + textoPontuacao.get_height()))
    pygame.display.update()


jogador = Jogador()
tirosJogador = []
asteroides = []
contagem = 0
estrelas = []
alienigenas = []
tirosAlienigena = []
rodando = True
while rodando:
    relogio.tick(60)
    contagem += 1
    if not fimDeJogo:
        if contagem % 50 == 0:
            ran = random.choice([1, 1, 1, 2, 2, 3])
            asteroides.append(Asteroide(ran))
        if contagem % 1000 == 0:
            estrelas.append(Estrela())
        if contagem % 750 == 0:
            alienigenas.append(Alienigena())
        for i, a in enumerate(alienigenas):
            a.x += a.velocidadeX
            a.y += a.velocidadeY
            if a.x > largura + 150 or a.x + a.largura < -100 or a.y > altura + 150 or a.y + a.altura < -100:
                alienigenas.pop(i)
            if contagem % 60 == 0:
                tirosAlienigena.append(TiroAlienigena(a.x + a.largura // 2, a.y + a.altura // 2))

            for b in tirosJogador:
                if (b.x >= a.x and b.x <= a.x + a.largura) or b.x + b.largura >= a.x and b.x + b.largura <= a.x + a.largura:
                    if (b.y >= a.y and b.y <= a.y + a.altura) or b.y + b.altura >= a.y and b.y + b.altura <= a.y + a.altura:
                        alienigenas.pop(i)
                        if somLigado:
                            bangGrande.play()
                        pontuacao += 50
                        break

        for i, b in enumerate(tirosAlienigena):
            b.x += b.velocidadeX
            b.y += b.velocidadeY
            if (b.x >= jogador.x - jogador.largura // 2 and b.x <= jogador.x + jogador.largura // 2) or b.x + b.largura >= jogador.x - jogador.largura // 2 and b.x + b.largura <= jogador.x + jogador.largura // 2:
                if (b.y >= jogador.y - jogador.altura // 2 and b.y <= jogador.y + jogador.altura // 2) or b.y + b.altura >= jogador.y - jogador.altura // 2 and b.y + b.altura <= jogador.y + jogador.altura // 2:
                    vidas -= 1
                    tirosAlienigena.pop(i)
                    break

        jogador.atualizarLocalizacao()
        for b in tirosJogador:
            b.mover()
            if b.verificarForaDaTela():
                tirosJogador.pop(tirosJogador.index(b))

        for a in asteroides:
            a.x += a.velocidadeX
            a.y += a.velocidadeY

            if (a.x >= jogador.x - jogador.largura // 2 and a.x <= jogador.x + jogador.largura // 2) or (a.x + a.largura <= jogador.x + jogador.largura // 2 and a.x + a.largura >= jogador.x - jogador.largura // 2):
                if (a.y >= jogador.y - jogador.altura // 2 and a.y <= jogador.y + jogador.altura // 2) or (a.y + a.altura >= jogador.y - jogador.altura // 2 and a.y + a.altura <= jogador.y + jogador.altura // 2):
                    vidas -= 1
                    asteroides.pop(asteroides.index(a))
                    if somLigado:
                        bangGrande.play()
                    break

            # colisao tiro com asteroide
            for b in tirosJogador:
                if (b.x >= a.x and b.x <= a.x + a.largura) or b.x + b.largura >= a.x and b.x + b.largura <= a.x + a.largura:
                    if (b.y >= a.y and b.y <= a.y + a.altura) or b.y + b.altura >= a.y and b.y + b.altura <= a.y + a.altura:
                        if a.rank == 3:
                            if somLigado:
                                bangGrande.play()
                            pontuacao += 10
                            na1 = Asteroide(2)
                            na2 = Asteroide(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroides.append(na1)
                            asteroides.append(na2)
                        elif a.rank == 2:
                            if somLigado:
                                bangPequeno.play()
                            pontuacao += 20
                            na1 = Asteroide(1)
                            na2 = Asteroide(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroides.append(na1)
                            asteroides.append(na2)
                        else:
                            pontuacao += 30
                            if somLigado:
                                bangPequeno.play()
                        asteroides.pop(asteroides.index(a))
                        tirosJogador.pop(tirosJogador.index(b))
                        break

        for s in estrelas:
            s.x += s.velocidadeX
            s.y += s.velocidadeY
            if s.x < -100 - s.largura or s.x > largura + 100 or s.y > altura + 100 or s.y < -100 - s.altura:
                estrelas.pop(estrelas.index(s))
                break
            for b in tirosJogador:
                if (b.x >= s.x and b.x <= s.x + s.largura) or b.x + b.largura >= s.x and b.x + b.largura <= s.x + s.largura:
                    if (b.y >= s.y and b.y <= s.y + s.altura) or b.y + b.altura >= s.y and b.y + b.altura <= s.y + s.altura:
                        tiroRapido = True
                        inicioTiroRapido = contagem
                        estrelas.pop(estrelas.index(s))
                        tirosJogador.pop(tirosJogador.index(b))
                        break

        if vidas <= 0:
            fimDeJogo = True

        if inicioTiroRapido != -1:
            if contagem - inicioTiroRapido > 500:
                tiroRapido = False
                inicioTiroRapido = -1

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            jogador.virarEsquerda()
        if teclas[pygame.K_RIGHT]:
            jogador.virarDireita()
        if teclas[pygame.K_UP]:
            jogador.moverFrente()
        if teclas[pygame.K_z]:
            if tiroRapido:
                tirosJogador.append(Tiro())
                if somLigado:
                    tiro.play()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_z:
                if not fimDeJogo:
                    if not tiroRapido:
                        tirosJogador.append(Tiro())
                        if somLigado:
                            tiro.play()
            if evento.key == pygame.K_m:
                somLigado = not somLigado
            if evento.key == pygame.K_TAB:
                if fimDeJogo:
                    fimDeJogo = False
                    vidas = 3
                    asteroides.clear()
                    alienigenas.clear()
                    tirosAlienigena.clear()
                    estrelas.clear()
                    if pontuacao > maiorPontuacao:
                        maiorPontuacao = pontuacao
                    pontuacao = 0

    redesenharJanela()
pygame.quit()