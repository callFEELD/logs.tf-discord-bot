from threading import Thread

import http.server
import socketserver

# defines a custom Handler for the Webserver to process the GET and PIOST requests
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        print("post request")

        self.send_response(200)
        self.send_header(b'Content-type', "text/plain")
        self.end_headers()
        self.wfile.write(toSend)

def webserver():
    PORT = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


def run():
    # Running start essentials
    thread1 = Thread(target = webserver, args = ( ))
    thread1.start()