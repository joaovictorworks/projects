import tkinter as tk
from tkinter import Frame, Label, Entry, Button, CENTER, NSEW, RAISED, END
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from PIL import Image

# Cores ---------------------- 
co0 = "#000000"  # black
co1 = "#cc1d4e"  # red
co2 = "#feffff"  # white
co3 = "#0074eb"  # blue
co6 = "#d9d9d9"  # grey

janela = tk.Tk()
janela.title("Compressor de Imagem")
janela.geometry('420x340') 
janela.config(bg=co2)
janela.resizable(width=False, height=False)

# ISSO CORRIGE O DESALINHAMENTO: Força a janela a centralizar o frame principal
janela.columnconfigure(0, weight=1)
janela.rowconfigure(0, weight=1)

img_original = None 

# --- Funções ---

def selecionar_arquivo():
    global img_original
    
    ficheiro = askopenfilename(filetypes=[("Imagens", "*.jpg;*.jpeg;*.png;*.bmp")])
    
    if not ficheiro:
        return
        
    try:
        img_original = Image.open(ficheiro)
        largura_orig, altura_orig = img_original.size
        
        tamanho_original.config(text=f'Original: {largura_orig}x{altura_orig}')
        mostrar_campos()
        
        entrada_largura.delete(0, END)
        entrada_altura.delete(0, END)
        
    except Exception as e:
        messagebox.showerror('Erro', f'Não foi possível abrir a imagem.\n{e}')

def calcular_altura_automatica(event=None):
    if img_original is None:
        return
        
    try:
        largura_digitada = int(entrada_largura.get())
        largura_orig, altura_orig = img_original.size
        
        nova_altura = int((largura_digitada / largura_orig) * altura_orig)
        
        entrada_altura.delete(0, END)
        entrada_altura.insert(0, str(nova_altura))
    except ValueError:
        entrada_altura.delete(0, END)

def converter_e_salvar():
    if img_original is None:
        return

    try:
        largura = int(entrada_largura.get())
        altura = int(entrada_altura.get())
        
        nova_img = img_original.resize((largura, altura))
        
        local_salvar = asksaveasfilename(
            defaultextension=".jpg", 
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
        )
        
        if local_salvar:
            nova_img.save(local_salvar)
            messagebox.showinfo('Sucesso', 'A imagem foi convertida com sucesso!')
            esconder_campos()
            
    except ValueError:
        messagebox.showerror('Erro de Entrada', 'Por favor, digite apenas números inteiros.')
    except Exception as e:
        messagebox.showerror('Erro', f'Ocorreu um erro ao salvar:\n{e}')

def mostrar_campos():
    tamanho_original.grid(row=2, column=0, columnspan=2, sticky=NSEW, pady=10)
    nova_largura_lbl.grid(row=3, column=0, sticky=NSEW, pady=5)
    nova_altura_lbl.grid(row=3, column=1, sticky=NSEW, pady=5)
    entrada_largura.grid(row=4, column=0, pady=5, padx=10)
    entrada_altura.grid(row=4, column=1, pady=5, padx=10)
    # Botão de converter centralizado sem sticky
    b_converter.grid(row=5, column=0, columnspan=2, pady=20) 

def esconder_campos():
    tamanho_original.grid_remove()
    nova_largura_lbl.grid_remove()
    nova_altura_lbl.grid_remove()
    entrada_largura.grid_remove()
    entrada_altura.grid_remove()
    b_converter.grid_remove()


# --- Interface Gráfica (Layout) ---

frame = Frame(janela, bg=co2, relief='flat')
frame.grid(row=0, column=0, sticky=NSEW)

# Garante que as duas colunas do frame tenham exatamente o mesmo tamanho interno
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

app_nome = Label(frame, text='Compressor de Imagem', anchor=CENTER, pady=15, font=('Courier', 18, 'bold'), bg=co2, fg=co0)
app_nome.grid(row=0, column=0, columnspan=2, sticky=NSEW)

# BOTÃO CORRIGIDO: Sem sticky=NSEW e com largura fixa (width=22) para ficar perfeitamente centralizado
b_novo = Button(frame, text='+ Selecionar Imagem', width=22, command=selecionar_arquivo, font=('Courier', 11, 'bold'), relief=RAISED, bg=co3, fg=co2, cursor="hand2")
b_novo.grid(row=1, column=0, columnspan=2, pady=10)

# Elementos ocultos
tamanho_original = Label(frame, text='', font=('Courier', 12, 'bold'), bg=co2, fg=co3)
nova_largura_lbl = Label(frame, text='Nova Largura (px)', font=('Courier', 10, 'bold'), bg=co2, fg=co0)
nova_altura_lbl = Label(frame, text='Nova Altura (px)', font=('Courier', 10, 'bold'), bg=co2, fg=co0)

entrada_largura = Entry(frame, width=12, justify='center', font=('Courier', 11), highlightbackground=co6, highlightthickness=1)
entrada_largura.bind('<KeyRelease>', calcular_altura_automatica) 

entrada_altura = Entry(frame, width=12, justify='center', font=('Courier', 11), highlightbackground=co6, highlightthickness=1)

b_converter = Button(frame, text='Converter e Salvar', width=22, command=converter_e_salvar, font=('Courier', 11, 'bold'), relief=RAISED, bg=co1, fg=co2, cursor="hand2")

janela.mainloop()
