import tkinter as tk
from tkinter import messagebox
import game_utils

# Cores modernas ---------------------------------------
co0 = "#FFFFFF"  # branca
co1 = "#333333"  # preta pesado
co2 = "#fcc058"  # laranja
co3 = "#38576b"  # valor
co4 = "#3297a8"  # azul (Jogador 1 - X)
co5 = "#fff873"  # amarela
co7 = "#e85151"  # vermelha (Jogador 2 - O)
fundo = "#3b3b3b" # cinza escuro

# Criando janela principal -----------------------------
janela = tk.Tk()
janela.title('Jogo da Velha')
janela.geometry('260x440')
janela.configure(bg=fundo)
janela.resizable(width=False, height=False)

# Dividindo a janela em 2 frames -----------------------
frame_cima = tk.Frame(janela, width=240, height=100, bg=co1, relief='raised')
frame_cima.pack(fill='x', padx=10, pady=10)

frame_tabuleiro = tk.Frame(janela, bg=fundo, width=240, height=240)
frame_tabuleiro.pack(pady=5)
frame_tabuleiro.pack_propagate(False) # Mantém o tamanho do frame fixo para o centro funcional

# Configurações do frame cima (Placar) -----------------
app_x = tk.Label(frame_cima, text='X', font=('Ivy', 40, 'bold'), bg=co1, fg=co4); app_x.place(x=25, y=10)
app_x_nome = tk.Label(frame_cima, text='Jogador 1', font=('Ivy', 9, 'bold'), bg=co2, fg=co1); app_x_nome.place(x=12, y=70) # Começa destacado

app_x_pontos = tk.Label(frame_cima, text='0', font=('Ivy', 30, 'bold'), bg=co1, fg=co0); app_x_pontos.place(x=80, y=20)
app_separador = tk.Label(frame_cima, text=':', font=('Ivy', 30, 'bold'), bg=co1, fg=co0); app_separador.place(x=115, y=20)
app_o_pontos = tk.Label(frame_cima, text='0', font=('Ivy', 30, 'bold'), bg=co1, fg=co0); app_o_pontos.place(x=135, y=20)

app_o = tk.Label(frame_cima, text='O', font=('Ivy', 40, 'bold'), bg=co1, fg=co7); app_o.place(x=175, y=10)
app_o_nome = tk.Label(frame_cima, text='Jogador 2', font=('Ivy', 9, 'bold'), bg=co1, fg=co0); app_o_nome.place(x=162, y=70)


# Criando lógica do app -------------------------
jogador_1 = "X"
jogador_2 = "O"

pontuacao_x = 0
pontuacao_o = 0

tabelas = [['1','2','3'] , ['4','5','6'] , ['7','8','9']]

jogando = 'X' 
contador = 0 
contador_de_rodada = 0

def Iniciar_Jogo():
    global b_jogar
    b_jogar.pack_forget() 
    # Nova linha: O frame só fica branco na hora que o jogo começa!
    frame_tabuleiro.configure(bg=co0)
    botoes = []

    def atualizar_indicador_vez():
        # Muda o fundo do nome do jogador atual para destacar quem joga
        if jogando == 'X':
            app_x_nome.configure(bg=co2, fg=co1)
            app_o_nome.configure(bg=co1, fg=co0)
        else:
            app_o_nome.configure(bg=co2, fg=co1)
            app_x_nome.configure(bg=co1, fg=co0)

    def controlar(i):
        global jogando, contador, tabelas

        index = i - 1 
        linha_matriz = index // 3
        coluna_matriz = index % 3

        if botoes[index]['text'] == '':
            # CORREÇÃO VISUAL: Cores combinando com o placar original
            cor = co4 if jogando == 'X' else co7

            botoes[index]['fg'] = cor
            botoes[index]['text'] = jogando
            
            tabelas[linha_matriz][coluna_matriz] = jogando

            if jogando == 'X':
                jogando = 'O'
            else:
                jogando = 'X'

            contador += 1
            atualizar_indicador_vez()

            if contador >= 5:
                # Linhas
                if tabelas[0][0] == tabelas[0][1] == tabelas[0][2]: vencedor(tabelas[0][0]); return
                if tabelas[1][0] == tabelas[1][1] == tabelas[1][2]: vencedor(tabelas[1][0]); return
                if tabelas[2][0] == tabelas[2][1] == tabelas[2][2]: vencedor(tabelas[2][0]); return
                
                # Colunas
                if tabelas[0][0] == tabelas[1][0] == tabelas[2][0]: vencedor(tabelas[0][0]); return
                if tabelas[0][1] == tabelas[1][1] == tabelas[2][1]: vencedor(tabelas[0][1]); return
                if tabelas[0][2] == tabelas[1][2] == tabelas[2][2]: vencedor(tabelas[0][2]); return
                
                # Diagonais
                if tabelas[0][0] == tabelas[1][1] == tabelas[2][2]: vencedor(tabelas[0][0]); return
                if tabelas[0][2] == tabelas[1][1] == tabelas[2][0]: vencedor(tabelas[0][2]); return
                
                # Empate
                if contador >= 9:
                    vencedor('Foi Empate')

    def vencedor(vencedor_atual):
        global tabelas, contador_de_rodada, contador, jogando, pontuacao_x, pontuacao_o

        for botao in botoes:
            botao['state'] = 'disabled'

        # CORREÇÃO VISUAL: Label agora expande e centraliza perfeitamente no meio do tabuleiro
        app_vencedor = tk.Label(frame_tabuleiro, text='', font=('Ivy', 14, 'bold'), bg=co1, fg=co2, width=18, height=3, relief='groove')
        app_vencedor.place(relx=0.5, rely=0.5, anchor='center')

        if vencedor_atual == 'X':
            pontuacao_x += 1
            app_vencedor['text'] = 'Jogador 1 Venceu!'
            app_x_pontos['text'] = str(pontuacao_x)
            try:
                game_utils.save_highscore('jogo_velha', pontuacao_x)
            except Exception:
                pass
        elif vencedor_atual == 'O':
            pontuacao_o += 1
            app_vencedor['text'] = 'Jogador 2 Venceu!'
            app_o_pontos['text'] = str(pontuacao_o)
            try:
                game_utils.save_highscore('jogo_velha', pontuacao_o)
            except Exception:
                pass
        elif vencedor_atual == 'Foi Empate':
            app_vencedor['text'] = 'FOI EMPATE!'

    # Criar 9 botões do tabuleiro
    for i in range(1, 10):
        botao = tk.Button(frame_tabuleiro, text='', width=6, height=3, bg=co1, fg=co0, font=('Ivy', 18, 'bold'), relief='ridge', command=lambda i=i: controlar(i))
        row = (i-1) // 3
        col = (i-1) % 3
        botao.grid(row=row, column=col, padx=5, pady=5)
        botoes.append(botao)

    # Centraliza os botões dentro do frame (garante que grid funcione)
    for r in range(3):
        frame_tabuleiro.grid_rowconfigure(r, weight=1)
        frame_tabuleiro.grid_columnconfigure(r, weight=1)

# Botão inicial para começar o jogo
b_jogar = tk.Button(frame_tabuleiro, text='JOGAR', font=('Ivy', 14, 'bold'), bg=co2, fg=co1, width=12, relief='raised', command=Iniciar_Jogo)
b_jogar.pack(expand=True)

# Inicia o loop da interface
janela.mainloop()
