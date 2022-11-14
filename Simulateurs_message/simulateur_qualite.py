import paho.mqtt.client as mqtt
from random import randrange, uniform, randint
import time


#print(time.asctime())
date = time.localtime()
annee = date[0]
mois = date[1]
jour = date[2]
heure = date[3]
minute = date[4]
secondes = date[5]

mqttBroker = "test.mosquitto.org"
client = mqtt.Client("Scanette_NLF")
client.connect(mqttBroker)

def get_time():
    temps = time.localtime()
    date = str(temps[3]) + ":" + str(temps[4]) + ":" + str(temps[5]) + ":" + str(temps[2]) + ":" + str(temps[1]) + ":" + str(temps[0])
    return date
heure_debut = get_time()

heure_entree = "14:57:33:8:11:2022"
heure_M1 = "14:57:34:8:11:2022"
heure_M2 = "14:57:35:8:11:2022"
min_entree = heure_entree[4]
min_M1 = heure_M1[4]
min_M2 = heure_M2[4]
i = 1
while True:
    global heure_entree
    global heure_M1
    global heure_M2
    id = ""
    id += str(randint(1, 2))
    id += str(randint(0, 9))
    id += str(randint(0, 9))
    id += str(randint(0, 9))
    id += str(randint(0, 9))

    heure_entree[4] = str(int(heure_entree[4]) + i)
    heure_M1[4] = str(int(heure_M1[4]) + i)
    heure_M2[4] = str(int(heure_M2[4]) + i)


    #randNumber = randint(1, 2)
    #start = time.time()
    time.sleep(randint(5,6))
    #stop = time.time()
    #delta_t = stop - start
    heure_entree = get_time()
    message = str(id) + ";" + heure_entree + ";" + heure_M1 + ";" + heure_M2 + ";" + str(heure_entree)
    client.publish("ECAM_qualite", message)
    print(str(message))