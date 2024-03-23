import re
import db
from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import psycopg2.extras
from passlib.context import CryptContext


#---------------------------- cryptage du mot de passe --------------------------------------------------------------------------


password_ctx = CryptContext(schemes=['bcrypt']) # configuration de la bibliothèque

app = Flask(__name__)
app.secret_key  = b"4fa9213bf2708cf5d676d5c27df243db6042ca9e5ac9f89e05166f86491f00aa"

# Vérifie si un mail est valide
def is_valid_email(email):
    # Signes présents dans un email
    email_regex = r'^\S+@\S+\.\S+$'
    # re.match permet de vérifier si un email est valide
    if re.match(email_regex, email):
        return True
    else:
        return False


#--------------------------------------- Connexion au site web ----------------------------------------------------------------------


#page de connexion 
@app.route("/connexion")
def connexion():
   if session != {}:
      connected = True
      return render_template("connexion.html",connected =connected)
   return render_template("connexion.html")
  
  

#succès de la connexion
@app.route("/success", methods = ["GET"])
def true_connect():
   email = request.args.get("mail",None)
   password = request.args.get("password",None).encode("utf-8")
   
   if is_valid_email(email):
      with db.connect() as conn:
         with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("SELECT id_adherent,nom,prenom,mdp FROM adherent WHERE email = (%s)",(email,))
            data_adherent = cur.fetchall()

            if not data_adherent :
               not_subscribed = False
               pas_inscrit = "Vous n'êtes pas inscrit. Veuillez vous inscrire si vous voulez vous connecter."
               return render_template("connexion.html",not_subscribed = not_subscribed,pas_inscrit = pas_inscrit)

            else:
               if password_ctx.verify(password,data_adherent[0].mdp):
                     session["user"] = data_adherent[0].prenom+" "+data_adherent[0].nom+" "+str(data_adherent[0].id_adherent)
                     connected = True
                     return render_template("success.html",connected = connected)
               # échec de la connexion
               else:
                     connected = False
                     msg_erreur = "Adresse mail et/ou mot de passe incorrect"
                     return render_template("connexion.html",connected = connected,msg_erreur = msg_erreur)
   else:
               connected = False
               msg_erreur = "Adresse mail et/ou mot de passe incorrect"
               return render_template("connexion.html",connected = connected,msg_erreur = msg_erreur)

#------------------------------------------------------------------------------------------------------------------------------------------
#redirection vers les pages principales
@app.route("/")
def redirection():
   return redirect(url_for('accueil'))

# Page d'accueil
@app.route("/accueil")
def accueil():
   if session != {}:
      connected = True
      return render_template("accueil.html",connected = connected)
   return render_template("accueil.html")

#------------------------------------------------Gestions des sorties et inscriptions -----------------------------------------------------
#Suppression ou creation de la coordee
@app.route("/params_sortie")

def choix_user():
   if session != {}:
     connected = True
     return render_template("params_sortie.html",connected = connected)
   
@app.route("/choix_sortie",methods = ["POST"])

def choix_sortie():
    if session != {}:
        connected = True
        num_sortie = request.form.get("num_sortie",None)
        nom_cordee = request.form.get("nom_cordee",None)
        choix_definitif =  request.form.get("del_close",None)
        if choix_definitif == "cloturer":
          with db.connect() as conn:
               with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                  cur.execute("SELECT id_adherent FROM inscrit WHERE id_sortie =%s", (num_sortie,))
                  data_parts = cur.fetchall()
                  cur.execute(" SELECT COUNT (id_adherent) FROM inscrit WHERE id_sortie =%s",(num_sortie,))
                  counter = cur.fetchone()
                  cur.execute("DELETE FROM sortie WHERE id_sortie = %s",(num_sortie,))
                  cur.execute("INSERT INTO cordee (nom_cordee,participants) VALUES (%s,%s)",(nom_cordee,counter))
                  cur.execute("SELECT id_cordee FROM cordee")
                  data_cordee = cur.fetchall()
                  for data in data_parts:
                     cur.execute("INSERT INTO appartient(id_adherent,id_cordee) VALUES (%s,%s)",(data.id_adherent,data_cordee[-1].id_cordee))
                     return render_template("choix_sorties.html",connected = connected)
                  
        else:
            
            with db.connect() as conn:
               with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                   cur.execute("DELETE FROM sortie WHERE id_sortie = %s",(num_sortie,))
                   msg_reussite = "Votre sortie a bien été supprimée"
                   return render_template("choix_sorties.html",msg_reussite = msg_reussite)


            
         




#Page d'inscription
@app.route("/inscription")
def inscription():
   if session != {}:
      connected = True
      msg_erreur  = "Vous êtes déja inscrit !"
      return render_template("inscription.html", connected = connected,msg_erreur = msg_erreur)
   else:
      with db.connect() as conn:
            with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
               cur.execute(" SELECT nivfr FROM niveau")
               level = cur.fetchall()
      return render_template("inscription.html",level = level)
   

# vérification de l'inscription 
@app.route("/verification",methods = ['POST'])

def verif():
   # Récupération des données 
   prenom = request.form.get("prenom",None)
   nom = request.form.get("nom",None)
   email = request.form.get("email",None)
   password = request.form.get("password",None)
   niv_grimpeur = request.form.get("niv_grimpeur",None)

   hashed_psw = password_ctx.hash(password) # Cryptage du mot de passe 
   if session == {}:
      if is_valid_email(email):
         with db.connect() as conn:
            with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
               cur.execute("INSERT INTO adherent(email,mdp,nom,prenom,niv_grimpeur)  VALUES (%s,%s,%s,%s,%s)",(email,hashed_psw,nom,prenom,niv_grimpeur))
               cur.execute("SELECT id_adherent FROM adherent WHERE email = %s",(email,))
               id_adherent = cur.fetchone()
               session["user"] = prenom+" "+nom+" "+str(id_adherent.id_adherent)
               connected = True
               return render_template("verification.html",connected =connected,Nom = nom,Prenom = prenom)
      connected = False
      msg_erreur = "Adresse mail incorrect: doit contenir: . et @"
      return render_template("inscription.html",connected = connected, msg_erreur = msg_erreur) 
   else:
      with db.connect() as conn:
            with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
               cur.execute("SELECT email FROM adherent WHERE email = %s",(email,))
               result = cur.fetchone()
               if result != None:
                  msg_erreur = "Vous êtes déja inscrit !"
                  return render_template("inscription.html",result =result,msg_erreur =msg_erreur)

   
#-------------------------------------------- Gestion des guides ------------------------------------------------------------------
#Affichage des guides existants

@app.route("/nos_guides")
def nos_guides():
   with db.connect() as conn:
         with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("SELECT nom,prenom,id_adherent FROM adherent WHERE niv_guide IS NOT NULL")
            personnes = cur.fetchall()
            if session != {}:
               connected = True
               return render_template("nos_guides.html",connected = connected,personnes =personnes)
            return render_template("nos_guides.html",personnes = personnes)
         


@app.route("/nos_guides/<profile>/")

def profil_guide(profile):
   profile = profile.split()
   with db.connect() as conn:
            with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
               cur.execute("SELECT prenom,nom,email,niv_guide FROM adherent WHERE nom = %s AND prenom = %s AND id_adherent = %s",(profile[1],profile[0],profile[2]))
               results = cur.fetchall()
               if session != {}:
                  connected =  True
                  return render_template("profile_guide.html",results = results,connected = connected)
            return render_template("profile_guide.html",profile =profile,results = results)

    
@app.route("/nos_guides/<profile>/<foo>")
def retour1(profile,foo):
   return redirect(url_for(foo))
         


# Page de subscription pour devenir guide
@app.route("/devenir_guide")
def devenir_guide():
   with db.connect() as conn:
            with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
               cur.execute(" SELECT nivfr FROM niveau")
               level = cur.fetchall()
               if session != {}:
                  connected = True
                  return render_template("devenir_guide.html",level = level,connected = connected)
               return render_template("devenir_guide.html",level = level)



#Vérification des données entrées
@app.route("/verif_guide",methods = ['POST'])
def verif_guide():
   if session !={}:
      connected = True
      list_nivfr = ['1', '2', '3', '4', '5a', 
                  '5b', '5c', '6a', '6b', '6c', '7a', 
                  '7b', '7c', '8a', '8b', '8c', '9a', 
                  '9b', '9c']
      prenom = request.form.get("prenom",None)
      nom = request.form.get("nom",None)
      id_adherent = request.form.get("id_adherent",None)
      niv_grimpeur = request.form.get("niv_guide",None)
      power_climber = list_nivfr.index(niv_grimpeur)
      with db.connect() as conn:
               with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                  cur.execute("SELECT niv_grimpeur FROM adherent WHERE nom = %s AND prenom = %s AND id_adherent = %s",(nom,prenom,id_adherent))
                  level_climber = cur.fetchone()
                  if level_climber == None:
                     msg_erreur = "Erreur! Données incorrectes!"
                     return render_template("devenir_guide.html",msg_erreur = msg_erreur,connected =connected)
                  real_power_climber = list_nivfr.index(level_climber.niv_grimpeur)
                  if real_power_climber < power_climber:
                     msg_erreur = "Erreur! Le niveau de guide doit être inférieur au niveau de grimpeur !"
                     return render_template("devenir_guide.html",msg_erreur = msg_erreur,connected =connected)
                  else:
                     cur.execute("UPDATE adherent SET niv_guide = %s WHERE id_adherent = %s",(power_climber,id_adherent))
                     msg_succes = "Vérification réussie"
                     return render_template("devenir_guide.html",msg_succes = msg_succes,connected = connected)
                  
   else:
      connected  = False
      msg_erreur1 = "Vous n'êtes pas connecté !"
      return render_template("devenir_guide.html",connected =connected,msg_erreur1 = msg_erreur1)



      
#----------------------------------------------------------Gestion des localités ---------------------------------------------------------------    

# Affichage des localités 
@app.route("/localites")
def localites():
     with db.connect() as conn:
         with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("SELECT DISTINCT localite FROM site_escalade")
            localites = cur.fetchall()
            if session != {}:
               connected = True
               return render_template("localites.html",loca= localites,connected =connected)
            return render_template("localites.html",loca = localites)




@app.route("/localites/<region>/")
def choix_localite(region):
     with db.connect() as conn:
         with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("SELECT DISTINCT nom_site FROM site_escalade WHERE localite = %s",(region,))
            result = cur.fetchall()
            if result == [] or result == None:
               return redirect(url_for(region))
            else:
               if session != {}:
                  connected = True
                  return render_template("choix_localite.html",result = result,connected = connected)
               connected = False
               return render_template("choix_localite.html",result = result,connected = connected)
               

# Liste des voies
@app.route("/localites/<region>/<site>/")
def choix_voies(region,site):
   with db.connect() as conn:
         with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
            cur.execute("SELECT id_voie,nom_voie,longueur_voie,nivfr,code_voie FROM voie NATURAL JOIN site_escalade WHERE localite = %s AND nom_site = %s",(region,site))
            result = cur.fetchall()
            if session != {}:
                  connected = True
                  return render_template("choix_sites.html",result=result,connected = connected)
            connected = False
            return render_template("choix_sites.html",result=result,connected = connected)
            
         

@app.route("/localites/<region>/<site>/<error>")
def error(region,site,error):
   return redirect(url_for(error))

#---------------------------------------------Gestion des sorties prévues et organisées-----------------------------------------------------------------------------------------

# Création d'une sortie
@app.route("/organise_sortie")

def organise_sortie():
      with db.connect() as conn:
               with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                  cur.execute("SELECT nivfr FROM niveau")
                  level = cur.fetchall()
                  cur.execute("SELECT DISTINCT nom_site,localite FROM voie NATURAL JOIN site_escalade")
                  data_out = cur.fetchall()
                  if session != {}:
                     connected = True
                     return render_template("organise_sortie.html",data_out =data_out,level =level,connected = connected)
                  return render_template("organise_sortie.html",data_out =data_out,level =level)

   #return render_template("organise_sortie.html",data_out = data_out)

# Verification de la validité de la sortie            
@app.route("/choix_sorties_voies",methods = ["POST"])
def verif_sortie():
   if session != {}:
      num_adherent = request.form.get("id_adherent",None)
      num_adherent = int(num_adherent)
      niv_grimpeur = request.form.get("niv_grimpeur",None)
      choix_localite  = request.form.get("choix_sortie",None)
      choix_localite = choix_localite.split()
      choix_maniere = request.form.get("choix_maniere",None)
      date_sortie = request.form.get("date_escalade",None)
      msg_description = request.form.get("msg_description",None)
      list_nivfr = ['1', '2', '3', '4', '5a', 
                     '5b', '5c', '6a', '6b', '6c', '7a', 
                     '7b', '7c', '8a', '8b', '8c', '9a', 
                     '9b', '9c']
      index_grimpeur = list_nivfr.index(niv_grimpeur)
      with db.connect() as conn:
                  with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                     cur.execute("SELECT nivfr FROM niveau")
                     level = cur.fetchall()
                     cur.execute("SELECT DISTINCT localite FROM voie NATURAL JOIN site_escalade")
                     data_out = cur.fetchall()
                     cur.execute("SELECT niv_grimpeur FROM adherent WHERE niv_grimpeur = %s AND id_adherent = %s",(niv_grimpeur,num_adherent))
                     niv_adherent = cur.fetchone()
                     index_vrai_niv = list_nivfr.index(niv_adherent.niv_grimpeur)
                     if index_grimpeur < index_vrai_niv:
                        msg_erreur = "Votre niveau doit correspondre à votre niveau."
                        render_template("organise_sortie.html",msg_erreur = msg_erreur,level = level,data_out = data_out)
                     else:
                        cur.execute("SELECT nom_voie FROM voie NATURAL JOIN site_escalade WHERE nivfr = %s AND localite = %s AND nom_site = %s",(niv_grimpeur,choix_localite[1],choix_localite[0]))
                        data_sortie = cur.fetchall()

                        if data_sortie == [] or data_sortie== None:
                              msg_erreur = "Voie inexistante dans cette avec ce niveau"
                              return render_template("organise_sortie.html",msg_erreur = msg_erreur,level = level,data_out = data_out)
                        else:
                              cur.execute("INSERT INTO sortie(organisateur,site_souhaite,court_description,date_sortie,nivfr,maniere) VALUES (%s,%s,%s,%s,%s,%s)",(num_adherent,choix_localite[0],msg_description,date_sortie,niv_grimpeur,choix_maniere))
                              cur.execute("SELECT id_sortie FROM sortie WHERE organisateur = %s",(num_adherent,))
                              sortie_id = cur.fetchone()
                              cur.execute("INSERT INTO inscrit VALUES (%s,%s)",(num_adherent,sortie_id.id_sortie))
                              return render_template("valid_sortie.html",data_sortie = data_sortie,choix_localite =choix_localite)
   else:
       msg_prev = "Vous devez vous connecter pour participer aux sorties"
       return render_template("valid_sortie.html",msg_prev = msg_prev)

      
   
    


#Affichage des sorties prévues   
@app.route("/sorties_prevues")  

def sorties_prevues():
      if session != {}:
            data_user = session["user"].split()
            id_adherent = data_user[2]
            with db.connect() as conn:
                        with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                           cur.execute( 'SELECT id_sortie,COUNT(id_sortie) As nbe_inscrits,adherent.prenom,adherent.nom,adherent.id_adherent,sortie.site_souhaite,sortie.court_description,sortie.nivfr,sortie.date_sortie FROM inscrit NATURAL JOIN sortie JOIN adherent ON adherent.id_adherent = sortie.organisateur GROUP BY (id_sortie,prenom,nom,adherent.id_adherent,site_souhaite,court_description,nivfr,date_sortie)')
                           data_sortie = cur.fetchall()
                           cur.execute("SELECT organisateur FROM sortie WHERE organisateur =%s",(id_adherent,))
                           datas = cur.fetchone()
                           if datas == None or datas == []:
                                 modif_sortie  = False
                                 return render_template("sorties_prevues.html",data_sortie =data_sortie,modif_sortie = modif_sortie)
                           else:
                                 modif_sortie = True
                                 return render_template("sorties_prevues.html",data_sortie =data_sortie,modif_sortie = modif_sortie,foo = int(id_adherent))

      else:
         with db.connect() as conn:
                     with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                        cur.execute('SELECT id_sortie,COUNT(id_sortie) As nbe_inscrits,adherent.prenom,adherent.nom,adherent.id_adherent,sortie.site_souhaite,sortie.court_description,sortie.nivfr,sortie.date_sortie FROM inscrit NATURAL JOIN sortie JOIN adherent ON adherent.id_adherent = sortie.organisateur GROUP BY (id_sortie,prenom,nom,adherent.id_adherent,site_souhaite,court_description,nivfr,date_sortie)')
                        data_sortie = cur.fetchall()
                        return render_template("sorties_prevues.html",data_sortie = data_sortie)

#Participation de l'utilisateur
@app.route("/sorties_prevues/<data_id_sortie>")

def participe_sortie(data_id_sortie):
   if session != {}:
      data_user = session["user"].split()
      connected = True
      if  len(data_id_sortie) >2:
          return  redirect(url_for(data_id_sortie))
      else:
         with db.connect() as conn:
                     with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                        cur.execute("INSERT INTO inscrit (id_adherent,id_sortie) VALUES (%s,%s)",(data_user[2],data_id_sortie))
                        cur.execute("SELECT adherent.id_adherent,nom,prenom FROM adherent JOIN inscrit ON adherent.id_adherent = inscrit.id_adherent WHERE inscrit.id_sortie  = %s",(data_id_sortie,))
                        data_inscrit = cur.fetchall()
                        return render_template("sortie_params.html",connected = connected,data_inscrit = data_inscrit)
   else:
      #msg_erreur = "Pour participer à une sortie vous devez vous connecter"
      #connected = False
      #return render_template("sortie_params.html",msg_erreur = msg_erreur,connected = connected)
      return redirect(url_for('accueil'))
      

@app.route("/sorties_prevues/<data_list>/<foos>")

def boom(data_list,foos):
    return redirect(url_for(foos))
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Page de l'histoire de l'association d'escalade
@app.route("/Association")

def Association():
   if session != {}:
      connected = True
      return render_template("association.html",connected =connected)
   return render_template("association.html")
  
#---------------------------------------------------------- Niveaux ----------------------------------------------------------
# affichage des niveaux d'escalade
@app.route("/niveaux")

def niveaux():
   with db.connect() as conn:
      with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
         cur.execute("SELECT * FROM niveau")
         niv_result = cur.fetchall()
      
      if session != {}:
         connected = True
         return render_template("niveaux.html",connected =connected, niveau  = niv_result)
   return render_template("niveaux.html", niveau  = niv_result)

#--------------------------------------------------------------------------------------------------------------------------------------------------------

# affichage du profil 
@app.route("/profil")

def profil():
   with db.connect() as conn:
      with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
         user = session["user"]
         user = user.split()
         cur.execute("SELECT prenom,nom,email,niv_grimpeur FROM adherent WHERE nom = %s AND prenom = %s",(user[1],user[0]))
         results = cur.fetchall()
   return render_template("profil.html",results = results)



              
  

#historique des voies grimpées

@app.route("/voies_grimpes")
def voies_grimpes():
   with db.connect() as conn:
            with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
               cur.execute("SELECT * FROM voies_grimpes")
               data_grimpe = cur.fetchall()
               if session != {}:
                  connected = True
                  return render_template("voies_grimpes.html",data_grimpe =data_grimpe,connected =connected)

               return render_template("voies_grimpes.html",data_grimpe =data_grimpe)

#----------------------------------------------------------------Gestion des adhérents --------------------------------------------------------------------
# Liste des adhérents
@app.route("/adherent")

def adherent():
    with db.connect() as conn:
            with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
               cur.execute("SELECT prenom,nom,id_adherent FROM adherent")
               personnes = cur.fetchall()
               if session != {}:
                  connected = True
                  return render_template("adherent.html",personnes = personnes,connected = connected)
               return render_template("adherent.html",personnes = personnes)
               
   
@app.route("/adherent/<profile>/")

def profil_adherent(profile):
   profile = profile.split()
   with db.connect() as conn:
            with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
               cur.execute("SELECT prenom,nom,email,niv_grimpeur FROM adherent WHERE nom = %s AND prenom = %s AND id_adherent = %s",(profile[1],profile[0],profile[2]))
               results = cur.fetchall()
               if session != {}:
                  connected =  True
                  return render_template("profil_adherent.html",results = results,connected = connected)
   return render_template("profil_adherent.html",profile =profile,results = results)

    
@app.route("/adherent/<profile>/<foo>")
def retour(profile,foo):
   return redirect(url_for(foo))

#------------------------------------------------Recherches voies ------------------------------------------------------------------------------------------------------------------
# Recherhes des voies
@app.route("/recherche_voies")

def recherche_voies():
     with db.connect() as conn:
            with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                cur.execute("SELECT DISTINCT nom_site FROM site_escalade")
                data_site = cur.fetchall()
                cur.execute("SELECT nivfr FROM niveau")
                level = cur.fetchall()
                if session !={}:
                    connected = True
                    return render_template("recherche_voies.html", data_site = data_site,level = level,connected =connected)
                return render_template("recherche_voies.html", data_site = data_site,level = level)
                
            

# Voies trouvées par recherche des voies
@app.route("/voie_trouvee")

def voie_trouvee():
    site_escal = request.args.get("choice_way",None)
    level = request.args.get("nivo",None)
    choice_long  =request.args.get("long_way",None)
    choice_long = choice_long.split()
    with db.connect() as conn:
               with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                  if len(choice_long) >1:
                     cur.execute("SELECT nom_voie,id_voie,longueur_voie,code_voie,nivfr FROM voie NATURAL JOIN site_escalade WHERE %s <longueur_voie AND longueur_voie< %s AND nom_site = %s AND nivfr = %s",(int(choice_long[0]),int(choice_long[1]),site_escal,level))
                     dat_voie = cur.fetchall()
                  else:
                     cur.execute("SELECT nom_voie,id_voie,longueur_voie,code_voie,nivfr FROM voie NATURAL JOIN site_escalade WHERE longueur_voie>%s AND nom_site = %s AND nivfr = %s",(int(choice_long[0]),site_escal,level))
                     dat_voie = cur.fetchall()


                  if dat_voie == [] or dat_voie == None:
                      msg_erreur = "Voie non trouvée"
                      if session !={}:
                          connected = True
                          return render_template("voie_trouvee.html",msg_erreur = msg_erreur,connected = connected)
                      return render_template("voie_trouvee.html",msg_erreur = msg_erreur)
               if session != {}:
                   connected  = True
                   return render_template("voie_trouvee.html",dat_voie = dat_voie,connected = connected)
               return render_template("voie_trouvee.html",dat_voie = dat_voie)
               
    
#Information sur la 1ere cordée à avoir escaladée la voie
@app.route("/voie_trouvee/<id_voie>")

def first_climbed(id_voie):
      if len(id_voie) > 2:
        return redirect(url_for(id_voie))
      else:
           with db.connect() as conn:
               with conn.cursor(cursor_factory=  psycopg2.extras.NamedTupleCursor) as cur:
                   cur.execute("SELECT id_cordee,maniere,nom_cordee,participants ,date_escalade FROM voies_grimpes NATURAL JOIN cordee WHERE id_voie = %s ORDER BY date_escalade LIMIT 1;",(id_voie,))
                   data_first = cur.fetchone()
                   if data_first == [] or data_first == None:
                      msg_erreur = "Données inexistantes"
                      return render_template("histo_voies.html",msg_erreur = msg_erreur)
                   else:
                       return render_template("histo_voies.html",data_first = data_first)
          
        
                      
                  
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

   



# Déconnexion
@app.route("/deconnexion")
def deconnexion():
   if session != {}:
      session.pop("user")
      return render_template("deconnexion.html")

if __name__ == '__main__':
  app.run()

