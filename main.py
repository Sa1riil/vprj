#!/usr/bin/env python
import os
import pickle
from base64 import b64decode,b64encode
from binascii import hexlify, unhexlify
from os import popen
from lxml import etree
import cgi,cPickle
from Crypto.Cipher import AES
from Crypto import Random


from flask import Flask, request, make_response, render_template_string


app = Flask(__name__)

# Config stuff
KEY=Random.new().read(32) # 256 bit key for extra security!!!
BLOCKSIZE=AES.block_size
ADMIN_SECRET=Random.new().read(32) # need to keep this secret
APP_NAME = 'SLA 410 - cybersec curs: Gabriel si Iurie'

CONFIG = {
    'encrypto_key' : b64encode(KEY),
    'secret_admin_value' : b64encode(ADMIN_SECRET),
    'app_name' : APP_NAME,
}


def unpad(value, bs=BLOCKSIZE):
   pv = ord(value[-1])
   if pv > bs:
      raise Exception('Bad padding')
   padding = value[-pv:]
   if len(padding) != pv or len(set([a for a in padding])) != 1:
      raise Exception('Bad padding')
   return value[:-pv]


def pad(value, bs=BLOCKSIZE):
   pv = bs - (len(value) % bs)
   return value + chr(pv) * pv


def encrypt(value, key):
   iv = Random.new().read(BLOCKSIZE)
   cipher = AES.new(key, AES.MODE_CBC, iv)
   padded_value = pad(value)
   return iv + cipher.encrypt(padded_value)


def decrypt(value, key):
   iv = value[:BLOCKSIZE]
   decrypt_value = value[BLOCKSIZE:]
   cipher = AES.new(key, AES.MODE_CBC, iv)
   decrypted = cipher.decrypt(decrypt_value)
   return unpad(decrypted)



def rp(command):
    return popen(command).read()


@app.route('/')
def index():
    return """
    <html>
    <head><title>Vulnerable Flask App: """ + CONFIG['app_name'] +"""</title></head>
    <body>
        <p><h3>Functions</h3></p>
        <a href="/cookie">Set and get cookie value</a><br>
        <a href="/lookup">Do DNS lookup on address</a><br>
        <a href="/evaluate">Evaluate expression</a><br>
        <a href="/sayhi">Receive a personalised greeting</a><br>
    </body>
    </html>
    """
        #<a href="/xml">Parse XML</a><br>
        #<a href="/config">View some config items</a><br>

# code injection
@app.route('/evaluate', methods = ['POST', 'GET'])
def evaluate():
    expression = None
    if request.method == 'POST':
        expression = request.form['expression']
        if expression == "'" or expression == '"' or expression == '""' or expression == "''":
           return """
           <html>
               <body>""" + "Result: Introduceti doar numere pentru a face calcule." + """
               </body>
            </html>
            """
    return """
    <html>
       <body>""" + "Result: " + (str(eval(expression)).replace('\n', '\n<br>')  if expression else "") + """
          <form action = "/evaluate" method = "POST">
             <p><h3>Enter expression to evaluate</h3></p>
             <p><input type = 'text' name = 'expression'/></p>
             <p><input type = 'submit' value = 'Evaluate'/></p>
          </form>
       </body>
    </html>
    """



# command injection
@app.route('/lookup', methods = ['POST', 'GET'])
def lookup():
   address = None
   if request.method == 'POST':
      address = request.form['address']
      if ";" in address or "&" in address:
         return """
         <html>
            <body>""" + "Result:\n<br>If you try any other tricks, the session will be stopped.\n" + """
            </body>
         </html>
         """
   return """
   <html>
      <body>""" + "Result:\n<br>\n" + (rp("nslookup " + address).replace('\n', '\n<br>')  if address else "") + """
         <form action = "/lookup" method = "POST">
            <p><h3>Enter address to lookup</h3></p>
            <p><input type = 'text' name = 'address'/></p>
            <p><input type = 'submit' value = 'Lookup'/></p>
         </form>
      </body>
   </html>
   """
    
# deserialisation vulnerability
@app.route('/cookie', methods = ['POST', 'GET'])
def cookie():
    cookieValue = None
    value = None
    
    if request.method == 'POST':
        cookieValue = request.form['value']
        value = cookieValue
    elif 'value' in request.cookies:
        cookieValue = cPickle.loads(b64decode(request.cookies['value']))
    form = """
    <html>
       <body>Cookie value: """ + str(cookieValue) + """
          <form action = "/cookie" method = "POST">
             <p><h3>Enter value to be stored in cookie</h3></p>
             <p><input type = 'text' name = 'value'/></p>
             <p><input type = 'submit' value = 'Set Cookie'/></p>
          </form>
       </body>
    </html>
    """
    resp = make_response(form)
    
    if value:
        resp.set_cookie('value', b64encode(cPickle.dumps(value)))

    return resp


# server side template injection
@app.route('/sayhi', methods = ['POST', 'GET'])
def sayhi():
   name = ''
   if request.method == 'POST':
      name = '<br>Hello %s!<br><br>' %(request.form['name'])

   template = """
   <html>
      <body>
         <form action = "/sayhi" method = "POST">
            <p><h3>What is your name?</h3></p>
            <p><input type = 'text' name = 'name'/></p>
            <p><input type = 'submit' value = 'Submit'/></p>
         </form>
      %s
      </body>
   </html>
   """ %(name)
   return render_template_string(template)


if __name__ == "__main__":
   app.run(host='localhost', port=4000)

