from tkinter import *
import tkinter

# cores
cor1 = "#0a0a0a"  # black / preta
cor2 = "#fafcff"  # white / branca
cor3 = "#21c25c"  # green / verde
cor4 = "#eb463b"  # red / vermelha
cor5 = "#dedcdc"  # gray / Cizenta
cor6 = "#3080f0"  # blue / azul

# configuracões da janela ----------------------
janela = Tk()
janela.title("")
janela.geometry('300x180')
janela.configure(bg=cor1)
janela.resizable(FALSE,FALSE)

# definindo variaveis globais --------------------------

global tempo
global rodar
global contador
global limitador

limitador = 59
tempo = '00:00:00'
rodar = False
contador = 1

# funcão iniciar
# def iniciar():
#     global tempo
#     global contador
#     global limitador

#     if rodar:
#         # antes do cronomentro começar
#         if contador <=1:
#             inicio = 'Comecendo em ' +str(contador)
#             label_tempo['text'] = inicio
#             label_tempo['font'] = 'Arial',10
        
#         # depois do cronometro começar
#         else:
#             label_tempo['font'] = ('Times',50,'bold')
#             temporario = str(tempo)
#             h,m,s = map(int,temporario.split(":"))
#             h = int(h)
#             m = int(m)
#             s = int(contador)
        
#         if (s>limitador):
#             contador = 0
#             m +=1

#         s = str(0)+str(s)
#         m = str(0)+str(m)
#         h = str(0)+str(h)

#         temporario = str(h[-2:]) + ":" + str(m[-2:]) + ":" +str(s[-2:])
#         label_tempo['text'] = temporario
#         tempo = temporario

#         # atualizando os valores atuais
#         label_tempo.after(1000,iniciar)
#         contador +=1

def iniciar():
    global tempo
    global contador
    global limitador
    global rodar

    if rodar:

        # Contagem regressiva
        if contador <= 0:
            inicio = f"Começando em {contador}"
            label_tempo['text'] = inicio
            label_tempo['font'] = ('Arial', 12)

            h = 0
            m = 0
            s = 0

        # Cronômetro normal
        else:
            label_tempo['font'] = ('Times', 50, 'bold')

            h, m, s = map(int, tempo.split(":"))
            s += 1

            if s > limitador:
                s = 0
                m += 1

            if m >= 60:
                m = 0
                h += 1

        temporario = f"{h:02d}:{m:02d}:{s:02d}"
        label_tempo['text'] = temporario
        tempo = temporario

        contador += 1
        label_tempo.after(1000, iniciar)

# funcão para dar inicio
def start():
    global rodar
    if not rodar:
        rodar = True
        iniciar()

# funcão para pausar
def pausar():
    global rodar
    rodar = False


# funcão para reiniciar
# def reiniciar():
#     global tempo
#     global contador

#     # reiniciando o contador
#     contador = 0
#     # reiniciando o tempo
#     tempo = '00:00:00'
#     label_tempo['text'] = tempo

def reiniciar():
    global tempo
    global contador
    global rodar

    rodar = False
    contador = 0
    tempo = "00:00:00"
    label_tempo['text'] = tempo

# criando labels--------------------------
label_app = Label(janela, text="cronômentro", font=('Arial,18'),bg=cor1,fg=cor2)
label_app.place(x=20, y=5)

label_tempo = Label(janela, text='00:00:00', font=('Times',50,'bold'),bg=cor1,fg=cor4)
label_tempo.place(x=20,y=30)

# criando Botões---------------------------
botao_iniciar = Button(janela,command=start, text="Iniciar", width=10,height=2,bg=cor1,fg=cor2,font=('Ivy',8,'bold'),relief='raised',overrelief='ridge')
botao_iniciar.place(x=20,y=130)

botao_pausa = Button(janela, command=pausar,text='Pausar', width=10,height=2,bg=cor1,fg=cor2,font=('Ivy',8,'bold'),relief='raised',overrelief='ridge')
botao_pausa.place(x=105,y=130)

botao_reiniciar = Button(janela,command=reiniciar, text="Reiniciar", width=10,height=2,bg=cor1,fg=cor2,font=('Ivy',8,'bold'),relief='raised',overrelief='ridge')
botao_reiniciar.place(x=190,y=130)

janela.mainloop()
