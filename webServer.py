import http.server
import io
import os
import re
import servoServer
import sys

API = re.compile('^/?api/?', re.IGNORECASE)
SERVO = servoServer.Servo()
root = os.path.abspath(os.getcwd())

def main():
    global root
    args = sys.argv
    if (len(args) >= 2):
        root = args[1]
    server_address = ('', 80)
    httpd = http.server.HTTPServer(server_address, Dispatch)
    SERVO.set_percent(0)
    print('Starting webserver on port 80. Root: ' + root)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down...')
        httpd.shutdown()
        httpd.server_close()
        print('Shut down.')

class Dispatch(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if (API.match(self.path)):
            self.Api()
            return
        else:
            p = self.sanitized_path()
            p = root + p
            print(p)
            if (not os.path.isfile(p)):
                self.send_error(404)
                return
            f = open(p, 'r')
            out = bytes(f.read(), 'utf-8')
            f.close()
            self.send_response(200)
            self.send_header('content-length', len(out))
            self.end_headers()
            self.wfile.write(out)
            return

    def do_POST(self):
        # although I originally intended for the API to use post, it appears python wants to fight me about reading post data.
        self.send_error(405)
        return

    def Api(self):
        print("API")
        getPercent = re.compile('^/?api/getpercent', re.IGNORECASE)
        setPercent = re.compile('^/?api/setpercent\?value=([0-9]+(\.[0-9]+)?)$', re.IGNORECASE)
        val = setPercent.match(self.path)
        if (val != None):
            ival = float(val.group(1))
            print("set: ", ival)
            SERVO.set_percent(ival)
            self.send_response(204)
            self.end_headers()
        elif (getPercent.match(self.path)):
            ival = SERVO.get_percent()
            print("get: ", ival)
            self.send_response(200)
            out = bytes(str(ival), 'utf-8')
            self.send_header('content-length', len(out))
            self.end_headers()
            self.wfile.write(out)
        else:
            self.send_error(400)
    
    def sanitized_path(self):
        safe = re.sub(r'/\.\./', '/\\.\\./' , self.path)
        if (safe is '/'):
            return "/index.html"
        return safe

if (__name__ == "__main__"):
    main()
