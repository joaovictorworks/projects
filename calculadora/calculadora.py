import tkinter as tk

janela = tk.Tk()
janela.title('Calculadora')
janela.geometry('260x360')
janela.configure(bg='#202020')

expressao = ""
texto_visor = tk.StringVar()
texto_visor.set("0")

# --- FUNÇÃO DE CLIQUE (Sem alterações) ---
def ao_clicar(texto):
    global expressao
    
    if texto == '<':
        expressao = expressao[:-1]
        if expressao == "":
            texto_visor.set("0")
        else:
            texto_visor.set(expressao)
            
    elif texto == '=':
        try:
            expressao_calculo = expressao.replace('x', '*')
            resultado = str(eval(expressao_calculo))
            texto_visor.set(resultado)
            expressao = resultado 
        except Exception:
            texto_visor.set("Erro")
            expressao = ""
    else:
        if expressao == "" and texto != '.':
            expressao = texto
        else:
            expressao += texto
        texto_visor.set(expressao)

# --- CONFIGURAÇÃO DO VISOR (PARTE DE CIMA) ---
frame_cima = tk.Frame(janela, bg='#202020', relief='flat')
frame_cima.pack(side='top', fill='x', padx=10, pady=10)

# O Label do visor AGORA FICA NA COLUNA 0 (Esquerda)
app_nome = tk.Label(
    frame_cima, 
    textvariable=texto_visor, 
    width=11, 
    height=2, 
    bg='#202020', 
    fg='white', 
    anchor='e', # Garante que o número fique encostado na direita do label, colado no <
    font=('Ivy', 22, 'bold')
)
app_nome.grid(row=0, column=0, pady=10, sticky='ew')

# Botão '<' AGORA FICA NA COLUNA 1 (Direita)
btn_apagar = tk.Button(
    frame_cima,
    text='<',
    width=3, 
    height=1,
    bg='#202020',
    fg='#FF9500', 
    font=('Arial', 14, 'bold'), 
    relief='flat',
    command=lambda: ao_clicar('<')
)
btn_apagar.grid(row=0, column=1, padx=(5, 5), pady=10, sticky='e')

# INVERSÃO DO WEIGHT: Agora a coluna 0 (visor) expande e empurra o < para o canto direito
frame_cima.grid_columnconfigure(0, weight=1)
frame_cima.grid_columnconfigure(1, weight=0)

# --- CONFIGURAÇÃO DOS BOTÕES (PARTE DE BAIXO - Sem alterações) ---
frmae_botoes = tk.Frame(janela, bg='#202020')
frmae_botoes.pack(side='bottom', anchor='w', padx=10, pady=10)

botoes = [
    ['7','8','9','/'],
    ['4','5','6','x'],
    ['1','2','3','-'],
    ['0','.','=','+']
]

for linha_idx, linha in enumerate(botoes):
    for coluna_idx, texto_botao in enumerate(linha):
        if texto_botao in ['/', 'x', '-', '+', '=']:
            cor_fundo = '#FF9500'
            cor_texto = 'white'
        else:
            cor_fundo = '#333333'
            cor_texto = 'white'
            
        btn = tk.Button(
            frmae_botoes,
            text=texto_botao,
            width=5,
            height=2,
            bg=cor_fundo,
            fg=cor_texto,
            font=('Arial', 11, 'bold'),
            relief='flat',
            command=lambda char=texto_botao: ao_clicar(char)
        )
        btn.grid(row=linha_idx, column=coluna_idx, padx=3, pady=3)

janela.mainloop()
