import socket, datetime, threading, time, ssl

cache = {}  # global variable for storing cached responses
cache_expiry_time = 30  # cache expiry time in seconds
BLACKLIST = ['info.cern.cgh', '188.184.21.107']


def printIP(website_ip):
    # Function prints the website url with its public IPv4 address
    print("Client is trying to access: ", website_ip, "IPv4 address:", socket.gethostbyname(website_ip))


def requestParser(cs):
    # Receive the connection and decodes it then stores it into a request variable
    # get the hostname ip by splitting the request and returns both the request and ip
    req = cs.recv(4096).decode()
    hostname_ip = req.split("\n")[1].split(":")[1].strip()
    return hostname_ip, req


def TCP(machineIP, port):
    # Creates a socket for the proxy server and tries to bind it
    # Prints an error with socket, then exits
    proxyS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        proxyS.bind((machineIP, port))
        proxyS.listen(5)  # allow up to 5 connection before refusing new ones
    except socket.error as e:
        print(f"\033[91mError: {e}\033[0m")
        exit()
    return proxyS


def send_recv_data(hostname_socket, hostname_ip, c_req, client_socket):
    # Connects to the destination and sends the request
    # Decode the response and send the encoded version back to the client
    # Cache the response in the dictionary and starts the timer
    # Handles errors of sockets
    try:
        hostname_socket.connect((hostname_ip, 80))
        hostname_socket.send(c_req.encode())
        response = hostname_socket.recv(4096).decode()
        client_socket.send(response.encode())
        cache[hostname_ip] = (response, time.time())
    except socket.gaierror as e:
        send_error_response(client_socket, f"Name resolution error: {e}")

    except socket.error as e:
        send_error_response(client_socket, f"Connection error: {e}")


def send_error_response(client_socket, error_message):
    print(f"\033[91mError connecting to destination server: {error_message}\033[0m")
    error_response = "Error connecting to destination server. Try again later.".encode()
    if error_message is str: # problem with sending a string to client
        error_response = error_message.encode()
    client_socket.send(error_response)


def print_request(client_address):
    # Store the time in a variable and prints in bold
    current_time = datetime.datetime.now().strftime("%F %T")
    print(f"Received request from \033[1;31m{client_address}\033[0m at \033[1m{current_time}\033[0m")


def handle_request(client_socket):
    # Most of this function calls other functions check the details of each function individually
    hostname_ip, c_req = requestParser(client_socket)
    printIP(hostname_ip)
    if hostname_ip in BLACKLIST:
        send_error_response(client_socket, "Access to this website is blocked.")
    else:
        if hostname_ip in cache:
            # if the response is already cached, send it to the client
            response, timestamp = cache[hostname_ip]
            if (time.time() - timestamp) < cache_expiry_time:
                client_socket.send(response.encode())
                client_socket.close()
                return
        hostname_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            send_recv_data(hostname_socket, hostname_ip, c_req, client_socket)
            client_socket.close()
        except Exception as e:
            send_error_response(client_socket, e)
            hostname_socket.close()


def server(ip, port):
    # Initialize the server and announce the listening ip and port
    proxyS = TCP(ip, port)
    print(f'Server is listening on \033[1;4;31m{ip}:\033[1;4;31m{port}\033[0m')
    # Create an infinite loop to ensure server is always up and listening for new connections
    while True:
        print("Listening for incoming connections...")
        client_socket, client_address = proxyS.accept()
        print_request(client_address)
        threading.Thread(target=handle_request, args=(client_socket,)).start()


if __name__ == '__main__':
    while True:
        try:
            port = int(input("Please choose the desired port between 1024 and 65535): "))
            if not 1024 <= port <= 65535:
                print("Invalid port number. Please choose a port between 1024 and 65535.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")
    print("\033[91m" + "WARNING: Don't forget to match the IPv4 and port number for the client" + "\033[0m")
    server(str(socket.gethostbyname(socket.gethostname())), port)
