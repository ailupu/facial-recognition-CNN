from face_utils import rect_to_bb
from lbp_7x7 import lbp_7x7
import cv2
import dlib
import os
import copy
from PIL import Image

#apelare librarie dlib
#este nevoie ca in acelasi fisier sa existe shape_predictor_68_face_landmarks.dat
detector = dlib.get_frontal_face_detector()
crop = []
lbp_imagini = []
l_imag = list()
l_hist_imag = list()

#path-ul spre baza de date
curent_dir = os.getcwd()
img_dir = os.path.join(curent_dir, "gt_db")

folder = ""
cnt_imagini_total = 0

for subfolder in os.listdir(img_dir):
    print(subfolder)
    os.chdir(os.path.join(img_dir, subfolder))

    for imagini in os.listdir("."):
        if imagini.endswith('jpg') and not imagini.endswith('crop.jpg') and not imagini.endswith('lbp.jpg'):
            print(imagini)

            folder += subfolder
            folder += " "
            folder += imagini

            img_data = cv2.imread(os.path.join(img_dir, subfolder, imagini), 0)

            #detectia fetei folosind libraria dlib
            rects = detector(img_data, 1)
            histograma = 0

            for (i, rect) in enumerate(rects):
                if imagini.endswith(".jpg") and not imagini.endswith('crop.jpg') and not imagini.endswith('lbp.jpg'):
                    #se deseneaza dreptunghiul care incadreaza fata si apoi se decupeaza imaginea
                    (x, y, w, h) = rect_to_bb(rect)
                    b = cv2.rectangle(img_data, (x, y), (x + w, y + h), 10, 0)
                    c = b[y:y + h, x:x + w]

                    try:
                        #imaginile se redimensioneaza la 154x154 pixeli
                        c = cv2.resize(c, (154, 154))
                        c1 = copy.deepcopy(c)

                        #salvare imagini cu niveluri de gri si doar cu fata persoanei 
                        IMAG_normal = Image.fromarray(c)
                        IMAG_normal.save(subfolder + "_" + imagini[0:-4] + "_" + "crop.jpg")

                        #calculul modelului local binar pe 7x7 blocuri si salvarea imaginilor in baza de date
                        lbp = lbp_7x7(c, c1)
                        IMAG = Image.fromarray(lbp)
                        IMAG.save(subfolder + "_" + imagini[0:-4] + "_" + "lbp.jpg")

                        cnt_imagini_total += 1

                        lbp = 0
                        folder = ""

                    except Exception as eroare:
                        print(img_data)
                        print(eroare)
