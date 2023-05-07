import socket, os

def parse_request(request):
    # Mem-parse HTTP request
    request_parts = request.split()
    file_path = ""
    method = "GET"
    if len(request_parts) != 0:
        method = request_parts[0]
        file_path = request_parts[1][1:]  # menghilangkan leading slash '/'
        if file_path == '' or file_path == '...':
            file_path = 'index.html'
    return method, file_path


def create_response(file_path, method):
    if method == 'GET':
        # Mencari file yang diminta oleh client
        print(f"File {file_path} terbuka")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                # Membuat response message dengan header HTTP dan konten file yang diminta
                response = f"HTTP/1.1 200 OK\n\n{file.read()}"
        else:
            # Membuat response message dengan pesan '404 Not Found'
            response = "HTTP/1.1 404 Not Found\n\n404 Not Found"
    else:
        # Membuat response message dengan pesan '405 Method Not Allowed'
        response = "HTTP/1.1 405 Method Not Allowed\n\n405 Method Not Allowed"
    return response


def run_web_server(host, port):
    # Membuat socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Mengikat socket ke alamat dan port tertentu
    server_socket.bind((host, port))
    # Menerima koneksi dari client
    server_socket.listen(1)
    print(f"Server berjalan di http://{host}:{port}")

    while True:
        # Menerima koneksi dari client
        client_socket, client_address = server_socket.accept()
        print(f"Koneksi diterima dari {client_address}")
        # Menerima request dari client
        request = client_socket.recv(1024).decode()
        # print(f"Request:\n{request}")
        method, file_path = parse_request(request)
        response = create_response(file_path, method)
        # Mengirimkan response message ke client
        client_socket.sendall(response.encode())
        client_socket.close()


# Menjalankan web server dengan host "localhost" dan port 8080
run_web_server("localhost", 8080)

