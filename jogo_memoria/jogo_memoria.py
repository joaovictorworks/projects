import os
import sys
import tkinter as tk
from tkinter import messagebox
import random
from PIL import ImageTk, Image

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import game_utils

# CONFIGURAÇÕES FIXAS DE ESTILO
cor_fundo = "#343a40"
cor_letra = "#ffffff"
font_style = ('Arial', 12, 'bold')

# FORÇAR GRADE 8x10 E ESCOLHER AS PRIMEIRAS 40 IMAGENS PNG
# (10x8 = 80 cartas -> 40 pares)
# Carregar imagens da pasta central de assets (foi movida para ../assets)
assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
base_dir = assets_dir
all_pngs = []
try:
    all_pngs = [f for f in sorted(os.listdir(base_dir)) if f.lower().endswith('.png')]
except Exception:
    all_pngs = []
DESIRED_PAIRS = 40
if len(all_pngs) >= DESIRED_PAIRS:
    arquivos_png = all_pngs[:DESIRED_PAIRS]
else:
    # se houver menos de 40 imagens, usa todas disponíveis; se nenhuma, gera nomes de fallback
    arquivos_png = all_pngs if all_pngs else [f'{i}.png' for i in range(1, DESIRED_PAIRS + 1)]

# Forçar a grade pedida pelo usuário
# Forçar a grade pedida pelo usuário (8 linhas x 10 colunas)
num_linhas = 8
num_colunas = 10

# Total de cartas e tentativas
num_images = len(arquivos_png)
total_cards = num_images * 2
max_tentativa = total_cards

# CRIANDO A INTERFACE PRINCIPAL ===========
janela = tk.Tk()
janela.title('Jogo da Memória')
janela.configure(bg=cor_fundo)

# CARREGAR E REDIMENSIONAR AS IMAGENS =====
tamanho_imagem = (70, 70) # Tamanho da imagem em pixels (Largura x Altura)
imagens_tk = {} # Dicionário para o Python não apagar as imagens da memória

# Loop que carrega cada PNG e salva no dicionário (caminho relativo ao script)
for arquivo in arquivos_png:
    caminho = os.path.join(base_dir, arquivo)
    try:
        img = Image.open(caminho)
        img = img.resize(tamanho_imagem)
        imagens_tk[arquivo] = ImageTk.PhotoImage(img)
    except Exception:
        print(f"Aviso: Não encontrei a imagem {arquivo} em {caminho}.")

# Criando uma imagem toda preta para ser as "Costas" da carta
img_costas = Image.new('RGB', tamanho_imagem, color='black')
foto_costas = ImageTk.PhotoImage(img_costas)

# Subclasse de Button para armazenar atributos personalizados como nome_imagem
class Carta(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.nome_imagem = None

# CRIAR UMA GRID ALEATÓRIA PARA OS CARTÕES ==========================
def creat_card_grid():
    cartas = arquivos_png * 2 # Duplica as 8 imagens para fazer 16 cartas (pares)
    random.shuffle(cartas)
    grid = []
    for _ in range(num_linhas):
        linha = []
        for _ in range(num_colunas):
            linha.append(cartas.pop())
        grid.append(linha)
    return grid

# LIDA COM O CLIQUE DO JOGADOR NOS CARTÕES ==================
def card_click(linha, col):
    # Trava para evitar cliques se já existirem 2 cartões sendo checados
    if len(cartao_revelado) >= 2:
        return

    cartao = cartoes[linha][col]
    nome_imagem_oculta = grid[linha][col]
    
    # Verifica se o cartão já está revelado ou já foi desativado (já fez par)
    if cartao['state'] == tk.DISABLED or cartao in cartao_revelado:
        return
        
    # Vira a carta: Muda a imagem preta pela imagem PNG
    cartao.config(image=imagens_tk[nome_imagem_oculta]) 
    cartao.nome_imagem = nome_imagem_oculta # Guardamos o nome na própria carta para checar depois
    cartao_revelado.append(cartao)
    
    if len(cartao_revelado) == 2:
        # Dá 1 segundo (1000ms) para o jogador ver a segunda carta
        janela.after(1000, check_match)

# VERIFICA SE OS DOIS CARTÕES REVELADOS SÃO IGUAIS
def check_match():
    global cartao_revelado
    cartao1, cartao2 = cartao_revelado
    
    if cartao1.nome_imagem == cartao2.nome_imagem:
        cartao1.config(state=tk.DISABLED)
        cartao2.config(state=tk.DISABLED)
        cartoes_correspondante.extend([cartao1, cartao2])
        check_win() 
    else:
        # Errou! Esconde as cartas e CONTA UMA TENTATIVA
        cartao1.config(image=foto_costas)
        cartao2.config(image=foto_costas)
        update_score() # <--- Mude para cá!
        
    cartao_revelado.clear()

# VERIFICA SE O JOGADOR GANHOU O JOGO =====
def check_win():
    if len(cartoes_correspondante) == num_linhas * num_colunas:
        messagebox.showinfo('Parabéns!', 'Você Ganhou o jogo!')
        # salvar highscore: quanto menos tentativas, melhor -> usamos (max_tentativa - tentativas)
        try:
            score = max(0, max_tentativa - tentativas)
            game_utils.save_highscore('jogo_memoria', score)
        except Exception:
            pass
        janela.quit()

# ATUALIZA A PONTUAÇÃO E VERIFICA SE O JOGADOR PERDEU ===========================
def update_score():
    global tentativas
    tentativas += 1
    label_tentativas.config(text="Tentativas: {}/{}".format(tentativas, max_tentativa))
    if tentativas >= max_tentativa:
        messagebox.showinfo('Fim de jogo', 'Você perdeu o jogo!')
        janela.quit()

# CRIAR GRADE DE CARTÕES ===================
grid = creat_card_grid()
cartoes = []
cartao_revelado = []
cartoes_correspondante = []
tentativas = 0

for linha in range(num_linhas):
    linhas_cartoes = []
    for coluna in range(num_colunas):
        # Aqui removemos o width e height em texto, pois a imagem define o tamanho do botão
        cartao = Carta(janela, image=foto_costas, bg='black',
                       command=lambda r=linha, c=coluna: card_click(r, c),
                       relief=tk.RAISED, bd=1)
        cartao.grid(row=linha, column=coluna, padx=5, pady=5)
        linhas_cartoes.append(cartao)
    cartoes.append(linhas_cartoes)

# LABEL PARA NÚMERO DE TENTATIVAS ==============
label_tentativas = tk.Label(janela, text="Tentativas: {}/{}".format(tentativas, max_tentativa), 
                            fg=cor_letra, bg=cor_fundo, font=font_style)
label_tentativas.grid(row=num_linhas, columnspan=num_colunas, padx=10, pady=10)

janela.mainloop()