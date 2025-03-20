from flask import Flask , render_template , session , redirect , url_for , flash , request
import pymysql 
import os 
import sqlite3
#import re as rd  



###
#
#configurations

app = Flask(__name__) 
app.secret_key = 'AppRessourceHumaine_MukokoGracia'

###
#
# interface login 
# @app.route('/',methods = ['POST','GET'])
@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        num = request.form['num']
        pas = request.form['password'] 
        statut = 'actif'

        #connection avec la base de donnee 
        with sqlite3.connect("rh.db") as con :
            ## verification du mot de passe 
            pwd = con.cursor()
            pwd.execute("select * from employes where phoneEmpl = ? and passwordEmpl = ?", [num , pas])
            cur = pwd.fetchone()

            ## verification du email
            mail = con.cursor()
            mail.execute("select * from employes where emailEmpl = ? and passwordEmpl = ?", [num , pas])
            curM = mail.fetchone()

            ##verification du statut 
            st = 'actif'
            stat = con.cursor()
            stat.execute("select * from employes where statut = 'actif' and phoneEmpl = ? and passwordEmpl = ? " , [num, pas])
            data = stat.fetchone()

            #mail
            statM = con.cursor()
            statM.execute("select * from employes where statut = 'actif' and emailEmpl = ? and passwordEmpl = ? " , [num, pas])
            dataM = statM.fetchone()

            ## verification si la personne est deja mort 
            mrt = con.cursor() 
            mrt.execute("select * from employes where lifeEmploye = 'oui' and phoneEmpl = ? and passwordEmpl = ? " , [num, pas])
            dataMort = mrt.fetchone()

            mrtM = con.cursor() 
            mrtM.execute("select * from employes where  lifeEmploye = 'oui' and emailEmpl = ? and passwordEmpl = ? " , [num, pas])
            dataMortM = mrtM.fetchone()

            if curM:

                if dataM:
                    if dataMortM:
                        session['rh'] = True 
                        session['id'] = curM[0]
                        session['nom'] = curM[1]
                        session['poste'] = curM[12]
                        return redirect("/home")

                    
                        
                    else:
                        return flash("personnel  est deja  décède")
                    
                else:
                    return flash("statut bloque ,veillez consulte le rh ")
                # teste cote phone
            elif cur:
                if data:
                    if dataMort:
                        session['rh'] = True 
                        session['id'] = cur[0]
                        session['nom'] = cur[1]
                        session['poste'] = cur[12]

                        return redirect('/home')
                    else:
                        return flash("personnel  est deja  décède")
                else:
                    return flash("statut bloque ,veillez consulte le rh ")
            else:
                return flash("mot de passe errone ")


             
       
    return render_template('auth-login.html')

### 
# 
# deconnexion 
@app.route('/deco')
def deco():
    session.clear()
    return redirect('/')


###
#
# interface d'accueil 
@app.route("/home")
def home():
    if 'rh' in session:
        return render_template('index.html') 
    else:
        return redirect('/')



