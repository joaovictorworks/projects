from tkinter import * # type: ignore
from tkinter import Tk, ttk
import os
# importando pillow
from PIL import Image, ImageTk
# importando bibliotecas 
from tkinter import messagebox
import wifi_qrcode_generator.generator
import io
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

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

images = {}

# assets path
assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))

# Criando a janela principal
janela = Tk()
janela.title('Gerador de QR Code para Wi-Fi')
janela.geometry('1000x600')
janela.configure(bg=co1)
janela.resizable(False,False)

# Função para quebrar o texto em várias linhas se necessário
def wrap_text(text, max_width, font_name, font_size, canvas_obj):
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        sep = " " if current_line else ""
        candidate = current_line + sep + word
        if canvas_obj.stringWidth(candidate, font_name, font_size) <= max_width:
            current_line = candidate
        else:
            lines.append(current_line.strip())
            current_line = word

    lines.append(current_line.strip())
    return lines

# Função para salvar imagem como PDF com fundo e título estilizados
def save_image_as_pdf_with_background(image_path, pdf_path, title, background_color='#FFFFFF', text_color='#000000'):
    # Abrindo a imagem para obter as dimensões
    image = Image.open(image_path)
    image_width, image_height = image.size

    # Criando o canvas (o tamanho da página é obtido a partir do canvas)
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Dimensões da página
    page_width, page_height = c._pagesize

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
   
    app_qr.config(image=qr_img)
    images['app_qr'] = qr_img

    # Salvar a imagem QR Code em um arquivo (em assets)
    qr_img_file_path = os.path.join(assets_path, "qr.png")
    img_qr_code.save(qr_img_file_path)

    # Gerar PDF
    gerar_pdf(qr_img_file_path)

# Função para gerar o PDF com fundo e título
def gerar_pdf(image_path):
    title = e_mensagem.get()
    background_color = tela['bg']  # Cor de fundo padrão
    text_color = '#FFFFFF'  # Cor do texto padrão

    pdf_path = os.path.join(assets_path, "output.pdf")
    save_image_as_pdf_with_background(image_path, pdf_path, title, background_color, text_color)
    messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")

# Função para ajustar cores do fundo
def escala(valor):
    r = s_red.get()
    g = s_green.get()
    b = s_blue.get()
    cor = f'#{r:02x}{g:02x}{b:02x}'
    tela.config(bg=cor)

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
app_img = Image.open(os.path.join(assets_path, 'technology.png'))
app_img = app_img.resize((40, 40))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, bg=co1, relief=FLAT)
app_logo.grid(row=0, column=0, padx=10)

app_titulo = Label(frameCima, text='Gerador QR Code Wi-Fi', bg=co1, fg=co0, font=('Arial', 28, 'bold'))
app_titulo.grid(row=0, column=1, padx=10)

# Campos de entrada
l_ssid = Label(frameMeio, text='SSID', font=("Arial", 14), bg=co9)
l_ssid.grid(row=0, column=0, padx=10, pady=10, sticky=W)
... (file continues)
