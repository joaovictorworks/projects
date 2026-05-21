from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# Importando Pillow
from PIL import ImageTk, Image

# import strings
import string
import random

# Cores ---------------------------
cor1 = "#0a0a0a"  # black / preta
cor2 = "#fafcff"  # white / branca
cor3 = "#21c25c"  # green / verde
cor4 = "#eb463b"  # red / vermelha
cor5 = "#dedcdc"  # gray / Cizenta
cor6 = "#3080f0"  # blue / azul

# definicões de janela
janela = Tk()
janela.title('')
janela.geometry('295x360')
janela.configure(bg=cor5)
estilo = ttk.Style(janela)
estilo.theme_use('clam')

# dividindo a tela em dois frames -----------------------------------
frame_cima = Frame(janela,width=295,height=50,bg=cor5,pady=0,padx=0,relief='flat')
frame_cima.grid(row=0,column=0,sticky=NSEW)

frame_baixo = Frame(janela,width=295,height=310,bg=cor2,pady=0,padx=0,relief='flat')
frame_baixo.grid(row=1,column=0,sticky=NSEW)

# Trabalhando no frame Cima ---------------------------------
img = Image.open('icons8-password-100.png')
img = img.resize((40,40),Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(img)

app_logo = Label(frame_cima,height=60,image=img,compound=LEFT,padx=10,relief='flat',anchor='nw',bg=cor5)
app_logo.place(x=2,y=2)

app_nome = Label(frame_cima,text='GERADOR DE SENHAS',width=20,height=1,padx=0,relief='flat',anchor='nw',font=('Ivy',16,'bold'),bg=cor5,fg=cor1)
app_nome.place(x=45,y=10)

app_linha = Label(frame_cima,text='',width=295,height=1,padx=0,relief='flat',anchor='nw',font=('Ivy',1),bg=cor4,fg=cor1)
app_linha.place(x=0,y=45)

# ----------------------- funcoes gerar senha -------------------
def criar_senhar():
    alfa_maior = string.ascii_uppercase
    alfa_menor = string.ascii_lowercase
    numeros = '1234567890'
    simbolos = '@!#$[]{}()*;:/,_-.,+'

    global combinar
    combinar = ""

    if estado_1.get() == alfa_maior:
        combinar += alfa_maior

    if estado_2.get() == alfa_menor:
        combinar += alfa_menor

    if estado_3.get() == numeros:
        combinar += numeros

    if estado_4.get() == simbolos:
        combinar += simbolos

    if combinar == "":
        app_senha['text'] = "Selecione uma opção"
        return

    comprimento = int(spin.get())
    senha = "".join(random.sample(combinar, comprimento))
    app_senha['text'] = senha

    # Ativa o botão copiar e define o comando
    botão_copiar_senha.config(command=lambda: copiar_senha(senha))
    botão_copiar_senha.grid()  # mostra o botão


def copiar_senha(senha):
    janela.clipboard_clear()
    janela.clipboard_append(senha)
    janela.update()  # ← AGORA FUNCIONA DE VERDADE
    messagebox.showinfo("Sucesso", "A senha foi copiada com sucesso!")


#------------------------------ Botão copia -----------------------------
botão_copiar_senha = Button(frame_baixo,text='COPIAR',width=7,height=2,overrelief='solid',relief='raised',anchor='center',font=('Ivy',10,'bold'),bg=cor6,fg=cor1) 
# Não mostra ainda
botão_copiar_senha.grid(row=0,column=1,sticky=NW,padx=7,pady=10,columnspan=1)
botão_copiar_senha.grid_remove()


#Trabalhando em frame Baixo --------------------------------
app_senha = Label(frame_baixo,text='----',width=21,height=2,padx=0,relief='solid',anchor='center',font=('Ivy',12,'bold'),bg=cor2,fg=cor1)
app_senha.grid(row=0,column=0,columnspan=1,sticky=NSEW,padx=3,pady=10)

app_info = Label(frame_baixo,text='Numero Total de caracteres na senha',height=1,padx=0,relief='flat',anchor='nw',font=('Ivy',10,'bold'),bg=cor2,fg=cor1)
app_info.grid(row=1,column=0,columnspan=2,sticky=NSEW,padx=5,pady=1)

var = IntVar()
var.set(8)
spin = Spinbox(frame_baixo, from_=0,to=20,width=5,textvariable=var)
spin.grid(row=2,column=0,columnspan=2,sticky=NW,padx=5,pady=8)

alfa_maior = string.ascii_uppercase
alfa_menor = string.ascii_lowercase
numeros = '1234567890'
simbolos = '@!#$[]{}()*;:/,_-.,+'

frame_caracters = Frame(frame_baixo,width=295,height=210,bg=cor2,pady=0,padx=0,relief='flat')
frame_caracters.grid(row=3,column=0,sticky=NSEW,columnspan=3)

# -------------------------Letras maiuculas---------------------------------------
estado_1 = StringVar()
estado_1.set(False)
check_1 = Checkbutton(frame_caracters, width=1, variable=estado_1, onvalue=alfa_maior, offvalue="off", relief='flat', bg=cor2)
check_1.grid(row=0,column=0,sticky=NW,padx=2,pady=5)
app_info = Label(frame_caracters,text='ABC Letras maiusculas',height=1,padx=0,relief='flat',anchor='nw',font=('Ivy',10,'bold'),bg=cor2,fg=cor1)
app_info.grid(row=0,column=1,sticky=NW,padx=2,pady=5)
# ------------------------------- Letras minusculas ------------------------------
estado_2 = StringVar()
estado_2.set(False)
check_2 = Checkbutton(frame_caracters, width=1, variable=estado_2, onvalue=alfa_menor, offvalue="off", relief='flat', bg=cor2)
check_2.grid(row=1,column=0,sticky=NW,padx=2,pady=5)
app_info = Label(frame_caracters,text='ABC Letras minusculas',height=1,padx=0,relief='flat',anchor='nw',font=('Ivy',10,'bold'),bg=cor2,fg=cor1)
app_info.grid(row=1,column=1,sticky=NW,padx=2,pady=5)
# -------------------------- Numeros------------------------------
estado_3 = StringVar()
estado_3.set(False)
check_3 = Checkbutton(frame_caracters, width=1, variable=estado_3, onvalue=numeros, offvalue="off", relief='flat', bg=cor2)
check_3.grid(row=2,column=0,sticky=NW,padx=2,pady=5)
app_info = Label(frame_caracters,text='123 Números',height=1,padx=0,relief='flat',anchor='nw',font=('Ivy',10,'bold'),bg=cor2,fg=cor1)
app_info.grid(row=2,column=1,sticky=NW,padx=2,pady=5)
# ------------------------- Simbolos---------------------------
estado_4 = StringVar()
estado_4.set(False)
check_4= Checkbutton(frame_caracters, width=1, variable=estado_4, onvalue=simbolos, offvalue="off", relief='flat', bg=cor2)
check_4.grid(row=3,column=0,sticky=NW,padx=2,pady=5)
app_info = Label(frame_caracters,text='!@# Simbolos',height=1,padx=0,relief='flat',anchor='nw',font=('Ivy',10,'bold'),bg=cor2,fg=cor1)
app_info.grid(row=3,column=1,sticky=NW,padx=2,pady=5)
#----------------------------------- Botão-----------------------------------
botão_gerar_senha = Button(frame_caracters,command=criar_senhar,text='Gerar Senha',width=34,height=1,overrelief='solid',relief='flat',anchor='center',font=('Ivy',10,'bold'),bg=cor4,fg=cor1)
botão_gerar_senha.grid(row=5,column=0,sticky=NSEW,padx=7,pady=12,columnspan=5)


janela.mainloop()
