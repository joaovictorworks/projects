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

# =====================================================================
# CONFIGURAÇÃO DA GRADE E DAS VARIÁVEIS (DEFINIDAS NO TOPO)
# =====================================================================
num_linhas = 8
num_colunas = 10
DESIRED_PAIRS = 40  # 80 cartas / 2

# Configuração dos caminhos (Procura na própria pasta do jogo)
base_dir = os.path.dirname(os.path.abspath(__file__))

all_pngs = []
try:
    # Lista apenas os arquivos PNG da própria pasta do jogo (ignora ícones se houver)
    all_pngs = [f for f in sorted(os.listdir(base_dir)) if f.lower().endswith('.png') and f.lower() != 'icon.png']
except Exception:
    all_pngs = []

# Garante que teremos exatamente 40 itens na lista
if len(all_pngs) >= DESIRED_PAIRS:
    arquivos_png = all_pngs[:DESIRED_PAIRS]
else:
    arquivos_png = list(all_pngs)
    fim_fallback = DESIRED_PAIRS - len(arquivos_png)
    for i in range(1, fim_fallback + 1):
        arquivos_png.append(f'fallback_{i}.png')

# Total de cartas e tentativas
num_images = len(arquivos_png)
total_cards = num_images * 2
max_tentativa = total_cards

# CRIANDO A INTERFACE PRINCIPAL ===========
janela = tk.Tk()
janela.title('Jogo da Memória')
janela.configure(bg=cor_fundo)

# CARREGAR E REDIMENSIONAR AS IMAGENS =====
tamanho_imagem = (70, 70) 
imagens_tk = {} 

# Criando uma imagem toda preta para ser as "Costas" da carta
img_costas = Image.new('RGB', tamanho_imagem, color='black')
foto_costas = ImageTk.PhotoImage(img_costas)

# Loop que carrega cada PNG e salva no dicionário
for arquivo in arquivos_png:
    caminho = os.path.join(base_dir, arquivo)
    try:
        if "fallback_" in arquivo or not os.path.exists(caminho):
            raise FileNotFoundError
        img = Image.open(caminho)
        img = img.resize(tamanho_imagem)
        imagens_tk[arquivo] = ImageTk.PhotoImage(img)
    except Exception:
        # Placeholder caso a imagem não exista na pasta
        img_placeholder = Image.new('RGB', tamanho_imagem, color='#555555')
        imagens_tk[arquivo] = ImageTk.PhotoImage(img_placeholder)

# Subclasse de Button para armazenar atributos personalizados
class Carta(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.nome_imagem = None

# CRIAR UMA GRID ALEATÓRIA PARA OS CARTÕES ==========================
def creat_card_grid():
    cartas = arquivos_png * 2 
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
    if len(cartao_revelado) >= 2:
        return

    cartao = cartoes[linha][col]
    nome_imagem_oculta = grid[linha][col]
    
    if cartao['state'] == tk.DISABLED or cartao in cartao_revelado:
        return
        
    cartao.config(image=imagens_tk[nome_imagem_oculta]) 
    cartao.nome_imagem = nome_imagem_oculta 
    cartao_revelado.append(cartao)
    
    if len(cartao_revelado) == 2:
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
        cartao1.config(image=foto_costas)
        cartao2.config(image=foto_costas)
        update_score() 
        
    cartao_revelado.clear()

# VERIFICA SE O JOGADOR GANHOU O JOGO =====
def check_win():
    if len(cartoes_correspondante) == num_linhas * num_colunas:
        messagebox.showinfo('Parabéns!', 'Você Ganhou o jogo!')
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

# INICIALIZAÇÃO DA GRADE E ESTADO DO JOGO ===================
grid = creat_card_grid()
cartoes = []
cartao_revelado = []
cartoes_correspondante = []
tentativas = 0

for linha in range(num_linhas):
    linhas_cartoes = []
    for coluna in range(num_colunas):
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