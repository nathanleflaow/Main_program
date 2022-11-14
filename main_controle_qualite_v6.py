"""
Programme qui :
    - reçoit la liste des portières
    - affiche les gamme portière avant, arrière ou attendre prochaine portiere
    - demande à l'opérateur : conforme/non conforme
        - si non conforme : retouché ou rebut
    - envoie un message MQTT avec n° pièce (1 = avant, 2 = arrière) et dit si elle était conforme ou non conforme
"""

from tkinter import *
import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

identifiant = []
liste_portiere = []
heure_entree = []

"""Fonction pour obtenir l'heure"""
def get_time():
    temps = time.localtime()
    date = str(temps[3]) + ":" + str(temps[4]) + ":" + str(temps[5]) + ":" + str(temps[2]) + ":" + str(temps[1]) + ":" + str(temps[0])
    return date


"""Récéption message MQTT de la scanette"""
def on_message(client, userdata, message):
    global identifiant
    global heure_entree
    global liste_portiere
    message = str(message.payload.decode("utf-8"))
    print(str(message))
    a = message.split(";")
    identifiant.append(a[0])
    liste_portiere.append(a[0])
    heure_entree.append(a[1])
    print(liste_portiere)


mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Controle_qualite")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("ECAM_scanette")
client.on_message = on_message

"""Création de la fenêtre"""

root = Tk()

root.title("Contrôle qualité")
# root.geometry('1950x950')
root.config(bg='#7F8FA6')
# root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.geometry("1024x744")
# root.iconbitmap("C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/Logo_ECAM_Rennes.ico")

root.columnconfigure(0, weight = 2)
root.columnconfigure(1, weight = 1)

portiere_actuelle = "?"

"""Création d'image"""
incrementation = 0
def update_image():
    global liste_portiere
    global portiere_actuelle
    global incrementation
    position = [1,1,1,-1,-1,-1]

    while len(liste_portiere) == 0:
        canvas.itemconfigure(point, state='normal')
        canvas.move(point,position[incrementation%6]*50,0)
        time.sleep(0.2)
        incrementation += 1
        canvas.itemconfig(canvas_image,image=image_attente)
        canvas.update()
    if liste_portiere[0][0] == "1":
        canvas.itemconfigure(point, state='hidden')
        portiere_actuelle = liste_portiere[0]
        canvas.itemconfig(canvas_image,image=image_avant)
        root.update()
    elif liste_portiere[0][0] == "2":
        canvas.itemconfigure(point, state='hidden')
        portiere_actuelle = liste_portiere[0]
        canvas.itemconfig(canvas_image,image=image_arriere)
        root.update()

    return None

def conforme():
    global heure_entree
    client.publish("ECAM_qualite", str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "conforme")
    print(str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "conforme")
    del liste_portiere[0]
    del heure_entree[0]
    canvas.itemconfig(canvas_image,image=image_portiere_validee)
    canvas.update()
    time.sleep(2)
    update_image()

def non_conforme():
    global heure_entree
    button_conforme.config(text = "Retouché", command = retouche, bg = "orange")
    button_non_conforme.config(text = "Rebut", command = rebut)
    root.update()

def retouche():
    global heure_entree
    button_conforme.config(text = "Conforme", command = conforme, bg = "#13B94D")
    button_non_conforme.config(text = "Non conforme", command = non_conforme)
    client.publish("ECAM_qualite", str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "retouche")
    print(str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "retouche")
    del heure_entree[0]
    del liste_portiere[0]
    canvas.itemconfig(canvas_image,image=image_portiere_validee)
    canvas.update()
    time.sleep(2)
    update_image()

def rebut():
    global heure_entree
    button_conforme.config(text = "Conforme", command = conforme, bg = "#13B94D")
    button_non_conforme.config(text = "Non conforme", command = non_conforme)
    client.publish("ECAM_qualite", str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "rebut")
    print(str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time() + ";" + "rebut")
    del heure_entree[0]
    del liste_portiere[0]
    canvas.itemconfig(canvas_image,image=image_portiere_validee)
    canvas.update()
    time.sleep(2)
    update_image()


width = 600
height = 600
image_avant = PhotoImage(file= "C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/porte_avant_qualite.png").zoom(1).subsample(1)
image_arriere = PhotoImage(file= "C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/porte_arriere_qualite.png").zoom(1).subsample(1)
image_attente = PhotoImage(file= "C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/attente.png").zoom(1).subsample(1)
image_portiere_validee = PhotoImage(file= "C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/portiere_validee.png").zoom(1).subsample(1)


"""Canvas image"""
canvas = Canvas(root, width = width, height = height, bg="#7F8FA6", highlightthickness=1)
canvas_image = canvas.create_image(width/2, height/2, image = image_attente)
point = canvas.create_oval(230,450,240,460,fill = "black")
canvas.grid(row = 1, column = 0, sticky = W, padx = 25, rowspan = 3)



# """Logo ECAM Rennes"""
image_logo_ECAM = PhotoImage(file= "C:/Users/natha/Desktop/ECAM/ECAM/Usine_4.0/Programmes_Python/Main_program/Logo_ECAM_Rennes.png").zoom(1).subsample(14)
my_label = Label(root, image = image_logo_ECAM, bg='#7F8FA6')
# my_label.place(x=1, y=500)
my_label.grid(row = 3, column = 2,columnspan = 3, sticky = "SE")

label_title = Label(root, text = "Contrôle qualité", font=("Helvetica", 20), bg='#7F8FA6', pady = 14)
label_title.grid(row = 0, column = 0)


"""Création bouton"""
button_conforme = Button(root, text = "Conforme", font=("Helvetica", 15), width = 15, height = 2, command = conforme, bg = "#13B94D")
button_conforme.grid(row = 1, column = 1, pady = 100, columnspan = 3)

button_non_conforme = Button(root, text = "Non conforme", font=("Helvetica", 15), height = 2, width = 15, bg = "#EA223C", command = non_conforme)
button_non_conforme.grid(row = 2, column = 1, pady = 0, columnspan = 3)

button_EPI1 = Button(root, text = "EPI 1", font=("Helvetica", 10), height = 2, width = 5)
button_EPI1.grid(row = 0, column = 1, padx = 10, pady = 21)

button_EPI2 = Button(root, text = "EPI 2", font=("Helvetica", 10), height = 2, width = 5)
button_EPI2.grid(row = 0, column = 2, padx = 10, pady = 21)

button_EPI3 = Button(root, text = "EPI 3", font=("Helvetica", 10), height = 2, width = 5)
button_EPI3.grid(row = 0, column = 3, padx = 10, pady = 21)

update_image()
#frame.pack(expand = YES)

root.mainloop()