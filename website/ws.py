import http.server
import socketserver
import sys
import logging

PORT = 80

Handler = http.server.SimpleHTTPRequestHandler



#logging override
class LoggingRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        logger.info("{0},{1},{2}".format(self.address_string(), self.log_date_time_string(), self.requestline))




logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('./logfile.log')
handler.setLevel(logging.INFO)

# add the handlers to the logger
logger.addHandler(handler)

logger.info("serving at port {0}".format(PORT))
#print("serving at port", PORT)

httpd = socketserver.TCPServer(("", PORT), LoggingRequestHandler)

#buffer = 1
#sys.stderr = open('./logfile.txt', 'w', buffer)
httpd.serve_forever()
