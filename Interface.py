from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import smtplib
from email.mime.text import MIMEText as text
import email.utils
from bs4 import BeautifulSoup
import urllib.request

# emails test http://univcergy.phpnet.org/python/mail.html


ma_liste = [ ]


# -------------------- Interfaces ----------------
def Menu_principal():
    global fenetre
    fenetre = Tk()
    fenetre.geometry('200x200')
    fenetre.title("Menu principal");

    Titre = Label(fenetre, text="Nom campagne", fg='Blue', font="Arial 12 italic")
    Titre.grid(row=4, column=0)

    # Gestionnaire de layout pour placement widgets
    fenetre.grid()

    # Button
    bouton0 = Button(fenetre, text='Ok', command=Verification_BD)
    bouton0.grid(row=6, column=4)

    # Création d'un widget Entry (champ de saisie)
    texte = StringVar()

    # Stock la saisie dans la variable champ
    global Champ
    Champ = Entry(fenetre, textvariable=texte, bg='white', fg='black')
    Champ.focus_set()
    Champ.grid(column=0, columnspan=3, row=6)

    fenetre.grid_columnconfigure(0, weight=1)
    fenetre.mainloop()


def Verification_BD():
    liste = [ 'test' ];

    # Recuperation des données du champ et comparaison avec BD de saisies
    for donnees in liste:
        input = Champ.get()
        if input == donnees or input == '':
            # le texte incorrect : on affiche une boîte de dialogue
            showwarning('Résultat', 'texte incorrect.\nVeuillez recommencer !')
            texte.set('')
        else:
            # le texte est bon : on ajoute le nom du projet et on lance le 2eme interface
            liste.append(input)
            print(liste)
            Interface2()


def Interface2():
    global fenetre2
    global ma_liste
    global listbox

    fenetre2 = Toplevel(fenetre)
    fenetre2.title('fenetre2')
    fenetre2.geometry('300x300')
    fenetre2.transient(fenetre)

    p = PanedWindow(fenetre, orient=HORIZONTAL)

    p.grid()
    # Button

    bouton1 = Button(fenetre2, text='Dedoublonner', command=lambda: com3_Dedoublonner()).grid(column=1, row=0)

    # Button
    bouton2 = Button(fenetre2, text='Import CSV', command=lambda: com2_bimportCSV()).grid(column=1, row=1)

    # Button
    bouton3 = Button(fenetre2, text='Valider').grid(column=2, row=0)
    # Button
    bouton4 = Button(fenetre2, text='Import Url', command=lambda: com1_bimportURL()).grid(column=2, row=1)

    # Bouton suite
    bouton5 = Button(fenetre2, text='Suite', command=Interface3).grid(column=4, row=10)

    listbox = Listbox(fenetre2, selectmode="multiple")
    listbox.grid(row=3, column=1)

    # Bouton suppression
    delete_button = Button(fenetre2, text="Delete",
                           command=lambda listbox=listbox: listbox.delete(listbox.curselection()[ 0 ])).grid(column=4,
                                                                                                             row=3)

    if (ma_liste != ""):
        print("Liste1 avant Listebox :", ma_liste)
        for i in range(len(ma_liste)):
            listbox.insert(END, ma_liste[ i ])

    fenetre2.grid_columnconfigure(0, weight=1)
    fenetre2.mainloop()


# Interface d'envoi de mail
def Interface3():
    global fenetre3
    fenetre3 = Toplevel(fenetre)
    fenetre3.title('fenetre3')
    fenetre3.geometry('400x400')
    fenetre3.transient(fenetre)

    p = PanedWindow(fenetre, orient=HORIZONTAL)

    p.grid()
    # Création d'un widget Entry (champ de saisie)
    adresse = StringVar()
    objet = StringVar()

    label1 = Label(fenetre3, text="Adresse expéditeur", fg='black')
    label1.grid(column=0, row=1)
    # Stock la saisie dans la variable champ
    global Expediteur
    Expediteur = Entry(fenetre3, bg='white', fg='black')
    Expediteur.focus_set()
    Expediteur.grid(column=1, row=1)

    label2 = Label(fenetre3, text="Objet", fg='black')
    label2.grid(column=0, row=2)
    global Obj
    Objet = Entry(fenetre3, bg='white', fg='black')
    Objet.focus_set()
    Objet.grid(column=1, row=2)

    global Champmessage
    Champmessage = Entry(fenetre3)
    Champmessage.grid(row=4, column=0, columnspan=3)

    bouton6 = Button(fenetre3, text='Ok', command=lambda: com4(Expediteur.get(), Champmessage.get(), Objet.get()))
    bouton6.grid(column=1, row=5)

    fenetre3.grid_columnconfigure(0, weight=1)
    fenetre3.mainloop()


# -------------------- Fin Interfaces ----------------
# -------------------- Sous-fenêtres -----------------
def fen_envoyer(Expediteur, Objet, Champmessage):
    global fenetreenvoyer
    global Button_send1

    fenetreenvoyer = Toplevel(fenetre)
    fenetreenvoyer.title('Fenêtre configuration envoi')
    fenetreenvoyer.geometry('250x150')
    fenetreenvoyer.transient(fenetre)

    label = Label(fenetreenvoyer, text="Email Test", fg='black')
    label.grid(column=0, row=1)

    global Champ_emailTEST
    Champ_emailTEST = Entry(fenetreenvoyer, bg='white', fg='black')
    Champ_emailTEST.focus_set()
    Champ_emailTEST.grid(column=1, row=1)

    global Button_send1
    Button_send1 = Button(fenetreenvoyer, text='Envoyer',
                          command=lambda: send_mail(Expediteur, Objet, Champmessage, Champ_emailTEST.get()))
    Button_send1.grid(column=2, row=1)

    global Button_send2
    Button_send2 = Button(fenetreenvoyer, text='Envoyer à toute la liste',
                          command=lambda: send_mail(Expediteur, Objet, Champmessage, Champ_emailTEST.get()))
    Button_send2.grid(column=1, row=10)

    fenetreenvoyer.grid_columnconfigure(0, weight=1)
    fenetreenvoyer.mainloop()


# fenetre d'import fichier CSV
def fen_import_csv():
    global fenetreimportCSV
    global ChampCSV
    fenetreimportCSV = Toplevel(fenetre)
    fenetreimportCSV.title('Import CSV')
    fenetreimportCSV.geometry('150x150')
    fenetreimportCSV.transient(fenetre)

    label = Label(fenetreimportCSV, text="Nom fichier CSV", fg='black')
    label.grid(column=0, row=1)

    global ChampCSV
    ChampCSV = Button(fenetreimportCSV, text='Import', command=lambda: com3())
    ChampCSV.grid(column=1, row=5)

    fenetreimportCSV.grid_columnconfigure(0, weight=1)
    fenetreimportCSV.mainloop()


def fen_import_url():
    global fenetreimporturl
    fenetreimporturl = Toplevel(fenetre)
    fenetreimporturl.title('Import CSV')
    fenetreimporturl.geometry('200x150')
    fenetreimporturl.transient(fenetre)

    label = Label(fenetreimporturl, text="Import URL", fg='black')
    label.grid(column=0, row=1)

    global Champurl
    Champurl = Entry(fenetreimporturl, bg='white', fg='black')
    Champurl.focus_set()
    Champurl.grid(column=0, row=2)

    bouton = Button(fenetreimporturl, text='Import', command=lambda: com2())
    bouton.grid(column=4, row=2)

    fenetreimporturl.grid_columnconfigure(0, weight=1)
    fenetreimporturl.mainloop()


# -------------------- Fin Sous-fenêtres -----------------
# -------------------- Commandes -----------------
# commandes fenetres & interfaces à executions multiples pour bouton Import URL & import CSV
def com1_bimportURL():
    fenetre2.destroy()
    fen_import_url()


def com2_bimportCSV():
    fenetre2.destroy()
    fen_import_csv()


def com3_Dedoublonner():
    doublon(ma_liste)
    fenetre2.destroy()
    Interface2()


def com2():
    crawlerWeb(Champurl.get())
    fenetreimporturl.destroy()
    Interface2()


def com3():
    recup_fichier()
    fenetreimportCSV.destroy()
    Interface2()


def com4(Expediteur, Champmessage, Objet):
    fen_envoyer(Expediteur, Champmessage, Objet)
    Interface3()


# -------------------- Fonctionnalités ----------------
def send_mail(Expediteur, Objet, Champmessage, Champ_emailTEST):
    global ma_liste

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("testpythontp1234@gmail.com", "Azerty1234!@")

    msg = text(Champmessage)
    msg[ 'From' ] = email.utils.formataddr((Expediteur, 'test'))
    msg[ 'Subject' ] = Objet

    if Champ_emailTEST != "":
        server.sendmail(Expediteur, Champ_emailTEST, msg.as_string())

    else:
        for i in range(0, len(ma_liste)):
            server.sendmail(Expediteur, ma_liste[ i ], msg.as_string())


def doublon(liste):
    global ma_liste
    if (ma_liste != ""):
        ma_liste = list(set(ma_liste))
    return ma_liste


def recup_fichier():
    global filename
    global ma_liste
    filename = askopenfilename(title="Ouvrir votre document", filetypes=[ ('csv files', '.csv'), ('all files', '.*') ])
    fichier = open(filename, "r")
    ma_liste = fichier.readlines()
    fichier.close()
    print("Liste import CSV:", ma_liste)
    return ma_liste
    # Label(fenetreimportCSV, text=content).pack(padx=10, pady=10)


def crawlerWeb(x):
    # emails test http://univcergy.phpnet.org/python/mail.html
    with urllib.request.urlopen(x) as response:
        webpage = response.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        for anchor in soup.find_all('a'):
            if ('mailto:' in anchor.get('href')):
                ma_liste.append(anchor.get('href')[ 7: ])
    print("Liste sortie du crawler :", ma_liste)
    return ma_liste
    server.quit()


# ----------------------------------------------------
# ----------------------- Main  ----------------------
Menu_principal()