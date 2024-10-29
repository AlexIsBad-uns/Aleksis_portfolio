from flask import Flask, render_template ,request
import time
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
load_dotenv()
app = Flask(__name__)


# Sūtīt e-pastus
def mail(email, pssd, mssg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, pssd)

    # utf-16 nodrošina garumzīmes un citus simbolus
    msg = MIMEText(mssg, 'plain', 'utf-16')
    msg['From'] = email
    msg['To'] = 'badunsaleksis@gmail.com'
    msg['Subject'] = "Jauna zina no Portfolio majaslapas"
    
    server.sendmail(email, 'badunsaleksis@gmail.com', msg.as_string())
    server.quit()



@app.route('/')
def home_page():
    return render_template("index.html")


def cleanMsg(data):
    name = data.get('name')
    email = data.get('email')
    msg = data.get('message')
    message = f"""
        From: {name} <{email}>
        Subject: Jauna zina no Portfolio majaslapas
        {msg}
    """
    return message

@app.route('/submit_form',methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        data = request.form.to_dict()
        msg = cleanMsg(data)
        password = os.environ.get('EMAIL_PASS')
        mail('badunsaleksis@gmail.com', password, msg)
        return render_template("index.html",code="test()")
    else:
        return f"Kautkas neiet"
    
# Problēmu gadījumā 
@app.errorhandler(404)  
def not_found(e): 
  return render_template("404.html") 

if __name__ == '__main__':
    app.run(debug=True)