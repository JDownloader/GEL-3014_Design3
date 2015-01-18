
from BaseHTTPServer import BaseHTTPRequestHandler
import SimpleHTTPServer
import json
import SocketServer

PORT = 8000

class WebServer:

    class MyRequestHandler (SimpleHTTPServer.SimpleHTTPRequestHandler) :

        def do_GET(self) :
            if self.path == "/position" :
                me = {  "top": 30, "left": 305}
                #send response code:
                self.send_response(200)
                #send headers:
                self.send_header("Content-type:", "text/html")
                # send a blank line to end headers:
                self.wfile.write("\n")

                #send response:
                json.dump(me, self.wfile)
            else :
                self.path = '/www' + self.path
                f = self.send_head()
                if f:
                    self.copyfile(f, self.wfile)
                    f.close()

    def __init__(self):
        return None

    def start_server(self):
        httpd = SocketServer.TCPServer(("", PORT), self.MyRequestHandler)
        httpd.serve_forever()

    def say_hello(self):
        print "Hello2, World!"