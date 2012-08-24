# Server and Networking Basics

Today we're going to learn about how computers on the internet talk to each other.
We're going to do that by building programs that work just like those you interact
with on the web do.

If you'd like to follow along, or move ahead, the lesson plan can be
found [here](https://github.com/kevinclark/Lesson-Plans/blob/master/networking/servers.md).

First, some prerequisites. You'll need a text editor and python.


#### Windows

Download and install **Notepad++**
* [http://download.tuxfamily.org/notepadplus/6.1.3/npp.6.1.3.Installer.exe](http://download.tuxfamily.org/notepadplus/6.1.3/npp.6.1.3.Installer.exe)

Download and run the python 2.7 installer from
http://www.python.org/ftp/python/2.7.3/python-2.7.3.msi

After running the installer:

1. Choose 'Install for all users', and click Next.
2. Leave the default directory selected 'C:\Python27\', and click Next.
3. Leave all options selected, and click Next.
4. Click Yes if you get a User Account Control prompt asking for
   permission to install software.
5. Click Finish
6. Click Yes to restart your computer.


#### Mac OSX

Download and open **Text Wrangler**
* http://ash.barebones.com/TextWrangler_4.0.1.dmg

Mac OSX has python built in.



### How Computers Talk

Computers communicate a lot like people do. When one computer needs to
talk to another, it needs to know where to reach it - like an address or
a phone number. After it's able to reach the computer it wants to talk
to, they communicate in whatever language they both know. The fancy word
for that is 'protocol', but don't worry about remembering it. It's not
important for the lesson.

Computers have addresses that are a series of numbers. For example,
'127.0.0.1' is the address for if you want to talk to the computer you're
working on. Because remembering lots of numbers is a little complicated,
we instead use names, and our computers essentially use a big phonebook
called 'DNS' to turn those names into numbers. For example, 'localhost'
is another name for the computer you're working on. It's the same as
'127.0.0.1'.

When you have a computer's address, you can find it. But a computer is
sort of like a hotel - there are lots of places programs can be waiting
to talk, and each of those places has a number. We call them 'ports'. So
to talk to a specific program on a specific computer, we need both the
address, and the port.

With all that in mind, we're going to write a very simple server. A
server is just a name for a program that sits on a computer waiting to
interact with something.


# First Server - Hello World!

Open your text editor, and create and save a new file called 'hello.py'.
In it, write this (we'll talk about it in just a moment):

```python
import SocketServer

class HelloWorldHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    self.wfile.write('Hello world!')

server = SocketServer.TCPServer(('localhost', 12345), HelloWorldHandler)
server.serve_forever()
```

Before we talk about it, go ahead and run it. You can do this on OS X by
opening the Terminal (use spotlight) and typing 'python hello.py'. On
windows, you should be able to double click the file, or go to the
command prompt (Run -> cmd) and typing 'python hello.py'.

You may be prompted to allow a local server to run by the windows
firewall. In that case:

1. Hit start, type 'windows firewall', and choose 'Windows Firewall' or 'Windows Firewall with Advanced Security'.
2. Click 'Advanced Settings' in the left pane.
3. Click 'Inbound Rules' in the left pane, then 'Create a new inbound rule' in the right pane.
4. Select 'Port', then 'TCP', and enter port 12345.
5. Click Next, then Next again, and Next for a third time.
6. Name the rule 'CoderDojo Tic-tac-toe'
7. Click finish.


Now that it's running, let's connect to it and see what it does. Point
your browser at http://localhost:12345 and see what happens.

You should see 'Hello world!' on the screen. So here's what's happening
in the code:

`import SocketServer` is how we load pre-existing code in python that
will help us write our server.

Everything from `class HelloWorldHandler` until we stop indenting is us
telling the computer what it's supposed to do when it encounters a new
connection. So we say 'to handle a new connection, write "Hello world!"
to something called wfile'. `wfile` is the way we send things across the
connection.

In the next line, `server = SocketServer.TCPServer(('localhost', 12345), HelloWorldHandler)`,
we tell python to create a new server, listening on our machine
(localhost) on port 12345. When it gets a connection, it's going to use
`HelloWorldHandler` to process it.

So when our web browser connects to the server, the server sends back
'Hello world!', and we see it on our screen.


### Two Way Communication - Echo

At this point we've got one way communication, but we'd like to be able
to do a bit of the talking. So let's change it so we send something and
it repeats it back to us. To do this, you can open a new file 'echo.py'
and type this in, or modify 'hello.py' to look like this - whichever you
prefer. We'll essentially be changing the class name, and adding lines
to 'handle'.


```python
import SocketServer

class EchoHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    data = self.rfile.readline()
    self.wfile.write(data)


server = SocketServer.TCPServer(('localhost', 12345), EchoHandler)
server.serve_forever()
```

This time, we're grabbing any data sent with `data = self.rfile.readline()`
before writing that data back to whoever we're talking with. So go ahead
and point your web browser to 'localhost:12345' again, and see what
happens.

I see 'GET / HTTP/1.1'. This is what my web browser sends when it
connects to something. This is the way it interacts. That's neat to see,
but we'd like to send something of our own. So if you're on windows,
open putty and point it at localhost and port 12345. Make sure you
select telnet. If you're on OS X, open the terminal (use spotlight) and
type `telnet localhost 12345`.

The screen is going to sit there now, waiting for you to do something.
Type in something and hit enter.

Now our server repeats what I'm sending. Telnet is a simple way to
connect to a server and be able to send things to it by hand. It can be
fun to explore with it. In fact, if you connect to www.google.com on port 80
and send the line we saw earlier, 'GET / HTTP/1.1', you'll see it send
you the html that makes up it's frontpage.

[Then I demo that]

So, the big thing to recognize here is that there's nothing special
about how a web browser communicates - it's just like us opening a
connection with telnet, but much much faster.


### Persistent Two Way Communication - Guessing Game

Now that we can communicate back and forth, let's make it a little more
interactive. Let's write a really simple number guessing game. Just like
before, make a new file and copy this in, or modify your current file to
look like this:

```python
import SocketServer
import random

class NumberHandler(SocketServer.StreamRequestHandler):
  def handle(self):
    number = random.randint(1,5)
    self.wfile.write("Guess a number between 1 and 5!\n")
    data = self.rfile.readline()
    self.wfile.write("You guessed: %s\n" % data)
    if data == str(number):
      self.wfile.write("You got it!\n")
    else:
      self.wfile.write("But it was %s\n" % number)


server = SocketServer.TCPServer(('localhost', 12345), NumberHandler)
server.serve_forever()
```

### TODO - Explain number server

So we'll need to strip that newline away. We can do that with the
'strip' method. Change `if data == str(number)` to `if data.strip() == str(number)`.

Now try it again and it works.


### Our first Web Server

### TODO - Explain web server

```python
import SocketServer

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
```
