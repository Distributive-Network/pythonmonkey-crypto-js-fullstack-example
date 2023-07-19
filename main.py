#!/usr/bin/env python3
"""
This is a simple fullstack app that allows a user to encrypt and
decrypt arbitrary text.
"""

#
# use PythonMonkey require to require the aes JavaScript module
#
import pythonmonkey as pm
aes = pm.require("./aes")

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import time

hostName = "localhost"
hostPort = 9001

class MyServer(BaseHTTPRequestHandler):
  def do_GET(self):
    parsed_path = urlparse(self.path)
    params = parse_qs(parsed_path.query)

    if (self.path == '/'):
      f = open("./index.html", 'rb')
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      self.wfile.write(f.read())
      f.close()
      return

    # handle requests for encrypting a strign
    elif (self.path.split("?")[0] == '/encrypt'):
      message = params['message'][0]
      key = params['key'][0]

      #
      # aes.encrypt() is a JavaScript function
      #
      cipher = aes.encrypt(message, key)

      # respond with the encrypted string
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      writeHTMLresponse(self.wfile.write, f"The encrypted string is: {cipher}")
      print(cipher)
      return

    # handle requests for decrypting a strign
    elif (self.path.split("?")[0] == '/decrypt'):
      cipher = params['ciphertext'][0]
      key = params['key'][0]

      #
      # aes.decrypt() is a JavaScript function
      #
      plain_text = aes.decrypt(cipher, key)

      # respond with the decrypted string
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      writeHTMLresponse(self.wfile.write, f"The decrypted string is: {plain_text}")
      print(plain_text)
      return

    else:
      self.send_response(404)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      writeHTMLresponse(self.wfile.write, "404 not found")

def writeHTMLresponse(writer, message):
  writer(bytes("<html><head><title>AES Encryption</title></head>", "utf-8"))
  writer(bytes("<body>", "utf-8"))
  writer(bytes(f"{message}", "utf-8"))
  writer(bytes("</body></html>", "utf-8")) 

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server running at http://%s:%s" % (hostName, hostPort))

try:
  myServer.serve_forever()
except KeyboardInterrupt:
  myServer.server_close()

