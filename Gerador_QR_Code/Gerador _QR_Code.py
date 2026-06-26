from tkinter import * # type: ignore
from tkinter import Tk, ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import wifi_qrcode_generator.generator
import io
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os
# Paleta de cores
co0 = "#1c1c1c"  # Preto
co1 = "#f5f5f5"  # Branco
co2 = "#4CAF50"  # Verde
co3 = "#283593"  # Azul escuro
co4 = "#212121"  # Cinza escuro
co5 = "#FF7043"  # Laranja
co6 = "#0288D1"  # Azul
co7 = "#26A69A"  # Verde água
co8 = "#37474F"  # Azul acinzentado
co9 = "#ECEFF1"  # Cinza claro
co10 = "#607D8B"  # Azul cinza médio
co11 = "#C5CAE9"  # Azul claro

# Criando a janela principal
janela = Tk()
janela.title("Gerador de QR Code para Wi-Fi")  # Título da janela
janela.geometry('1000x600')  # Dimensões da janela
janela.configure(background=co1)  # Definindo a cor de fundo
janela.resizable(width=False, height=False)  # Desabilitando redimensionamento

# Função para quebrar o texto em várias linhas se necessário
def wrap_text(text, max_width, font_name, font_size, canvas_obj):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        if canvas_obj.stringWidth(current_line + " " + word, font_name, font_size) <= max_width:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word

    lines.append(current_line.strip())
    return lines

# Função para obter o caminho de um recurso relativo ao script
def get_resource_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

# Função para carregar imagens de forma segura e com fallback
def load_image(filename, size=None, mode='RGBA', fallback_color=(200, 200, 200, 255)):
    path = get_resource_path(filename)
    try:
        img = Image.open(path)
    except (FileNotFoundError, OSError):
        if isinstance(size, tuple):
            img = Image.new(mode, size, fallback_color)
        else:
            img = Image.new(mode, (40, 40), fallback_color)
    else:
        if size is not None:
            img = img.resize(size)
    return ImageTk.PhotoImage(img)

# Função para salvar imagem como PDF com fundo e título estilizados
def save_image_as_pdf_with_background(image_path, pdf_path, title, background_color='#FFFFFF', text_color='#000000'):
    # Abrindo a imagem para obter as dimensões
    image = Image.open(image_path)
    image_width, image_height = image.size

    # Dimensões da página
    page_width, page_height = letter

    # Criando o canvas
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Definindo a cor de fundo
    c.setFillColor(HexColor(background_color))
    c.rect(0, 0, page_width, page_height, stroke=0, fill=1)

    # Adicionando o título estilizado
    font_name = "Helvetica-Bold"
    font_size = 32
    c.setFont(font_name, font_size)
    c.setFillColor(HexColor(text_color))
   
    # Quebrando o título em várias linhas, se necessário
    max_width = page_width - 2 * inch  # Margens de 1 polegada de cada lado
    lines = wrap_text(title, max_width, font_name, font_size, c)
   
    y_position = page_height - 1 * inch
    for line in lines:
        c.drawCentredString(page_width / 2, y_position, line)
        y_position -= font_size + 5  # Espaço entre as linhas

    # Calculando a posição para centralizar a imagem
    total_title_height = (font_size + 5) * len(lines)
    y_center = (page_height - image_height - total_title_height) / 2

    # Convertendo imagem para formato RGB e salvando temporariamente
    image = image.convert("RGB")
    temp_image_path = "temp_image.jpg"
    image.save(temp_image_path)

    # Adicionando a imagem
    c.drawImage(temp_image_path, (page_width - image_width) / 2, y_center, width=image_width, height=image_height)

    # Salvando e fechando o canvas
    c.save()

    # Remover a imagem temporária
    import os
    os.remove(temp_image_path)
# Função para atualizar o QR Code
def atualizar_qr_code():
    ssid = e_ssid.get()
    senha = e_senha.get()
    criptografia = selecionado.get()
    hidden = estado_hidden.get()
   
    qr_code = wifi_qrcode_generator.generator.wifi_qrcode(
        ssid=ssid,
        password=senha,
        authentication_type=criptografia,
        hidden=hidden == "Hidden"
    )
   
    img_qr_code = qr_code.make_image()
    buffer = io.BytesIO()
    img_qr_code.save(buffer, format="PNG")
    buffer.seek(0)
   
    qr_img = Image.open(buffer)
    altura = 190
    largura = 190
    qr_img = qr_img.resize((largura, altura))
    qr_img = ImageTk.PhotoImage(qr_img)
   
    image_refs['current_qr'] = qr_img
    app_qr.config(image=image_refs['current_qr'])

    # Salvar a imagem QR Code em um arquivo
    qr_img_file_path = "qr.png"
    img_qr_code.save(qr_img_file_path)

    # Gerar PDF
    gerar_pdf(qr_img_file_path)
# Função para gerar o PDF com fundo e título
def gerar_pdf(image_path):
    title = e_mensagem.get()
    background_color = tela['bg']  # Cor de fundo padrão
    text_color = '#FFFFFF'  # Cor do texto padrão

    pdf_path = "output.pdf"
    save_image_as_pdf_with_background(image_path, pdf_path, title, background_color, text_color)
    messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")

# Função para ajustar cores do fundo
def escala(valor):
    r = s_red.get()
    g = s_green.get()
    b = s_blue.get()
    cor = f'#{r:02x}{g:02x}{b:02x}'
    tela.config(bg=cor)

# Função para limpar campos e restaurar a visualização
def limpar_campos():
    e_ssid.delete(0, END)
    e_senha.delete(0, END)
    selecionado.set(criptografia_options[0])
    estado_hidden.set("Visible")
    e_mensagem.delete(0, END)
    e_mensagem.insert(0, 'Título para o PDF')
    tela.config(bg=co5)
    app_qr.config(image=image_refs['app_img_qr'])

# Frames
frameCima = Frame(janela, width=780, height=100, bg=co1, relief="flat", padx=10, pady=10)
frameCima.grid(row=0, column=0, columnspan=2, sticky=NW)

frameMeio = Frame(janela, width=380, height=300, bg=co9, relief="flat", padx=10, pady=10)
frameMeio.grid(row=1, column=0, sticky=NW)

frameBaixo = Frame(janela, width=380, height=150, bg=co1, relief="flat", padx=10, pady=10)
frameBaixo.grid(row=2, column=0, sticky=NW)

frameDireita = Frame(janela, width=580, height=450, bg=co1, relief="flat", padx=10, pady=10)
frameDireita.grid(row=1, column=1, rowspan=2, sticky=NW)

# Logo e título
app_img = load_image('logo.png', size=(40, 40))

app_logo = Label(frameCima, image=app_img, bg=co1, relief=FLAT)
app_logo.grid(row=0, column=0, padx=10)

app_titulo = Label(frameCima, text='Gerador QR Code Wi-Fi', bg=co1, fg=co0, font=('Arial', 28, 'bold'))
app_titulo.grid(row=0, column=1, padx=10)


# Campos de entrada
l_ssid = Label(frameMeio, text='SSID', font=("Arial", 14), bg=co9)
l_ssid.grid(row=0, column=0, padx=10, pady=10, sticky=W)
e_ssid = Entry(frameMeio, width=20, font=("Arial", 14))
e_ssid.grid(row=0, column=1, padx=10, pady=10)

l_senha = Label(frameMeio, text='Senha', font=("Arial", 14), bg=co9)
l_senha.grid(row=1, column=0, padx=10, pady=10, sticky=W)
e_senha = Entry(frameMeio, width=20, font=("Arial", 14), show='*')
e_senha.grid(row=1, column=1, padx=10, pady=10)

l_criptografia = Label(frameMeio, text='Criptografia', font=("Arial", 14), bg=co9)
l_criptografia.grid(row=2, column=0, padx=10, pady=10, sticky=W)
criptografia_options = ["WPA", "WEP", "None"]
selecionado = StringVar()
selecionado.set(criptografia_options[0])
menu_criptografia = OptionMenu(frameMeio, selecionado, *criptografia_options)
menu_criptografia.config(width=18, font=("Arial", 14))
menu_criptografia.grid(row=2, column=1, padx=10, pady=10)

l_hidden = Label(frameMeio, text='Hidden', font=("Arial", 14), bg=co9)
l_hidden.grid(row=3, column=0, padx=10, pady=10, sticky=W)
estado_hidden = StringVar()
estado_hidden.set("Visible")
menu_hidden = OptionMenu(frameMeio, estado_hidden, "Visible", "Hidden")
menu_hidden.config(width=18, font=("Arial", 14))
menu_hidden.grid(row=3, column=1, padx=10, pady=10)

e_mensagem = Entry(frameMeio, width=30, font=("Arial", 16), justify=CENTER)
e_mensagem.insert(0, 'Título para o PDF')
e_mensagem.grid(row=4, column=0, columnspan=2, pady=10)

# Controles de cor
l_red = Label(frameBaixo, text='Red', width=7, bg=co1, fg='red', anchor='nw', font=("Arial", 12, "bold"))
l_red.grid(row=0, column=0, sticky=NW, padx=10)
s_red = Scale(frameBaixo, from_=0, to=255, length=200, bg=co1, fg="red", orient=HORIZONTAL, command=escala)
s_red.grid(row=0, column=1, sticky=NW, padx=10)

l_green = Label(frameBaixo, text='Green', width=7, bg=co1, fg='green', anchor='nw', font=("Arial", 12, "bold"))
l_green.grid(row=1, column=0, sticky=NW, padx=10)
s_green = Scale(frameBaixo, from_=0, to=255, length=200, bg=co1, fg="green", orient=HORIZONTAL, command=escala)
s_green.grid(row=1, column=1, sticky=NW, padx=10)

l_blue = Label(frameBaixo, text='Blue', width=7, bg=co1, fg='blue', anchor='nw', font=("Arial", 12, "bold"))
l_blue.grid(row=2, column=0, sticky=NW, padx=10)
s_blue = Scale(frameBaixo, from_=0, to=255, length=200, bg=co1, fg="blue", orient=HORIZONTAL, command=escala)
s_blue.grid(row=2, column=1, sticky=NW, padx=10)

# Tela de visualização
tela = Label(frameDireita, bg=co5, width=72, height=24, bd=1)
tela.grid(row=0, column=0, sticky=NW, pady=0)

# Logo e título na tela
app_img_qr = load_image('logo.png', size=(200, 200))
app_qr = Label(frameDireita, image=app_img_qr, bg=co1, relief=FLAT)
app_qr.place(x=155, y=100)

# Manter referências de imagens para evitar descarte e atribuição direta a widgets
image_refs = {
    'app_logo': app_img,
    'app_img_qr': app_img_qr,
}

img_gerar = load_image('gerar.png', size=(24, 24))
img_limpar = load_image('limpar.png', size=(24, 24))
img_sair = load_image('sair.png', size=(24, 24))
image_refs['img_gerar'] = img_gerar
image_refs['img_limpar'] = img_limpar
image_refs['img_sair'] = img_sair

# Frame para botões
frameBotoes = Frame(frameDireita, width=300, height=100, bg=co1, bd=1)
frameBotoes.grid(row=1, column=0, pady=10)

# Estilos dos botões
style = ttk.Style()

# Botão "Gerar"
style.configure("Gerar.TButton", padding=6, relief="flat", background=co2, foreground=co0, font=('Arial', 11, 'bold'))
style.map("Gerar.TButton",
          foreground=[('pressed', co1), ('active', co0)],
          background=[('pressed', '!disabled', co3), ('active', co4)])

# Botão "Limpar"
style.configure("Limpar.TButton", padding=6, relief="flat", background=co5, foreground=co0, font=('Arial', 11, 'bold'))
style.map("Limpar.TButton",
          foreground=[('pressed', co1), ('active', co0)],
          background=[('pressed', '!disabled', co6), ('active', co7)])

# Botão "Sair"
style.configure("Sair.TButton", padding=6, relief="flat", background=co6, foreground=co0, font=('Arial', 11, 'bold'))
style.map("Sair.TButton",
          foreground=[('pressed', co1), ('active', co0)],
          background=[('pressed', '!disabled', co8), ('active', co10)])

# Botão "Gerar QR Code"
bt_gerar = ttk.Button(
    frameBotoes, 
    text='  Gerar QR Code', 
    compound=LEFT, 
    width=13, 
    image=img_gerar, 
    command=atualizar_qr_code,  # Função associada
    style="Gerar.TButton"
)
bt_gerar.grid(row=0, column=0, padx=10)

# Botão "Limpar"
bt_limpar = ttk.Button(
    frameBotoes, 
    text='  Limpar', 
    compound=LEFT, 
    width=12, 
    image=img_limpar, 
    command=limpar_campos,  # Reseta os campos e restaura a visualização
    style="Limpar.TButton"
)
bt_limpar.grid(row=0, column=1, padx=10)

# Botão "Sair"
bt_sair = ttk.Button(
    frameBotoes, 
    text='  Sair', 
    compound=LEFT, 
    width=12, 
    image=img_sair, 
    command=janela.quit,  # Fecha o aplicativo
    style="Sair.TButton"
)
bt_sair.grid(row=0, column=2, padx=10)

janela.mainloop()