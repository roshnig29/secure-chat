import eventlet
import eventlet.wsgi

from flask import Flask,render_template
from flask_socketio import SocketIO,send
import hashlib
import ssl
from Crypto.Cipher import AES

#Enter your details
ip = 'your_ip'
port = 5000
link_to_certificate = 'mycrt.crt' #filepath 
link_to_key = 'mykey.key' #filepath

KEY = hashlib.sha256(b"some random password").digest()	
#this will convert any pnemonic string which the user wants to choose as password to a 32 bit encrypted object
IV = b"abcdefghijklmnop"#Initialization vector should always be 16 bit
obj_enc = AES.new(KEY, AES.MODE_CFB, IV) #creating an object to encrypt our data with
obj_dec = AES.new(KEY, AES.MODE_CFB, IV) #creating an object to decrypt our data with			

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!123'
app.config['SSL_CERT'] = 'mycrt.crt'
app.config['SSL_KEY'] = 'mykey.key'

socketio = SocketIO(app,cors_allowed_origind = "*")

@socketio.on('message')
def handle_message(message):
    #print("Received message: "+message)
    if message !="User connected!":
        send(message,broadcast = True)

@app.route('/')
def index():
    return render_template("index.html")

#Run the server using eventlet
if(__name__)=="__main__":
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(app.config['SSL_CERT'], app.config['SSL_KEY'])
    eventlet.wsgi.server(eventlet.wrap_ssl(eventlet.listen((ip, port)), 
                                           certfile=link_to_certificate, keyfile=link_to_key, server_side=True), app) 