from flask import Flask,url_for,render_template
from config import Config
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import Receive_mail as rm

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
db = SQLAlchemy(app)
mail.init_app(app)

@app.route("/")
def index():
    return render_template('index.html')


def Download():
    if (rm.download() == True):
        if (rm.save_data() == True):
            data = pd.read_csv('E:/Python/fedral organization Python developer task/Task#1 Server End Coding using Flask/Attachments/order.csv')
            sendmail_to = data['mail_to'][0]
            msg = Message('Hello', sender='techdiv07@gmail.com',recipients=[sendmail_to])
            
            with app.open_resource("E:/Python/fedral organization Python developer task/Task#1 Server End Coding using Flask/Attachments/order.csv") as fp:
                msg.attach("order.csv","file/csv",fp.read())
            mail.send(msg)
            
            return True
        
    else:
        return False



def Send():
    try:

        data = pd.read_csv('E:/Python/fedral organization Python developer task/Task#1 Server End Coding using Flask/Attachments/order.csv')
        sendmail_to = data['mail_from'][0]
        mail_txt = rm.reply_mail()
        if(mail_txt):
            msg = Message('Hello', sender='techdiv07@gmail.com',recipients=[sendmail_to])
            msg.body = str(mail_txt)
            mail.send(msg)
            return True
        else:
            return False

    except:
        return False
    
    

@app.route("/Main_R")
def Main_R():
    if(Download()):
        return "<h3>User#1 Sent an email with an attestment. it was downloaded and send to User#2</h3>"
    elif(Send()):
        return "<h3>User#2 sent a reply which was send to User#1</h3>"
    else:
        return "<h3>Message Not Found!</h3>"


if __name__=="__main__":
    app.run(debug=True)
    