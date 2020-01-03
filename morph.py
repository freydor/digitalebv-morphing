from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from scipy import ndimage
from scipy import misc

fig = plt.figure(tight_layout=True)
Path = mpath.Path
gs = gridspec.GridSpec(3, 2)


class FacePair():
    hpoints = {
        "heyes" : [
            (302,192),
            (88,4),
        ],
        "hnose" : [
            (342,194),
            (-3,73),
        ]}
    meyes = [
        (310,235),
        (107,10)
    ]
    mnose = [
        (370,237),
        (2,70)
    ]
    def loadimage(imagefile):
        pic = Image.open(imagefile)
        pix = np.array(pic)
        return pix

def setplot(pix1,pix2):

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax1.imshow(pix1)
    ax1.set_title("horst")
    ax1.arrow(heyes[0][0],heyes[0][1],heyes[1][0],heyes[1][1], head_width=5.5, head_length=5.1, fc='k', ec='k')
    ax1.arrow(hnose[0][0],hnose[0][1],hnose[1][0],hnose[1][1],head_length=5.1, fc='k', ec='k')
    ax2.imshow(pix2)
    ax2.set_title("merkel")
    ax2.arrow(meyes[0][0],meyes[0][1],meyes[1][0],meyes[1][1], head_width=5.5, head_length=5.1, fc='k', ec='k')
    ax2.arrow(mnose[0][0],mnose[0][1],mnose[1][0],mnose[1][1], head_width=5.5, head_length=5.1, fc='k', ec='k')

def scalediff(vec1, vec2,ax):
    length1 = np.sqrt(np.power(vec1[1][0],2) + np.power(vec1[1][1],2))
    length2 = np.sqrt(np.power(vec2[1][0],2) + np.power(vec2[1][1],2))
    ratio = length1/length2
    nlength1 = (vec1[1][0]/length1, vec1[1][1]/length1)
    nlength2 = (vec2[1][0]/length2, vec2[1][1]/length2)
    ax.plot([0,nlength1[0]],[0,nlength1[1]], '-x',label="Horst")
    ax.plot([0,nlength2[1]],[0,nlength2[1]], '-o',label="Merkel")
    ax.legend()
    theta1 = np.arccos(nlength1[0])
    theta2 = np.arccos(nlength2[0])
    print("Normvektor 1: {} Vektor: {} Winkel (rad): {} \nNormvektor 2: {} Vektor: {} Winkel: {} \nVerhältnis: {} Winkel: {} ".format(nlength1,vec1[1], theta1 ,nlength2,vec2[1], theta2 , ratio , theta1-theta2) )
    return (ratio,theta1-theta2)

def rotate(img,theta):
    #c, s = np.cos(theta), np.sin(theta)
    #R = np.array(((c,-s),(s,c)))

    theta = np.pi/6
    matrot = [
        [np.cos(theta),-np.sin(theta),0],
        [np.sin(theta),np.cos(theta),0],
        [0,0,1],
    ]
    return np.matmul(R,img)


horst = loadimage("Horst-Seehofer.jpg")
merkel = loadimage('angela-merkel.jpg')
bhorst = horst.copy()
setplot(bhorst,merkel)
print("Skalierung Augenabstand hort->merkel")
ax1 = fig.add_subplot(gs[1, 0])
ax1.set_title("Augenabstand")
rotscale = scalediff(heyes,meyes,ax1)

print("Skalierung der Nase hort->merkel")
ax2 = fig.add_subplot(gs[1, 1])
ax2.set_title("Nase")
scalediff(hnose,mnose,ax2)

plt.show()
