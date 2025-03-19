from flask import Flask , render_template 
import pymysql 
import os 



###
#
#configurations

app = Flask(__name__) 
app.secret_key = 'AppRessourceHumaine_MukokoGracia'

###
#
# interface login 
@app.route('/',methods = ['POST','GET'])
@app.route('/login',methods = ['POST','GET'])
def login():
    return render_template('auth-login.html')



