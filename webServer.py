'''
A simple webServer that spins up a Servo
'''
import http.server
import os
import re
import sys
import servoServer

API = re.compile('^/?api/?', re.IGNORECASE)
SERVO = servoServer.Servo()
root = os.path.abspath(os.getcwd())

def main():
    '''
    The main program
    '''
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
    '''
    custom HttpRequestHandler to split to the servo library
    '''
    def do_GET(self):
        '''
        dispatches to api if it starts with /api/ otherwise handles like
        a file server.
        '''
        if (API.match(self.path)):
            self.api()
            return
        else:
            path = self.sanitized_path()
            path = root + path
            print(path)
            if (not os.path.isfile(path)):
                self.send_error(404)
                return
            req_file = open(path, 'r')
            out = bytes(req_file.read(), 'utf-8')
            req_file.close()
            self.send_response(200)
            self.send_header('content-length', len(out))
            self.end_headers()
            self.wfile.write(out)
            return

    def do_POST(self):
        '''
        so I apparently can't grab the POST data so I'm just going to
        ignore this even exists.
        '''
        self.send_error(405)
        return

    def api(self):
        '''
        Handles api calls based off path
        '''
        get_percent = re.compile(r'^/?api/getpercent', re.IGNORECASE)
        set_percent = re.compile(r'^/?api/setpercent\?value=([0-9]+(\.[0-9]+)?)$', re.IGNORECASE)
        val = set_percent.match(self.path)
        if (val != None):
            ival = float(val.group(1))
            SERVO.set_percent(ival)
            self.send_response(204)
            self.end_headers()
        elif (get_percent.match(self.path)):
            ival = SERVO.get_percent()
            self.send_response(200)
            out = bytes(str(ival), 'utf-8')
            self.send_header('content-length', len(out))
            self.end_headers()
            self.wfile.write(out)
        else:
            self.send_error(400)

    def sanitized_path(self):
        '''
        Sanitizes the request path and adds implied index
        '''
        safe = re.sub(r'/\.\./', '/\\.\\./', self.path)
        if (safe == '/'):
            return "/index.html"
        return safe

if (__name__ == "__main__"):
    main()
