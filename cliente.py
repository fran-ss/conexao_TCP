import socket
import tkinter as tk
from tkinter import filedialog, Label

from PIL import Image, ImageTk
import io
import pickle


def exibir_imagem(image_path):
    image = Image.open(image_path)
    image.thumbnail((300, 300))  # Ajuste o tamanho da imagem conforme necessário
    photo = ImageTk.PhotoImage(image)  # Use ImageTk para criar a imagem exibível

    imagem_label.config(image=photo)
    imagem_label.photo = photo  # Mantém uma referência à imagem para evitar a coleta de lixo
    imagem_label.place(x=30, y=260)  # posiciona a imagem na tela


def enviar_imagem():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    exibir_imagem(file_path)  # Exibe a imagem selecionada na interface

    image: Image = Image.open(file_path)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    image_data = image_bytes.getvalue()
    client_socket.send(image_data)

    info_bytes = client_socket.recv(1024)
    image_info = pickle.loads(info_bytes)

    tamanho_label.config(text=f"Tamanho da imagem: {image_info['tamanho']}")
    tipo_label.config(text=f"Tipo da imagem: {image_info['tipo']}")
    cores_label.config(text=f"Cores da imagem: {', '.join(image_info['cores'])}")

    client_socket.close()


HOST = '10.24.31.146'
PORT = 12345

root = tk.Tk()
root.geometry("700x600")
root.title("Cliente")
# ---------------

root.configure(background='#FFCD72')

labelInicial = Label(root, text="ImageAnalyzer", font="Georgia 30 ", bg='#FFCD72')
labelInicial.place(x=220, y=20)

labelInicial = Label(root, text="Aqui voce pode analisar o tamanho , cores e o tipo da sua imagem!", font="Georgia 13 ",
                     bg='#FFCD72')
labelInicial.place(x=90, y=90)

# --------------


enviar_button = tk.Button(root, text="Enviar Imagem ", font='Georgia 12', width=30, background='#F98023',
                          command=enviar_imagem)

enviar_button.place(x=205, y=200)

tamanho_label = Label(root, text="", font=("Georgia 12"), bg='#FFCD72')
tamanho_label.place(x=340, y=330)
tipo_label = Label(root, text="", font=("Georgia 12"), bg='#FFCD72')
tipo_label.place(x=340, y=360)
cores_label = Label(root, text="", font=("Georgia 12"), bg='#FFCD72')
cores_label.place(x=340, y=390)
imagem_label = tk.Label(root, background='#FFCD72')
imagem_label.place(x=340, y=420)

root.mainloop()