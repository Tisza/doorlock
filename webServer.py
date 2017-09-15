import http.server
import io
import os
import re
import servoServer

API = re.compile('^/?api/?', re.IGNORECASE)
SERVO = servoServer.Servo()

def main():
    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, Dispatch)
    SERVO.set_percent(0)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()
        httpd.server_close()

class Dispatch(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if (API.match(self.path)):
            self.Api()
            return
        else:
            p = self.sanitized_path()
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
        safe = safe[1:]
        if (safe is ''):
            return "index.html"
        return safe

if (__name__ == "__main__"):
    main()
