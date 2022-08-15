import schedule
import time
import mysql.connector
from python_orange_sms import utils


def sendSMS(numberReceveur,nomEleve,classe):
    # sans + (225...)
    SENDER_NAME = 'LTA send sms'
    AUTH_TOKEN = 'Basic YXljWUM1U1hMbHJOUTBJR2w5UGJXc3BDak52eGJ0SG06SlVyUjRuVTZCWnl3U21ScA=='
    message = "Bonjour chers parent l'etudiant {} en classe de {} n'a pas été présent aujourd'hui au sein du Lycee Technique Abidjan".format(nomEleve,classe)
    recipient_phone_number=numberReceveur
    dev_phone_number='2250787610716'

    sms = utils.SMS(AUTH_TOKEN = AUTH_TOKEN,SENDER_NAME=SENDER_NAME)
    res = sms.send_sms(message=message,dev_phone_number=dev_phone_number,recipient_phone_number=recipient_phone_number)
    print(res)
    if res.status_code == 201:
        print('MESSAGE ENVOYE AVEC SUCCES : ', res.text) # SMS sent
    else:
        print('UN PROBLEME EST SURVENU : ', res.text) # OOPS





def job():
    #connexion a la base de données
    db = mysql.connector.connect(
    host = "eu-cdbr-west-02.cleardb.net",
    user = "bce836f57eda4a",
    password = "6b7c3de3",
    database = "heroku_cc97a78d994c2bf"
    )
    #créer un curseur de base de données pour effectuer des opérations SQL
    cursor = db.cursor()
    cursor.execute("SELECT * FROM etudiants")

    #récupèrer toutes les lignes de la dernière instruction exécutée.
    res = cursor.fetchall()

    for line in res:
       nomEleve= line[1]
       numeroParent = line[3]
       classe=line[2]
       isPresent=line[4]
       if isPresent==False:
           print(nomEleve, " n'as pas été présent aujourd'hui ")
           print("ENVOYER UN MESSAGE A : ",numeroParent)
           sendSMS(numeroParent,nomEleve,classe)
           #send message to parent
       
       
    print("---------------------")
    # remettre tous a 0
    cursor.execute("UPDATE etudiants SET isPresent = %s",(False,))
    db.commit()  





schedule.every().day.at("12:55").do(job)
while True:
  schedule.run_pending()
  time.sleep(1)
# la boucle pour repeter chaque jour









