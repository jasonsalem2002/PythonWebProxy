# SocketProgramming

## Server code:

  ### Listens on a specified port for incoming connections, redirects the client's request to the destination server. After receiving the response, it caches it into a dictionary and returns it to the client. If the client makes the same request within 30 seconds he recieves the cached response faster. The code can also handle errors and send them to the client. 

## Client Code:
  
  ### This code sends an HTTP request to the proxy server. However, i added some features in which the client can obtain his own physical address, the IPv4 address of the domain and the domain name from an IPv4 address, finaly it can perform a traceroute to a domain.

## Sources used:

### [Socket Library](https://docs.python.org/3/library/socket.html)
### [UUID Library](https://docs.python.org/3/library/uuid.html)
### [SubProcess Library](https://docs.python.org/3/library/subprocess.html)
### [DateTime Library](https://docs.python.org/3/library/datetime.html)
### [Threading Library](https://docs.python.org/3/library/threading.html)
### [SYS Library](https://docs.python.org/3/library/sys.html) 
### Used [Geek for Geeks](https://www.geeksforgeeks.org/creating-a-proxy-webserver-in-python-set-1/) to understand how the code should be written.
### [StackOverFlow](https://stackoverflow.com/questions/73522096/why-is-the-proxy-not-working-when-sending-requests) to search for known errors.

# Output
![This is an image](https://github.com/jasonsalem2002/PythonWebProxy/blob/main/Output/OutputClientServer.png)
