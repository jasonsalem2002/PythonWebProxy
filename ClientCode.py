import datetime, socket, uuid, sys, subprocess


# Get the MAC address of the host
def get_mac_address():
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
    return mac_address


# Send an HTTP request to a server
def send_request(ip, port, website_ip):
    # Get the current time for calculating the round-trip time later
    start_time = datetime.datetime.now()
    # Create a client socket and attempt to connect to the specified IP address and port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((ip, port))
        except socket.error as e:
            print(f"\033[31mError: {e}\033[0m")
            return
        # Create a GET request to send to the proxy server, with the Host header set to the website's IP address
        request = f"GET / HTTP/1.1\r\nHost: {website_ip}\r\n\r\n"
        client_socket.send(request.encode())
        print(f"Connection successfully established with the server at \033[0m{ip}:{port}\033[0m")
        print(f"Request sent to proxy server at \033[0m{datetime.datetime.now():%Y-%m-%d %H:%M:%S}\033[0m")
        response = ""
        while True:
            data = client_socket.recv(4096).decode()
            if not data:
                break
            response += data
        # Get the current time again to calculate the round-trip time
        end_time = datetime.datetime.now()
        print(f"Response received from proxy server at \033[0m{end_time:%Y-%m-%d %H:%M:%S}\033[0m")
        print(f"Response: \n{response}")
        print(f"Round-trip time: {end_time - start_time}")
        print(f"Physical MAC address: \033[0m{get_mac_address()}\033[0m")


# Print the main menu of options for the user
def print_menu():
    print("1. Get IPv4 address of a domain")
    print("2. Get domain name of an IPv4 address")
    print("3. Trace Route to a domain")
    print("4. Get the MAC address of the host")
    print("5. Send an HTTP request to a website")
    print("6. Exit")


# Get the IP address of a domain
def get_ip_from_domain(domain):
    ip = socket.gethostbyname(domain)
    print(f"\033[0mThe IP address of \033[33m{domain}\033[0m is \033[32m{ip}\033[0m")


# Get the domain name of an IP address
def get_ip_from_domain(domain):
    ip = socket.gethostbyname(domain)
    print(f"\033[0mThe IP address of \033[33m{domain}\033[0m is \033[32m{ip}\033[0m")

# Get the domain name from an IP address
def get_domain_from_ip(ip):
    try:
        domain = socket.gethostbyaddr(ip)
        print(f"\033[0mThe domain name of \033[33m{ip}\033[0m is \033[32m{domain[0]}\033[0m")
    except socket.herror as e:
        print(f"\033[31mError: {e}\033[0m")


# Takes a domain name as input and uses the `subprocess` library to perform a traceroute to the domain.
# It then prints the results of the traceroute.
def get_traceroute(domain):
    try:
        process = subprocess.Popen(['tracert', domain], stdout=subprocess.PIPE)
        print(f"\033[0mTracing route to \033[33m{domain}\033[0m...")
        while True:
            output = process.stdout.readline().decode()
            if not output:
                break
            print(output.strip())
    except subprocess.CalledProcessError as e:
        print(f"\033[31mError: {e}\033[0m")


# Prompts the user for an IP address, port, and website name, and then calls the `send_request`
# function to send an HTTP request to the website through the specified proxy server.
def send_http_request():
    ip = input("Enter proxy server IP address: ")
    port = int(input("Enter proxy server port: "))
    website = input("Enter website name: ")
    send_request(ip, port, website)


# Main function of the program. It runs in a loop and presents a menu of options to the user. Depending
# on the user's input, it calls one of the other functions to perform a network-related task, or exits the program.
def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            domain = input("Enter domain name: ")
            get_ip_from_domain(domain)
        elif choice == "2":
            ip = input("Enter IP address: ")
            get_domain_from_ip(ip)
        elif choice == "3":
            domain = input("Enter domain name: ")
            get_traceroute(domain)
        elif choice == "4":
            print(f"\033[0mPhysical MAC address: \033[32m{get_mac_address()}\033[0m")
        elif choice == "5":
            send_http_request()
        elif choice == "6":
            print("Exiting program...")
            sys.exit(0)
        else:
            print(f"\033[31mInvalid choice, please enter a valid option number\033[0m")


if __name__ == '__main__':
    main()
