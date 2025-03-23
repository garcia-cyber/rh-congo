import sqlite3 as sq 

db = sq.connect("rh.db")

# creation de la table postes 
#
# 
db.execute("""
            create table if not exists postes(
           idPoste integer primary key autoincrement,
           libPoste varchar(80))
""")

# ajout du poste par defaut 
#
#
#db.execute("insert into postes(libPoste) values('responsable des ressources humaines')")

# creation de la table employes
# 
#

db.execute("""
                create table if not exists employes(
           idEmpl integer primary key autoincrement,
           nomsEmpl varchar(80),
           matriculeEmpl varchar(30) unique,
           civiliteEmpl varchar(30),
           sexeEmpl char(1), 
           phoneEmpl varchar(15), 
           emailEmpl varchar(50),
           communeEmpl varchar(30),
           adresseEmpl varchar(50),
           lieuNai varchar(40),
           dateNai date ,
           province varchar(40),
           posteEmpl integer ,
           statut varchar(10) default 'actif',
           lifeEmploye char(3) default 'oui',
           photoEmpl text , 
           dateR timestamp default current_timestamp , 
           register integer , 
           passwordEmpl varchar(40),
           foreign key(posteEmpl) references postes(idPoste)
           
           )
""") 

# information par defaut rh
#
#db.execute("insert into employes(nomsEmpl,matriculeEmpl,phoneEmpl,emailEmpl,passwordEmpl,register,posteEmpl) values('rh admin','000-rh/3','0982484573','rh@gmail.com','rh1234',1,1)")

## table conges 
db.execute("create table if not exists conges(idConge integer primary key autoincrement , debutC date , finC date , emplID integer, typeC varchar(40),foreign  key(emplID) references employes (idEmpl))")

#commit general 
db.commit()