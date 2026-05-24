from tkinter import *
from tkinter import Tk, ttk
from tkinter import messagebox

# cores -----------------------------
co0 = "#f0f3f5"  # Preta / black
co1 = "#feffff"  # branca / white
co2 = "#3fb5a3"  # verde / green
co3 = "#38576b"  # valor / value
co4 = "#403d3d"   # letra / letters

# configracões da janela -----------------------------
janela = Tk()
janela.title('')
janela.geometry('310x300')
janela.configure(background=co0)
janela.resizable(False,False)
# divisão da janela -----------------------------
frame_cima = Frame(janela,width=310,height=50,bg=co1,relief='flat')
frame_cima.grid(row=0,column=0,padx=1,pady=0,sticky=NSEW)

frame_baixo = Frame(janela,width=310,height=250,bg=co1,relief='flat')
frame_baixo.grid(row=1,column=0,padx=1,pady=0,sticky=NSEW)
# Configurando o frame cima -------------------------------
L_nome = Label(frame_cima,text='LOGIN', anchor=NE,font=('Iyv',25,'bold'),bg=co1,fg=co4)
L_nome.place(x=5,y=5)
L_linha = Label(frame_cima,text='',width=275, anchor=NW,font=('Iyv',1),bg=co2,fg=co4)
L_linha.place(x=10,y=45)

# Configurando o frame baixo -------------------------------
L_nome = Label(frame_baixo,text='Nome: *', anchor=NW,font=('Iyv',10,'bold'),bg=co1,fg=co4)
L_nome.place(x=10,y=20)
e_nome = Entry(frame_baixo,width=25,justify='left',font=('',15),highlightthickness=1,relief='solid')
e_nome.place(x=14,y=50)

L_pass = Label(frame_baixo,text='Senha: *', anchor=NW,font=('Iyv',10,'bold'),bg=co1,fg=co4)
L_pass.place(x=10,y=95)
e_pass = Entry(frame_baixo,width=25,justify='left',show="*",font=('',15),highlightthickness=1,relief='solid')
e_pass.place(x=14,y=130)

credenciais = ['Joao','1234567890']
# funcão verificar senha ----------
def verificar_senha():
    nome = e_nome.get()
    senha = e_pass.get()

    if nome ==  ' admin' and senha == 'admin':
        messagebox.showeinfo('Login', 'seja bem vindo Admin')
    elif credenciais[0] == nome and credenciais[1] == senha:
        messagebox.showinfo('Login' 'Seja bem vindo de volta' + credenciais[0])
    else:
        messagebox.showwarning('Erro' 'Verifique o Nome e a Senha !')


b_confirmar = Button(frame_baixo,text='Entrar',command=verificar_senha,width=39, height=2,font=('Iyv',8,'bold'),bg=co2,fg=co1,relief=RAISED,overrelief=RIDGE)
b_confirmar.place(x=10,y=180)



janela.mainloop()