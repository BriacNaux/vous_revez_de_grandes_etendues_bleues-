import csv
from csv import writer
import tkinter


# filename = 'Liste_des_noms_et_images.csv'

# header = ['nom', 'image']
# data = []


# with open(filename, 'w', newline="") as file :
#     csvwriter = csv.writer(file)
#     csvwriter.writerow(header)
#     csvwriter.writerows(data)

def saveName(choosenName, photo) :

  


    newData = []
    newData.append(choosenName)
    newData.append(photo)

    with open('Liste_des_noms_et_images.csv', 'a') as f_object :

        writer_object = writer(f_object)
        writer_object.writerow(newData)
        f_object.close


