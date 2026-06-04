import tkinter as tk
from tkinter import messagebox

#cores---------------------
cor0 = "#444466"  # Preta
cor1 = "#feffff"  # branca
cor2 = "#000000" # black/Preto rock
# criando a janela --------------
janela = tk.Tk()
janela.geometry('530x205')
janela.config(bg=cor1)
# configurando a janela -------------
tela = tk.Label(janela,bg=cor2,width=40,height=10,bd=1)
tela.grid(row=0,column=0)

frame_direita = tk.Frame(janela,bg=cor1)
frame_direita.grid(row=0,column=1,padx=5)

frame_baixo = tk.Frame(janela,bg=cor1)
frame_baixo.grid(row=1,column=0,columnspan=2,pady=15)
# função scale
def escala(valor):
    r = s_red.get()
    g = s_green.get()
    b = s_blue.get()
    
    rgb = f'{r}, {g} , {b}'
    

    hexadecimal = '#%02x%02x%02x' % (r,g,b)

    # alterando a cor do fundo
    tela['bg'] = hexadecimal

    # alterando a entry
    e_cor.delete(0,tk.END)
    e_cor.insert(0,hexadecimal)

# funcoa clica 
def onClick():
    # infromar
    messagebox.showinfo('Cor',"A cor foi copiada")


    # serve para criar botao copiar
    clip = tk.Tk()
    clip.withdraw()
    clip.clipboard_clear() 
    clip.clipboard_append(e_cor.get())
    clip.destroy()   

# configurando o frame direita -------------------
l_red = tk.Label(frame_direita,text='Red',width=7,bg=cor1,fg='red',anchor='nw',font=('Time New Roman',12,'bold'))
l_red.grid(row=0,column=0)
s_red = tk.Scale(frame_direita,command=escala,from_=0,to=255,length=150,bg=cor1,fg='red',orient=tk.HORIZONTAL)
s_red.grid(row=0,column=1)

l_green = tk.Label(frame_direita,text='Green',width=7,bg=cor1,fg='green',anchor='nw',font=('Time New Roman',12,'bold'))
l_green.grid(row=1,column=0)
s_green = tk.Scale(frame_direita,command=escala,from_=0,to=255,length=150,bg=cor1,fg='green',orient=tk.HORIZONTAL)
s_green.grid(row=1,column=1)

l_blue = tk.Label(frame_direita,text='Blue',width=7,bg=cor1,fg='blue',anchor='nw',font=('Time New Roman',12,'bold'))
l_blue.grid(row=2,column=0)
s_blue = tk.Scale(frame_direita,command=escala,from_=0,to=255,length=150,bg=cor1,fg='blue',orient=tk.HORIZONTAL)
s_blue.grid(row=2,column=1)

# configurando o frame baixo -------------------
l_rgb = tk.Label(frame_baixo,text='CÓDIGO RGB :',bg=cor1,font=('Iyv',10,'bold'))
l_rgb.grid(row=0,column=0,padx=5)
# entry
e_cor = tk.Entry(frame_baixo,width=12,font=('Iyv',10,'bold'),justify='center')
e_cor.grid(row=0,column=1,padx=5)

# botao copia
b_copia = tk.Button(frame_baixo,text='Copiar a Cor',command=onClick,bg=cor1,font=('Iyv',8,'bold'),relief='raised',overrelief='ridge')
b_copia.grid(row=0,column=2,padx=5)

# app nome
l_app_nome = tk.Label(frame_baixo,text='Seletor de Cores',anchor='nw',bg=cor1,font=('Iyv',15,'bold'))
l_app_nome.grid(row=0,column=3,padx=40)

janela.mainloop()