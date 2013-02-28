import SocketServer

# Step 1: Hello World
class HelloWorldHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    self.wfile.write('Hello world!')

# server = SocketServer.TCPServer(('localhost', 12345), HelloWorldHandler)
# server.serve_forever()


# Step 2: echo
class EchoHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    data = self.rfile.readline()
    print "Got: ", data
    self.wfile.write(data)
    print "Sent: ", data


server = SocketServer.TCPServer(('localhost', 12345), EchoHandler)
server.serve_forever()



# Step 3: guess a number
import random

class NumberHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    number = random.randint(1,5)
    self.wfile.write("Guess a number between 1 and 5!\n")
    data = self.rfile.readline()
    print "Got: ", data
    self.wfile.write("You guessed: %s\n" % data)
    # Do the strip change on the fly
    if data.strip() == str(number):
      self.wfile.write("You got it!\n")
    else:
      self.wfile.write("But it was %s\n" % number)


# server = SocketServer.TCPServer(('localhost', 12345), NumberHandler)
# server.serve_forever()


# Step 4: WebServer
class WebServerHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    request = self.rfile.readline()
    method, theFile, other = request.split()
    print "Get the file: %s" % theFile
    relativeFile = theFile[1:]
    response = open(relativeFile).read()
    self.wfile.write(response)



server = SocketServer.TCPServer(('localhost', 12345), WebServerHandler)
server.serve_forever()
