import tkinter
from tkinter import * # pyright: ignore[reportWildcardImportFromLibrary]
from tkinter import ttk
from PIL import Image, ImageTk
import os

# cores ----------------------------------------------------------
co0 = "#FFFFFF"  # white
co1 = "#333333"  # preta
co2 = "#111214"  # preta
co3 = "#4ed48a"  # verde / green
co4 = "#ff2457"  # vermelha / red

janela = Tk()
janela.title('Teste de Digitação')
janela.geometry('390x310')
janela.configure(bg=co0)

# Dividindo a janela ---------------------------------
frame_logo = Frame(janela, width=390, height=60, bg=co0, relief=FLAT)
frame_logo.grid(row=0, column=0)

frame_tela = Frame(janela, width=390, height=60, bg=co1, relief=FLAT)
frame_tela.grid(row=1, column=0)

frame_corpo = Frame(janela, width=390, height=190, bg=co0, relief=FLAT)
frame_corpo.grid(row=2, column=0)

# configurando o frame logo -----------------------------------
caminho_icone = os.path.join(os.path.dirname(__file__), 'icon.png')
imagen = Image.open(caminho_icone)

imagen = imagen.resize((50, 50), Image.Resampling.LANCZOS)
imagen = ImageTk.PhotoImage(imagen)

l_logo = Label(frame_logo, image=imagen, bg=co0,fg=co1,compound=LEFT,padx=10)
l_logo.place(x=10, y=10)
l_nome = Label(frame_logo, text='Teste de velocidade de digitação', font=('Arial', 15, "bold"), anchor="nw", justify='left', bg=co0, fg=co1)
l_nome.place(x=65, y=20)

frases = ["Olá, eu sou o João",
          "O mundial do Palmeras existe sim",
          "Se eu fosse a Liberadade, eu me daria a liberdade"
          "Louco é quem não acredita no Mundial do Palmeras",
          "Plana ou redonda, o que importa mesmo é cuidarmos da terra",
          "Compartilha este vídeo em seus grupos do facebook",
]

# função verificar 
def verificar():
    pass

# funcão iniciar
def iniciar():
    global frases
    global frase_digitada
    global b_verificar
    global l_velocidade
    global l_precisao
    global l_tempo

    # removendo o botão iniciar
    b_iniciar.destroy()


    # digite a frases
    l_digite = Label(frame_corpo,text='Digite a frase acima',font=('Arial',10,),bg=co0,fg=co0)
    l_digite.grid(row=0,column=0,padx=5,pady=10)

    frase_digitada = StringVar()
    e_digite = Entry(frame_corpo,textvariable=frase_digitada,width=42,relief=SOLID,font=('Arial',12),bg=co0,fg=co0)
    e_digite.grid(row=1,column=0,padx=5,pady=5)

    b_verificar = Button(frame_corpo,text='Verificar',font=('Ivy',8,'bold'),bg=co3,fg=co0)
    b_verificar.grid(row=2,column=0,padx=5,pady=15)

# configurando o frame tela -----------------------------------
l_tela = Label(frame_tela,text='Frase as ser digitada',width=32,height=3,font=('Ivy',11,'bold'),justify="left",wraplength=300,bg=co1,fg=co0)
l_tela.grid(row=0,column=0,padx=50,pady=6)

# configurando o frame corpo ---------------------------------
b_iniciar = Button(frame_corpo,command=iniciar,text='Iniciar o seu Texto',font=('Ivy',10,'bold'),justify="left",bg=co3,fg=co0)
b_iniciar.grid(row=0,column=0,padx=50,pady=40)

l_tempo = Label(frame_corpo,text='tempo 300',width=30,font=('Ivy',10,'bold'),anchor='nw',justify="left",bg=co0,fg=co1)
l_tempo.grid(row=1,column=0,padx=2,pady=5)

l_precisao = Label(frame_corpo,text='Precisão',width=30,font=('Ivy',10,'bold'),anchor='nw',justify="left",bg=co0,fg=co1)
l_precisao.grid(row=2,column=0,padx=2,pady=5)

l_velocidade = Label(frame_corpo,text='Velocidade',width=30,font=('Ivy',10,'bold'),anchor='nw',justify="left",bg=co0,fg=co1)
l_velocidade.grid(row=3,column=0,padx=2,pady=5)

janela.mainloop()