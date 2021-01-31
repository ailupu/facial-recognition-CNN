import numpy as np
import os
import random
import cv2
import pickle

crop = []
lbp_imagini = []
etichete_imagini = list()

#path-ul catre directorul cu baza de date
curent_dir = os.getcwd()
img_dir = os.path.join(curent_dir, "gt_db")

folder = ""
etichete = 0
l_hist_imag = list()

#nuamrul de imagini care sunt alocate pentru antrenare
nr = 11

etichete_total = list()

lbp_antrenare = list()
etichete_antrenare = list()

lbp_testare = list()
etichete_testare = list()

lista_imagini = list()
tuplu_random = 0
lista_toate = list()
print(len(os.listdir(img_dir)))

#se parcurge baza de date si se aleg aleator 11 imagini pentru antrenare si 4 imagini pentru testare
#pentru fiecare imagine se alege si o eticheta prin care persoana este recunoscută

for subfolder in os.listdir(img_dir):
    print(subfolder)
    os.chdir(img_dir + "/" + subfolder)
    etichete = int(subfolder[1:]) - 1
    etichete_imagini = list()

    for h_imag in os.listdir("."):
        # imaginile terminate cu crop.jpg sunt fetele decupate
        # imaginile cu extensia lbp.jpg sunt fetele procesate cu lbp
        if h_imag.endswith('crop.jpg'):
            print(h_imag)
            img_crt = cv2.imread(h_imag, 0)
            lista_imagini.append(img_crt)
            lista_toate.append(img_crt)

            etichete_imagini.append(etichete)
            etichete_total.append(etichete)

    tuplu_random = random.sample(list(enumerate(lista_imagini)), nr)

    index = list()
    valori = list()

    for idx, val in tuplu_random:
        index.append(idx)
        lbp_antrenare.append(val)
        etichete_antrenare.append(etichete_imagini[idx])

    index.sort()
    for x in range(0, 15):
        if x not in index:
            etichete_testare.append(etichete_imagini[x])
            lbp_testare.append(lista_imagini[x])

    tuplu_random = list()
    lista_imagini = list()
    etichete_imagini = list()

# Salvare date pentru cazul lbp

# lbp_antrenare = np.array(lbp_antrenare)
# with open("lbp_antrenare.txt", 'wb') as f:
#     pickle.dump(lbp_antrenare, f)
#
# lbp_testare = np.array(lbp_testare)
# with open("lbp_testare.txt", 'wb') as f1:
#     pickle.dump(lbp_testare, f1)
#
# etichete_antrenare = np.array(etichete_antrenare)
# with open("etichete_antrenare.txt", 'wb') as f2:
#     pickle.dump(etichete_antrenare, f2)
# print(etichete_antrenare)
#
# etichete_testare = np.array(etichete_testare)
# with open("etichete_testare.txt", 'wb') as f3:
#     pickle.dump(etichete_testare, f3)



# Salvare pentru cazul imaginilor simple (fara filtrare cu lbp)

lbp_antrenare = np.array(lbp_antrenare)
with open("crop_antrenare.txt", 'wb') as f:
    pickle.dump(lbp_antrenare, f)

print(lbp_antrenare)
lbp_testare = np.array(lbp_testare)
with open("crop_testare.txt", 'wb') as f1:
    pickle.dump(lbp_testare, f1)

etichete_antrenare = np.array(etichete_antrenare)
with open("crop_etichete_antrenare.txt", 'wb') as f2:
    pickle.dump(etichete_antrenare, f2)
print(etichete_antrenare)

etichete_testare = np.array(etichete_testare)
with open("crop_etichete_testare.txt", 'wb') as f3:
    pickle.dump(etichete_testare, f3)
