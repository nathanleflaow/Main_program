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
    global heure_montage_LV
    message = str(message.payload.decode("utf-8"))
    print(str(message))
    a = message.split(";")
    identifiant.append(a[0])
    liste_portiere.append(a[0])
    heure_entree.append(a[1])
    heure_montage_LV.append(a[2])
    print(liste_portiere)


mqttBroker = "test.mosquitto.org"
client = mqtt.Client("LV")
client.connect(mqttBroker)

client.loop_start()
client.subscribe("ECAM_scanette")
client.on_message = on_message

"""Création de la fenêtre"""

root = Tk()

root.title("Montage Lève Vitre")
root.config(bg='#7F8FA6')
root.geometry("1024x744")
root.iconbitmap("Logo_ECAM_Rennes.ico")

root.columnconfigure(0, weight = 2)
root.columnconfigure(1, weight = 1)

portiere_actuelle = "?"


"""Création d'image"""

def update_image():
    global liste_portiere
    global portiere_actuelle
    position = [1,1,1,-1,-1,-1]
    i = 0
    while len(liste_portiere) == 0:
        canvas.move(point,position[i%6]*50,0)
        time.sleep(0.2)
        i += 1
        canvas.itemconfig(canvas_image,image=image_attente)
        canvas.update()
    if liste_portiere[0][0] == "1":
        portiere_actuelle = liste_portiere[0]
        canvas.itemconfig(canvas_image,image=image_avant)
        root.update()
    elif liste_portiere[0][0] == "2":
        portiere_actuelle = liste_portiere[0]
        canvas.itemconfig(canvas_image,image=image_arriere)
        root.update()

    return None

def valide():
    global heure_entree
    client.publish("ECAM_LV", str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time())
    print(str(liste_portiere[0]) + ";" + str(heure_entree[0]) + ";" + get_time())
    del liste_portiere[0]
    del heure_entree[0]
    update_image()


width = 650
height = 600
image_avant = PhotoImage(file= "Montage_LV_avant.png").zoom(1).subsample(2)
image_arriere = PhotoImage(file= "Montage_LV_arriere.png").zoom(1).subsample(2)
image_attente = PhotoImage(file= "attente.png").zoom(1).subsample(2)

"""Canvas image"""
canvas = Canvas(root, width = width, height = height, bg="#7F8FA6", highlightthickness=1)
canvas_image = canvas.create_image(width/2, height/2, image = image_attente)
point = canvas.create_oval(380,550,390,560,fill = "black")
canvas.grid(row = 1, column = 0, sticky = W, padx = 25, rowspan = 2)


# """Logo ECAM Rennes"""
image_logo_ECAM = PhotoImage(file= "Logo_ECAM_Rennes.png").zoom(1).subsample(15)
my_label = Label(root, image = image_logo_ECAM, bg='#7F8FA6')
# my_label.place(x=1, y=500)
my_label.grid(row = 2, column = 1)

label_title = Label(root, text = "Montage coulisse", font=("Helvetica", 15), bg='#7F8FA6', pady = 20)
label_title.grid(row = 0, column = 0)


"""Création bouton"""
button_valide = Button(root, text = "Valider montage", font=("Helvetica", 15), width = 15, command = valide, bg = "#13B94D")
button_valide.grid(row = 1, column = 1, pady = 250)

button_EPI1 = Button(root, text = "EPI 1", font=("Helvetica", 10), height = 2, width = 5, command = EPI)
button_EPI1.grid(row = 0, column = 1, padx = 10, pady = 21)


update_image()

root.mainloop()