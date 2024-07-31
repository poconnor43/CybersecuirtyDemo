# gives us all of our low level port and domain accsess
import socket

def whois_lookup(domain:str):
    # makig a TCP socket request between the two different codes
    s =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect on the website to port 43
    s.connect(("whois.iana.org",43))
    s.send(f"{domain}\r\n".encode())
    #gets our response with a buffer
    response = s.recv(4096).decode()
    s.close()
    return response

#example/ unofficial test
#print(whois_lookup("google.com"))