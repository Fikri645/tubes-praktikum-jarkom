#Kelompok:
#Muhammad Fikri Wahidin (1301213505)
#Rashad Izza Andredi (1301213309)
#Josua Pane (1301210254)
import socket

def parse_request(request):
    # Memecah request menjadi bagian-bagian
    request_parts = request.split()
    file_path = ""
    method = "GET"
    if len(request_parts) != 0:
        # Mengambil method dari request
        method = request_parts[0]
        # Mengambil path file dari request dan menghapus karakter '/' pada awalnya
        file_path = request_parts[1][1:] 
        # Jika path file kosong atau mengandung '...', gunakan 'index.html'
        if file_path == '' or file_path == '...':
            file_path = 'index.html'
    return method, file_path

def create_response(file_path, method):
    if method == 'GET':
        try:
            # Membuka file dengan path yang diberikan
            with open(file_path, 'r') as file:
                # Membaca isi file dan menyusun respons HTTP
                response = f"HTTP/1.1 200 OK\n\n{file.read()}"
                print(f"File {file_path} terbuka")
        except FileNotFoundError:
            # Jika file tidak ditemukan, kirim respons '404 Not Found'
            response = "HTTP/1.1 404 Not Found\n\n404 Not Found"
            print(f"File {file_path} Tidak Ditemukan")
    else:
        # Jika metode bukan 'GET', kirim respons '405 Method Not Allowed'
        response = "HTTP/1.1 405 Method Not Allowed\n\n405 Method Not Allowed"
    return response

def run_web_server(host, port):
    # Membuat socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Mengikat socket ke alamat host dan port tertentu
    server_socket.bind((host, port))
    # Mendengarkan koneksi yang masuk dengan batasan antrian sebesar 1
    server_socket.listen(1)
    print(f"Server berjalan di http://{host}:{port}")

    while True:
        # Menerima koneksi dari client
        client_socket, client_address = server_socket.accept()
        print(f"Koneksi diterima dari {client_address}")

        # Menerima data dari client (request)
        request = client_socket.recv(1024).decode()
        # Memecah request menjadi metode dan path file
        method, file_path = parse_request(request)
        # Membuat respons HTTP berdasarkan path file dan metode
        response = create_response(file_path, method)

        # Mengirim respons ke client
        client_socket.sendall(response.encode())
        # Menutup koneksi dengan client
        client_socket.close()
        
# Menjalankan server web dengan host 'localhost' dan port 7070
run_web_server("localhost", 7070)


