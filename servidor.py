import socket
import pickle
from PIL import Image
import io


HOST = ''  # Endereço IP do servidor
PORT = 12345       # Porta a ser usada


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_socket.bind((HOST, PORT))


server_socket.listen()

print(f"Servidor escutando em {HOST}:{PORT}")


client_socket, client_address = server_socket.accept()

print(f"Conexão recebida de {client_address}")


image_data = client_socket.recv(1024)
image_data += client_socket.recv(1024)

#
image = Image.open(io.BytesIO(image_data))


image_info = {
    "tamanho": image.size,
    "tipo": image.format,
    "cores": image.getbands()
}


info_bytes = pickle.dumps(image_info)
client_socket.send(info_bytes)


client_socket.close()