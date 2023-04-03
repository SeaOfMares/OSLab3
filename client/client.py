#! /usr/bin/env python3

# Echo client program
import socket, sys, re,os
sys.path.append("..")       # for params
import params


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)
argument = sys.argv
fd = os.open(argument[1] , os.O_RDONLY)
total_bytes = os.path.getsize(argument) #get total amount of bytes
read_bytes = 10
outMessage = os.read(fd, read_bytes)

outMessage = "Hello world!".encode()
while len(outMessage):
    print("sending '%s'" % outMessage.decode())
    bytesSent = s.send(outMessage)
    outMessage = outMessage[bytesSent:]

data = s.recv(1024).decode()
print("Received '%s'" % data)

outMessage = "Hello world!"
while len(outMessage):
    print("sending '%s'" % outMessage)
    bytesSent = s.send(outMessage.encode())
    outMessage = outMessage[bytesSent:]

s.shutdown(socket.SHUT_WR)      # no more output

while 1:
    data = s.recv(1024).decode()
    print("Received '%s'" % data)
    if len(data) == 0:
        break
print("Zero length read.  Closing")
s.close()