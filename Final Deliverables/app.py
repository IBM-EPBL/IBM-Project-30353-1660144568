from flask_session import Session
from flask import Flask, render_template, redirect, request, session, jsonify
from datetime import datetime
import ibm_db
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sendgrid.helpers.mail import To
dsn_hostname = "9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
dsn_uid = "cpw36749"
dsn_pwd = "v3tByUIyAxkVKukX"
dsn_driver = "{{IBM DB2 ODBC DRIVER}}"
dsn_database = "bludb"
dsn_port = "32459"
dsn_protocol = "TCPIP"
dsn_security = "SSL"
dsn = ("DRIVER={0};"
"DATABASE={1};"
"HOSTNAME={2};"
"PORT={3};"
"PROTOCOL={4};"
"UID={5};"
"PWD={6};"
"SECURITY={7};").format(dsn_driver,dsn_database,dsn_hostname,dsn_port,dsn_protocol,dsn_uid,dsn_pwd,dsn_security)
print(dsn)
try:
  conn = ibm_db.connect(dsn,"","")
  print("success")
except:
  print(ibm_db.conn_errormsg())

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")



@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")

@app.route("/best/", methods=["GET"])
def best():
          if not session.get("name"):
           return redirect("/")
          sql = "SELECT * FROM PROD_TBL"
          stmt1 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt1)
          print(row)
          prodname = []
          prodprice = []
          prodimg = []
          while row != False:
            print (row["PROD_NAME"])
            prodname.append(row["PROD_NAME"])
            prodprice.append(row['PROD_PRICE'])
            prodimg.append(row['PRO_IMG'])
            row = ibm_db.fetch_assoc(stmt1)
          return render_template ( "bestdeals.html" , len = len(prodname), prodname = prodname,prodprice=prodprice,prodimg=prodimg)

@app.route("/male/", methods=["GET"])
def male():
          if not session.get("name"):
            return redirect("/")
          sql = "SELECT * FROM PROD_TBL WHERE PRO_CAT = 'Male'"
          stmt1 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt1)
          print(row)
          prodname = []
          prodprice = []
          prodimg = []
          while row != False:
            print (row["PROD_NAME"])
            prodname.append(row["PROD_NAME"])
            prodprice.append(row['PROD_PRICE'])
            prodimg.append(row['PRO_IMG'])
            row = ibm_db.fetch_assoc(stmt1)
          return render_template ( "maleshop.html" , len = len(prodname), prodname = prodname,prodprice=prodprice,prodimg=prodimg)

@app.route("/Female/", methods=["GET"])
def female():
          if not session.get("name"):
            return redirect("/")
          sql = "SELECT * FROM PROD_TBL WHERE PRO_CAT = 'Female'"
          stmt1 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt1)
          print(row)
          prodname = []
          prodprice = []
          prodimg = []
          while row != False:
            print (row["PROD_NAME"])
            prodname.append(row["PROD_NAME"])
            prodprice.append(row['PROD_PRICE'])
            prodimg.append(row['PRO_IMG'])
            row = ibm_db.fetch_assoc(stmt1)
          return render_template ( "Femaleshop.html" , len = len(prodname), prodname = prodname,prodprice=prodprice,prodimg=prodimg)

@app.route("/logged/",methods=["POST"])
def logged():
    user = request.form["user"].lower()
    pwd = request.form["pwd"]
    logged.mailid = user
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    query = "SELECT * FROM USER_TBL WHERE username = '"+user+"' AND password = '"+pwd+"'"
    stmt = ibm_db.exec_immediate(conn, query)
    rows = ibm_db.fetch_assoc(stmt)
    try:
      if len(rows) == 2:
          session["name"] = user
          print('ok')
          return redirect("/shop/")
      else:
          return render_template ( "login.html", msg="Wrong username or password." )
    except:
       return render_template ( "login.html", msg="Wrong username or password." )

@app.route("/loggedad/",methods=["POST"])
def loggedad():
    user = request.form["user"]
    pwd = request.form["pwd"]
    if user == "" or pwd == "":
        return render_template ( "login.html" )
    query5 = "SELECT * FROM ADMIN_TBL WHERE username = '"+user+"' AND password = '"+pwd+"'"
    stmt5 = ibm_db.exec_immediate(conn, query5)
    rows5 = ibm_db.fetch_assoc(stmt5)
    print(rows5)
    try:
      session["name"] = user
      if len(rows5) == 2:
          print('ok')
          return redirect("/add/")
      else:
          return render_template ( "admin.html", msg="Wrong username or password." )
    except:
       return render_template ( "admin.html", msg="Wrong username or password." )


@app.route("/shop/" , methods=['GET'])
def shop():
          if not session.get("name"):
           return redirect("/")
          sql = "SELECT * FROM PROD_TBL"
          stmt1 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt1)
          print(row)
          prodname = []
          prodprice = []
          prodimg = []
          while row != False:
            print (row["PROD_NAME"])
            prodname.append(row["PROD_NAME"])
            prodprice.append(row['PROD_PRICE'])
            prodimg.append(row['PRO_IMG'])
            row = ibm_db.fetch_assoc(stmt1)

          return render_template ( "index.html" , len = len(prodname), prodname = prodname,prodprice=prodprice,prodimg=prodimg)

@app.route("/Order/" , methods=['GET'])
def order():
          if not session.get("name"):
           return redirect("/")          
          sql = "SELECT * FROM ORDHIST_TBL Where PUR_MAIL = '"+logged.mailid+"'"
          stmt2 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt2)
          print(row)
          prod_name = []
          pur_date = []
          pur_mail = []
          while row != False:
            print (row["PROD_NAME"])
            prod_name.append(row["PROD_NAME"])
            pur_date.append(row['PUR_DATE'])
            pur_mail.append(row['PUR_MAIL'])
            row = ibm_db.fetch_assoc(stmt2)

          return render_template ( "order.html" , len = len(prod_name), prod_name = prod_name,purc_date=pur_date,purc_mail=pur_mail)
@app.route("/Orderhis/" , methods=['GET'])
def orderhis():
          if not session.get("name"):
           return redirect("/")  
          sql = "SELECT * FROM ORDHIST_TBL"
          stmt2 = ibm_db.exec_immediate(conn, sql)
          row = ibm_db.fetch_assoc(stmt2)
          print(row)
          prod_name = []
          pur_date = []
          pur_mail = []
          while row != False:
            print (row["PROD_NAME"])
            prod_name.append(row["PROD_NAME"])
            pur_date.append(row['PUR_DATE'])
            pur_mail.append(row['PUR_MAIL'])
            row = ibm_db.fetch_assoc(stmt2)

          return render_template ( "orderhis.html" , len = len(prod_name), prod_name = prod_name,purc_date=pur_date,purc_mail=pur_mail)


@app.route("/modal/" , methods=['GET'])
def modal():
        pro_name1 = request.args.get('pro_name1')
        print(pro_name1)
        modal.proname1 = pro_name1
        date = datetime.now()
        modal.mailid = logged.mailid
        sendmail()
        sql_stmt3 = "insert into ORDHIST_TBL values(?, ?, ?)"
        stmt3  = ibm_db.prepare(conn, sql_stmt3)
        ibm_db.bind_param(stmt3, 1, pro_name1)
        ibm_db.bind_param(stmt3, 2, date) 
        ibm_db.bind_param(stmt3, 3, logged.mailid)
        try:
          ibm_db.execute(stmt3)
          return render_template("added.html",pro_name1 = pro_name1)
        except:
          print(ibm_db.stmt_errormsg())
        



@app.route("/add/", methods=["GET"])
def add():
          if not session.get("name"):
           return redirect("/")
          return render_template("Add_product.html")


@app.route("/logout/", methods=["GET"])
def logout():
     session["name"] = None
     return render_template("login.html")

@app.route("/register/", methods=["GET"])
def register():
     return render_template("Register.html")

@app.route("/registered/", methods=["POST"])
def registered():
     username = request.form["username"]
     password = request.form["pass"] 
     sql2 = "insert into USER_TBL values(?,?)"
     stmt7 = ibm_db.prepare(conn, sql2)
     ibm_db.bind_param(stmt7, 1, username)
     ibm_db.bind_param(stmt7, 2, password)
     try:
      ibm_db.execute(stmt7)
      return render_template("login.html",msg = "Added Successfully")
     except:
       print(ibm_db.stmt_errormsg())
       return render_template("Register.html",msg = "tryagin")


@app.route('/sendmail')
def sendmail():
  str
  message = Mail(from_email='713319cs124@smartinternz.com',
    to_emails= To(logged.mailid),
    subject='Order Confirmed! Fashion Recommender',
    html_content='<pre>Thank you for your order! The estimated delivery date is based on the handing time and the warehouse processing time in certain cases, the estimated delivery date will vary.<br> You will receive a tracking number by email once your package ships.<br> You can check the status of your order on our App <br>Find your order confirmation below. Thank you again for ordering from Glamtique,</pre><br> For any changes to this order, contact Order Help Desk<br> <strong>Order Item Name :: '+modal.proname1+' </strong><br>If it is not you, please contact our support.<strong>Thank You</strong>')
  sg = SendGridAPIClient('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')
  response = sg.send(message)
  print(response.status_code)
  print(response.body)
  print(response.headers)
  # except Exception as e:
  #   print(e.message)

@app.route("/added/", methods=["POST"])
def added():
  prod_name = request.form["prodname"]
  prod_price = request.form["prodprice"] 
  prod_cat = request.form["prodcat"]
  prod_img = request.form["prodimg"]
  sql1 = "insert into PROD_TBL values(?,?,?,?)"
  stmt6 = ibm_db.prepare(conn, sql1)
  ibm_db.bind_param(stmt6, 1, prod_name)
  ibm_db.bind_param(stmt6, 2, prod_price)
  ibm_db.bind_param(stmt6, 3, prod_img)
  ibm_db.bind_param(stmt6, 4, prod_cat)
  try:
    ibm_db.execute(stmt6)
    return render_template("Add_product.html",msg = "Added Successfully")
  except:
    print(ibm_db.stmt_errormsg())
    return render_template("Add_product.html",msg = "tryagin")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
