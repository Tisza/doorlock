import http.server
import io
import re
import servoServer

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
            self.Api()
        else:
            super(Dispatch, self).do_GET()

    def do_POST(self):
        # although I originally intended for the API to use post, it appears python wants to fight me about reading post data.
        self.send_error(405)

    def Api(self):
        print("API")
        getPercent = re.compile('^/?api/getpercent', re.IGNORECASE)
        setPercent = re.compile('^/?api/setpercent\?value=([0-9]+(\.[0-9]+)?)$', re.IGNORECASE)
        val = setPercent.match(self.path)
        if (val != None):
            ival = float(val.group(1))
            print(ival)
            SERVO.set_percent(ival)
            self.send_response(204)
            self.end_headers()
        elif (getPercent.match(self.path)):
            print("GET!")
        else:
            self.send_error(400)

if (__name__ == "__main__"):
    main()
