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
@app.route('/',methods = ['POST','GET'])
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

###
#
# liste de personnel vivant 
@app.route('/personnel')
def personnel():
    if 'rh' in session:
        with sqlite3.connect("rh.db") as con :
            cur = con.cursor()
            cur.execute("select idEmpl, nomsEmpl,sexeEmpl,matriculeEmpl,civiliteEmpl,communeEmpl,adresseEmpl,lieuNai,dateNai,province,libPoste , statut , phoneEmpl from employes inner join postes on employes.posteEmpl = postes.idPoste where lifeEmploye = 'oui'") 
            data = cur.fetchall()

        return render_template('export-table.html', data = data ) 
    else:
        return redirect('/login')
    
###
#
# liste de personnel mort 
@app.route('/personnelM')
def personnelM():
    if 'rh' in session:
        with sqlite3.connect("rh.db") as con :
            cur = con.cursor()
            cur.execute("select idEmpl, nomsEmpl,sexeEmpl,matriculeEmpl,civiliteEmpl,communeEmpl,adresseEmpl,lieuNai,dateNai,province,libPoste , statut , phoneEmpl from employes inner join postes on employes.posteEmpl = postes.idPoste where lifeEmploye = 'non'") 
            data = cur.fetchall()

        return render_template('decedes.html', data = data ) 
    else:
        return redirect('/login')


##
#
# ajout de poste 
@app.route('/poste', methods = ['POST','GET']) 
def poste():
    if 'rh' in session:
        if request.method == 'POST':
            poste = request.form['poste'] 

            with sqlite3.connect('rh.db') as con :

                # verification du poste existsant 
                pst = con.cursor()
                pst.execute("select * from postes where libPoste = ?",[poste])
                dataP = pst.fetchone()

                if dataP:
                    flash("le poste existe deja dans le systeme")
                else:
                    cur = con.cursor()
                    cur.execute("insert into postes(libPoste) values(?)",[poste])
                    con.commit()
                    cur.close()
                    flash(f"poste {poste} ajoutee !! ")    
        return render_template('basic-form.html')
    else:
        return redirect('/login')
##
#
# liste des postes
@app.route('/listPoste')
def listPoste():
    if 'rh' in session:
        with sqlite3.connect('rh.db') as con :
            cur = con.cursor()
            cur.execute("select * from postes")
            data = cur.fetchall()
        return render_template('postes.html', data = data)
    else:
        return redirect("/login")
##
# 
# modifcation du postes
@app.route('/modifierPoste/<string:idPoste>', methods = ["POST",'GET'])
def modifier(idPoste):
    if 'rh' in session:
        if request.method == 'POST':
            poste = request.form['poste'] 
            with sqlite3.connect('rh.db') as con :
                add = con.cursor()
                add.execute("update postes set libPoste = ? where idPoste = ?",[poste,idPoste]) 
                con.commit()
                add.close()
                return redirect('/listPoste')
            
        with sqlite3.connect('rh.db') as con :
            cur = con.cursor()
            cur.execute("select * from postes where idPoste = ?", [idPoste])
            value = cur.fetchone()

        return render_template('modifiePoste.html', values = value)
    else:
        return redirect('/login')  
##
# 
# ajout de personnels  
@app.route("/addPersonnel",methods = ['POST', 'GET'])
def addPersonnel():
    if 'rh' in session:

        if request.method =='POST':
            noms = request.form['noms']
            telephone = request.form['telephone']
            matricule = request.form['matricule']
            commune = request.form['commune'] 
            avenue = request.form['avenue']
            lieu   = request.form['lieu']
            naissance = request.form['naissance']
            province = request.form['province']
            etat = request.form['etat']
            poste = request.form['poste']
            sexe = request.form['sexe']
            pwd  = 1234

            with sqlite3.connect("rh.db") as con :
                #verication du matricule 
                mat = con.cursor()
                mat.execute("select * from employes where matriculeEmpl = ?",[matricule])
                data_mat = mat.fetchone()

                #verification du telephone 
                tel = con.cursor()
                tel.execute("select * from employes where phoneEmpl = ?",[telephone])
                data_tel = tel.fetchone()

                #verification de poste 
                pst = con.cursor()
                pst.execute("select * from employes where posteEmpl = ?",[poste])
                data_pst = pst.fetchone()

                if data_mat:
                    flash(f" matricule {matricule} deja attribue".title()) 
                elif data_tel:
                    flash(f"numero {telephone} deja attribue".title())
                elif data_pst :
                    flash(f" post deja attribue".title())
                else:
                    cur = con.cursor()
                    cur.execute("""
                                    insert into employes(nomsEmpl,matriculeEmpl,civiliteEmpl,sexeEmpl,phoneEmpl,communeEmpl,adresseEmpl,lieuNai,dateNai,province,
                                posteEmpl,passwordEmpl,register) values(?,?,?,?,?,?,?,?,?,?,?,?,?)

""",[noms,matricule,etat,sexe,telephone,commune,avenue,lieu,naissance,province,poste,pwd,session['id']]) 
                    con.commit()
                    cur.close()
                    flash("personnel enregistree !!!")
                    return redirect('/addPersonnel')    







        with sqlite3.connect('rh.db') as con :
            pst = con.cursor()
            pst.execute("select * from postes")
            dt = pst.fetchall()

        return render_template("personnelAdd.html", dt = dt) 
    else:
        return redirect('/login')  
##
# 
# change le mot de passe
@app.route('/change/<idEmpl>',methods = ['POST',"GET"]) 
def change(idEmpl):
    if 'rh' in session:
        if request.method == 'POST':
            p1 = request.form['p1']
            p2 = request.form['p2']
            p3 = request.form['p3'] 

            with sqlite3.connect('rh.db') as con :
                #verification du mot de passe
                pd1 = con.cursor()
                pd1.execute("select * from employes where passwordEmpl = ? and idEmpl = ?",[p1,session['id']])
                data_p1 = pd1.fetchone() 

                if data_p1:
                    if p2 == p3:
                        cur = con.cursor()
                        cur.execute("update employes set passwordEmpl = ? where idEmpl = ?" , [p2,session['id']])
                        con.commit()
                        cur.close()
                        return redirect('/login')
                    else:
                        flash("le mot de passe doit etre conforme")
                else:
                    flash("ancien mot de passe incorrect")
        return render_template('auth-reset-password.html') 
    else:
        return redirect('/login')
##
# 
# conge 
@app.route('/conge/<string:idEmpl>', methods = ['POST','GET'])
def conge(idEmpl):
    if 'rh' in session:
        if request.method == 'POST':
            type = request.form['type']
            debut = request.form['debut'] 
            fin   = request.form['fin'] 

            with sqlite3.connect("rh.db") as con :
                #verification dela date du debut 

                dt = con.cursor()
                dt.execute("select * from conges where debutC = ? and emplID = ?", [debut, idEmpl])
                data_dt = dt.fetchone()

                #verification de la fin 

                ft = con.cursor()
                ft.execute("select * from conges where finC = ? and emplID = ?", [debut, idEmpl])
                data_ft = ft.fetchone()

                if data_dt:
                    flash("Pour cet employe la date du debut existe deja")
                elif data_ft:
                    flash("Pour cet employe la date de la fin existe deja")

                else:
                    cur = con.cursor()
                    cur.execute("insert into conges(debutC,finC , emplID , typeC) values(?,?,?,?)",[debut,fin,idEmpl,type])
                    con.commit()
                    cur.close()

                    flash("conge attribue!!!! ")


        return render_template('conge.html')   
    else:
        return redirect('/login')    

##
# 
# liste de personnel en conge
@app.route('/listConge')
def listConge():
    if 'rh' in session:
        with sqlite3.connect("rh.db") as con :
            cur = con.cursor()
            cur.execute("select idConge,nomsEmpl , phoneEmpl , debutC,finC,libPoste from employes inner join conges on conges.emplID = employes.idEmpl inner join postes on postes.idPoste = employes.posteEmpl ") 
            data = cur.fetchall()
        return render_template('vector-map.html', data = data )  
    else:
        return redirect('/login')   
##
#
# formulaire d'absence
@app.route('/absence/<idEmpl>', methods = ['POST','GET']) 
def absence(idEmpl):
    if 'rh' in session:
        return render_template("dropdown.html")
    else:
        return redirect('/login') 

##
# 
# boucle  
if __name__ == '__main__':

    app.run(debug=True)

