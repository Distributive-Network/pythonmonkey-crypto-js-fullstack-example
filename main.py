#!/usr/bin/env python3

import pythonmonkey as pm
require = pm.createRequire(__file__)
aes = require("./aes")

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import time

hostName = "localhost"
hostPort = 9000

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

    elif (self.path.split("?")[0] == '/encrypt'):
      print("encrypting string...")

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
      self.wfile.write(bytes("<html><head><title>AES Encryption</title></head>", "utf-8"))
      self.wfile.write(bytes("<body>", "utf-8"))
      self.wfile.write(bytes(f"the encrypted string is: {cipher}", "utf-8"))
      self.wfile.write(bytes("</body></html>", "utf-8"))
      return

    elif (self.path.split("?")[0] == '/decrypt'):
      print("decrypting string...")

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
      self.wfile.write(bytes("<html><head><title>AES Encryption</title></head>", "utf-8"))
      self.wfile.write(bytes("<body>", "utf-8"))
      self.wfile.write(bytes(f"the decrypted string is: {plain_text}", "utf-8"))
      self.wfile.write(bytes("</body></html>", "utf-8"))
      return

    else:
      self.send_response(404)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      self.wfile.write(bytes("404 not found", "utf-8"))

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))

