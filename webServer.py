import http.server
import re
import servoServer

DEBUG = True
API = re.compile('^/?api/?', re.IGNORECASE)
SERVO = servoServer.Servo()

def main():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, Dispatch)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        httpd.server_close()

class Dispatch(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if (API.match(self.path)):
            self.send_error(400, "API expects POST", "Api requests must be sent through POST, not GET")
        self.send_response(204)
        self.end_headers()

    def do_POST(self):
        if (API.match(self.path)):
            self.Api()
        self.send_response(204)
        self.end_headers()

    def Api(self):
        getPercent = re.compile('^/?api/getpercent', re.IGNORECASE)
        setPercent = re.compile('^/?api/setpercent', re.IGNORECASE)

def dprint(msg):
    if (DEBUG):
        print(msg)

if (__name__ == "__main__"):
    main()
