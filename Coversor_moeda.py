from tkinter import Tk, ttk
from tkinter import *
from PIL import Image, ImageTk,ImageOps,ImageDraw

import requests 
import json
import string

cor0 = "#FFFFFF"
cor1 = "#333333"
cor2 = "#38576b"

janela = Tk()
janela.geometry('300x350')
janela.title('Conversor')
janela.configure(bg=cor0)
janela.resizable(width=FALSE, height=FALSE)

style = ttk.Style(janela)
style.theme_use('clam')

# Frame superior
frame_cima = Frame(janela, width=300, height=60, bg=cor2)
frame_cima.grid(row=0, column=0)

frame_baixo = Frame(janela, width=300, height=290, bg=cor0)
frame_baixo.grid(row=1, column=0)

# funcão converter -----------------------

def converter():

    moeda_de = combo_de.get()
    moeda_para = combo_para.get()
    valor_entrado = valor.get()

    response = requests.get('https://v6.exchangerate-api.com/v6/43ac6e9e83737b30da257b25/latest/{}'.format(moeda_de))
    dados = json.loads(response.text)
    cambio = dados['conversion_rates'][moeda_para]

    resultado = float(valor_entrado)* float(cambio)

    if moeda_para == 'USD':
        simbolo = '$'
    elif moeda_para == 'EUR':
        simbolo = '€'
    elif moeda_para == 'INR':
        simbolo = '₹'
    elif moeda_para == 'BRL':
        simbolo = 'R$'
    elif moeda_para == 'JPY':
        simbolo = '¥' 
    elif moeda_para == 'AOA':
        simbolo = 'Kz' 

    moeda_equivalente = simbolo + "{:,.2f}".format(resultado)

    app_resultando['text'] = moeda_equivalente

    '''
    'AOA': 'Kz',
    'BRL': 'R$',
    'EUR': '€',
    'INR': '₹',
    'USD': '$',
    'JPY': '¥' 
'''

# Ícone
icon = Image.open('icons8-money-100.png')
icon = icon.resize((40, 40), Image.Resampling.LANCZOS)
icon = ImageTk.PhotoImage(icon)

# Label com ícone + texto
app_nome = Label(frame_cima,image=icon,compound=LEFT,text='Conversor de moeda',padx=10,pady=10,font=('Arial', 14, 'bold'),bg=cor2,fg=cor0)
app_nome.place(relx=0.45, rely=0.5, anchor=CENTER)

# Configuracoes de frame baixo ------------------------------------------
app_resultando = Label(frame_baixo,text='',width=15,height=2,relief='solid',anchor=CENTER,font=('Arial', 14, 'bold'),bg=cor0,fg=cor1)
app_resultando.place(x=55, y=10)

moeda = ['AOA','BRL','EUR','INR','USD','JPY']

app_de = Label(frame_baixo,text='De',width=8,height=1,relief='flat',anchor=NW,font=('Ivy', 10, 'bold'),bg=cor0,fg=cor1)
app_de.place(x=48, y=90)
combo_de = ttk.Combobox(frame_baixo,width=8,justify=CENTER,font=('Ivy',12,'bold'))
combo_de.place(x=50,y=115)
combo_de['values'] = (moeda)


app_para = Label(frame_baixo,text='Para',width=8,height=1,relief='flat',anchor=NW,font=('Ivy', 10, 'bold'),bg=cor0,fg=cor1)
app_para.place(x=150, y=90)
combo_para = ttk.Combobox(frame_baixo,width=8,justify=CENTER,font=('Ivy',12,'bold'))
combo_para.place(x=160,y=115)
combo_para['values'] = (moeda)

valor = Entry(frame_baixo,width=22,justify=CENTER,font=('Iyy',12,'bold'), relief=SOLID)
valor.place(x=50,y=155)

botao = Button(frame_baixo,command=converter,text='Converter',width=19,padx=5,height=1,bg=cor2,fg=cor0,font=('Ivy',12,'bold'),relief='raised',overrelief=RIDGE)
botao.place(x=50,y=210)


janela.mainloop()