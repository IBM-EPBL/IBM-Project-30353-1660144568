
import urllib.request
from colorama import Cursor
from flask import Flask,render_template, request, session,url_for,redirect
import ibm_db
#from pythondb import dbconn as db

try:
    conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756;SECURITY=SSL; SSLServerCertificateDigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=nhl80748;PWD=3yD0G9e6VuQHsOBX;", "", "")
    print("connection Success")
    
    
except:
    print("couldn't connect")


app = Flask(__name__)
@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/result",methods=['POST'])
def  login():
    msg=''
    email=request.form['email']
    password=request.form['password']
    conn('SELECT*FROM USER WHERE email=%s AND password=%s',(email,password))
    record=conn.fetchone()

    if record:
        session['loggedin']='True'
        session['email']=record[2]
        return "logged in successful"
    else:
        msg='invalid email/password'
    return render_template('index.html',msg=msg)    


        
if __name__=="__main__":
    app.run(debug=True)
