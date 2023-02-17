# SocketProgramming

## Server code:

  ### Listens on a specified port for incoming connections, redirects the client's request to the destination server. After receiving the response, it caches it into a dictionary and returns it to the client. If the client makes the same request within 30 seconds he recieves the cached response faster. The code can also handle errors and send them to the client.

## Client Code:
  
  ### This code sends an HTTP request to the proxy server. However, i added some features in which the client can obtain his own physical address, the IPv4 address of the domain and the domain name from an IPv4 address, finaly it can perform a traceroute to a domain.
