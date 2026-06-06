import tkinter as tk
from tkinter import messagebox
import random

# definido configuracoes do jogo ========
num_linhas = 4
num_colunas = 4
cartao_size_w = 10
cartao_size_h = 5
cores_cartoes = ['red','blue','green','yellow','purple','orange','cyan','magenta']
cor_fundo = "#343a40"
cor_letra = "#ffffff"
font_style = ('Arial',12,'bold')
max_tentativa = 25

# criar uma grid aleatoria de cores para os cartoes ==========================
def creat_card_grid():
    cores = cores_cartoes*2
    random.shuffle(cores)
    grid = []
    for _ in range(num_linhas):
        linha = []
        for _ in range(num_colunas):
            cor = cores.pop()
            linha.append(cor)
        grid.append(linha)
    return grid
# lida com o click do jabdo no cartoes ==================
def card_click(linha, coluna):
    cartao = cartoes[linha][coluna]
    cor = cartao['bg']
    if cor == 'black':
        cartao['bg'] = grid[linha][coluna] 
        cartao_revelado.append(cartao)
        if len(cartao_revelado) == 2:
            check_match()

# verifica se os dois cartoes revelados sao iguais
def check_match():
    cartao1, cartao2 = cartao_revelado
    if cartao1['bg'] == cartao2['bg']:
        cartao1.after(1000,cartao1.destroy)
        cartao2.after(1000,cartao2.destroy)
        cartoes_correspondante.extend([cartao1,cartao2])
        check_wen() 
    else:
        cartao1.after(1000,lambda:cartao1.config(bg='black'))
        cartao1.after(1000,lambda:cartao2.config(bg='black'))
    cartao_revelado.clear()
    update_score()

# VERIFICA SE O JOGANDO GANHOU O JOGO =====
def check_wen():
    # win when all cards have been matched (total matched widgets equals total cards)
    if len(cartoes_correspondante) == num_linhas * num_colunas:
        messagebox.showinfo('Parábens!', 'Você Ganhou o jogo!')
        janela.quit()
# atualiza a pontuação e verifica se o jogando perdeu o jogo ===========================
def update_score():
    global tentativas
    tentativas += 1
    label_tentativas.config(text="Tentativas: {}/{}".format(tentativas, max_tentativa))
    if tentativas >= max_tentativa:
        messagebox.showinfo('Fim de jogo', 'Você perdeu o jogo')
        janela.quit()

# criando a interface princiapl ===========
janela = tk.Tk()
janela.title('Jogo da Memória')
janela.configure(bg=cor_fundo)

# criar grande de cartoes ===================
grid = creat_card_grid()
cartoes = []
cartao_revelado = []
cartoes_correspondante = []
tentativas = 0
for linha in range(num_linhas):
    linhas_cartoes = []
    for co1 in range(num_colunas):
        # use default args in lambda to capture current loop variables
        cartao = tk.Button(janela, command=lambda r=linha, c=co1: card_click(r, c),width=cartao_size_w, height=cartao_size_h,bg='black', relief=tk.RAISED, bd=1)
        cartao.grid(row=linha, column=co1, padx=5, pady=5)
        linhas_cartoes.append(cartao)
    cartoes.append(linhas_cartoes)


# personarisando o botao================
# usar um dicionario de opções válido para estilos de botão
button_style = {'activebackground': '#f8f9fa','font': font_style,'fg':cor_letra}
janela.option_add('Button', button_style)

# Label para numera de tentativas ==============
label_tentativas = tk.Label(janela, text="Tentativas: {}/{}".format(tentativas, max_tentativa), fg=cor_letra, bg=cor_fundo, font=font_style)
label_tentativas.grid(row=num_linhas,columnspan=num_colunas,padx=10,pady=10)

janela.mainloop()