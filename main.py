#!/usr/bin/env python
import os
from base64 import b64decode,b64encode
from binascii import hexlify, unhexlify
from os import popen
from lxml import etree
import cgi,cPickle
from Crypto.Cipher import AES
from Crypto import Random


from flask import Flask, request, make_response, render_template_string, Markup, send_from_directory, send_file, render_template, redirect, url_for


app = Flask(__name__)


# Config stuff
KEY=Random.new().read(32) # 256 bit key for extra security!!!
BLOCKSIZE=AES.block_size
ADMIN_SECRET=Random.new().read(32) # need to keep this secret
APP_NAME = 'StreamWide test'

CONFIG = {
    'encrypto_key' : b64encode(KEY),
    'secret_admin_value' : b64encode(ADMIN_SECRET),
    'app_name' : APP_NAME,
}

def rp(command):
    return popen(command).read()


@app.route('/forum', methods = ['POST', 'GET'])
def forumIndex():
    if request.method == 'POST':
      search = request.form['search']
      command = "echo " + search
      searchRes = rp("echo " + search)
      print(searchRes)
      return render_template('index.html', searchResult=searchRes)
    return render_template('index.html')

@app.route('/screen.css')
def cssIndex():
    return redirect(url_for('static', filename='styles/screen.css'))

@app.route('/forum/profile', methods = ['POST', 'GET'])
def profileIndex():
    value0 = None
    if request.method == 'POST':
      value0 = request.form['usernamerepresentation']
    elif 'usernamerepresentation' in request.cookies:
      value0 = cPickle.loads(b64decode(request.cookies['usernamerepresentation']))

    print(value0 is None)
    if value0 is None:
       value0 = ""
    return render_template('profile.html', username=value0)

@app.route('/forum/topics', methods = ['POST', 'GET'])
def topicsIndex():
    if request.method == 'POST':
         expression = request.form['recapcha']
         posttext = request.form['body']
            
         if expression == "'" or expression == '"' or expression == '""' or expression == "''":
            return """
            <html>
                  <body>""" + "Result: Text only numbers otherwise your session will end." + """
                  </body>
               </html>
               """
         recapchaVal = int(str(eval(expression)).replace('\n', '\n<br>'))
         if recapchaVal <> 4:
            return """
            <html>
                  <body>""" + "Invalid recapcha." + """
                  </body>
               </html>
               """
         
         template = render_template('topic.html', text=posttext)
         print(posttext)
         return render_template_string(template)

    
    return render_template('topic.html', text="")

@app.route('/')
def index():
    return """
    <html>
    <head><title>StreamWide test: """ + CONFIG['app_name'] +"""</title></head>
    <body>
        <p><h3>StreamWide e-commerce website</h3></p>
        <a href="/personalized_profile">Personalize your profile </a><br>
        <a href="/lookup">Find more about our clients websites </a><br>
        <a href="/evaluate_prices">Calculate prices </a><br>
        <a href="/sayhi">Receive a personalised greeting </a><br>
        <a href="/
    </body>
    </html>
    """

@app.route(b64decode('L2V2YWx1YXRlX3ByaWNlcw=='), methods = ['POST', 'GET']) #/evaluate_prices
def evalua123fadewqewqeqwte():
    expression = None
    if request.method == 'POST':
        expression = request.form['expression']
        if expression == "'" or expression == '"' or expression == '""' or expression == "''":
           return """
           <html>
               <body>""" + "Result: Text only numbers otherwise your session will end." + """
               </body>
            </html>
            """
    return """
    <html>
       <body>""" + "Result: " + (str(eval(expression)).replace('\n', '\n<br>')  if expression else "") + """
          <form action = """ + b64decode('Ii9ldmFsdWF0ZV9wcmljZXMi') + """ method = "POST">
             <p><h3>Enter the products' prices to be evaluated</h3></p>
             <p><input type = 'text' name = 'expression'/></p>
             <p><input type = 'submit' value = 'Evaluate'/></p>
          </form>
       </body>
    </html>
    """

@app.route(b64decode('L2ltYWdl'), methods=['GET']) #/lovecats = /images, folosit la incarcarea imaginilor in app
def lo123zveeee341e():
    image_name = request.args.get('image_name')
    if not image_name:
        return 404
    else:
        return send_file(os.path.join(os.getcwd(), image_name))

@app.route(b64decode('L2FwYWNoZTI='), methods=['GET']) #/apache2
def cnf():
    param = request.args.get('param', 'not set')

    #param = Markup.escape(param)
    print(param)
    html = open('apache.html').read()
    
    response = make_response(html.replace('{{ param }}', param))
    response.headers.set('X-XSS-Protection', '0')
    return response

@app.route(b64decode('L2xvb2t1cA=='), methods = ['POST', 'GET']) #/lookup
def ldsaaaaaaaaaaookdasssssssssssssassssssssup():
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
         <form action = """ + b64decode('Ii9sb29rdXAi') + """  method = "POST">
            <p><h3>Find more about our clients, enter their domain name for additional information regarding their status.</h3></p>
            <p><input type = 'text' name = 'address'/></p>
            <p><input type = 'submit' value = 'Lookup'/></p>
         </form>
      </body>
   </html>
   """
    
@app.route(b64decode('L3BlcnNvbmFsaXplZF9wcm9maWxl'), methods = ['POST', 'GET']) # '/personalized_profile'
def per1235123666666666666fdfdfsdffsdsd6666666profdsadsadsadasile():
    value0 = None
    value = None
    
    if request.method == 'POST':
        value0 = request.form['value']
        value = value0
    elif 'value' in request.cookies:
        value0 = cPickle.loads(b64decode(request.cookies['value']))
    form = """
    <html>
       <body>Personalized name: """ + str(value0) + """
          <form action = """ + b64decode('Ii9wZXJzb25hbGl6ZWRfcHJvZmlsZSI=') + """ method = "POST">
             <p><h3>Enter your name for a personalized session during your shopping. </h3></p>
             <p><input type = 'text' name = 'value'/></p>
             <p><input type = 'submit' value = 'Set my profile'/></p>
          </form>
       </body>
    </html>
    """
    resp = make_response(form)
    
    if value:
        resp.set_cookie('value', b64encode(cPickle.dumps(value)))

    return resp


@app.route(b64decode('L3NheWhp'), methods = ['POST', 'GET']) #exec(compile(b64decode('QGFwcC5yb3V0ZSgnL3NheWhpJywgbWV0aG9kcyA9IFsnUE9TVCcsICdHRVQnXSk=').replace('\n', ''),'<string>','exec')); /sayhi
def sattttttttttttt0000000000000000000ttttttttttttttttttttttyhi():
   name = ''
   if request.method == 'POST':
      name = '<br>Hello %s!<br><br>' %(request.form['name'])

   template = """
   <html>
      <body>
         <form action = """ + b64decode("L3NheWhp") + """ method = "POST">
            <p><h3>What is your name?</h3></p>
            <p><input type = 'text' name = 'name'/></p>
            <p><input type = 'submit' value = 'Submit'/></p>
         </form>
      %s
      </body>
   </html>
   """ %(name)
   return render_template_string(template)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 8080, debug = False)
