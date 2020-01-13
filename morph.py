from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from scipy import ndimage
from scipy import misc
import scipy.spatial as spatial

class warp():

    def __init__(self,points,filename):
        self.points = points
        self.offset = 20
        self.delauny = []
        self.boundingbox = []
        self.result_pic = []
        self.loadimage(filename)
        self.bbox()

    def loadimage(self,imagefile):
        self.pic = Image.open(imagefile)
        self.pic = np.array(self.pic)
        self.size = self.pic.shape[:2]

    def updatePoints(self, points):
        self.points = points
        self.bbox()

    def updateExtraPoints(self,points):
        print("Add extra points outside of bbox")

    def bbox(self):
        xmin,xmax = self.points[0][:2]
        ymin,ymax = self.points[0][:2]
        xsum,ysum = [0,0]
        points = self.points
        for point in points:
                xsum = xsum + point[0]
                ysum = ysum + point[1]
                if xmin > point[0]:
                        xmin = point[0]
                elif xmax < point[0]:
                        xmax = point[0]
                if ymin > point[1]:
                        ymin = point[1]
                elif ymax < point[1]:
                        ymax = point[1]

        xmin = xmin - self.offset
        ymin = ymin - self.offset
        xmax = xmax + self.offset
        ymax = ymax + self.offset

        self.grid = np.asarray([(x, y) for y in range(int(0),int(self.size[1]-1))
                                for x in range(int(0),int(self.size[0]-1))], np.int32)

        self.bbox_size = [xmax-xmin, ymax-ymin]
        self.center = [xmin + self.bbox_size[0]/2, ymin + self.bbox_size[1]/2,'y']
        self.cog = [xsum/len(points),ysum/len(points),'o']
        self.boundingbox = [[xmin,ymin,'b'],[xmax,ymin,'b'],[xmax,ymax,'b'],[xmin,ymax,'b']]
        return self.boundingbox

    def allPoints(self,points):
        res = list(points)
        for point in self.points:
            res.append([point[1],point[0]])
        #res.append([self.cog[1],self.cog[0]])
        return res

    def getBoxes(self):
        res = []
        for point in self.boundingbox:
            res.append([point[1],point[0]])
        res.extend([[0,0],[self.size[0]-2,0],[self.size[0]-2,self.size[1]-2],[0,self.size[1]-2]])
        return res

    def biinterpolate(self,img,point):
        """
        Interpolation der Pixel aus dem quell bild
        """
        int_coords = np.int32(point)
        x, y = int_coords
        dx, dy = point - int_coords
        q11 = img[x, y]
        q21 = img[x, y+1]
        q12 = img[x+1, y]
        q22 = img[x+1, y+1]
        btm = q21.T * dx + q11.T * (1 - dx)
        top = q22.T * dx + q12.T * (1 - dx)
        inter_pixel = top * dy + btm * (1 - dy)
        return inter_pixel.T

    def warping(self,triangles,grid,img,delaunay,result):
        tri_index = delaunay.find_simplex(grid)
        for simplex in range(len(delaunay.simplices)):
            pos = grid[tri_index == simplex]
            out_coords = np.dot(triangles[simplex],
                                np.vstack((pos.T, np.ones(len(pos)))))
            x, y = pos.T
            result[x,y] = self.biinterpolate(img, out_coords)

    def triangle_matrix(self,vert,s_points,d_points):
            ones = [1, 1, 1]
            for tri_indices in vert:
                    src_tri = np.vstack((s_points[tri_indices, :].T, ones))
                    dst_tri = np.vstack((d_points[tri_indices, :].T, ones))
                    mat = np.dot(src_tri, np.linalg.inv(dst_tri))[:2, :]
                    yield mat

    def warp_steps(self,steps,spoints,dpoints):
        res = []
        points_step = []
        for point in zip(spoints,dpoints):
            line = [point[0]]
            x = (point[1][0] - point[0][0])/steps
            y = (point[1][1] - point[0][1])/steps
            for i in range(1,steps):
                line.append([point[0][0] + (i * x),point[0][1] + (i * y)])
            line.append(point[1])
            res.append(line)
        return np.array(res)

    def warp_sequence(self,o_warper,steps,dtype=np.uint8):
        """
        Start der Morphing sequence

        Für jeden zwischenschritt für die Animation:

        1. Verschiebung der einzelenen punkte berechnen
        2. Punktmenge triagunlieren (delaunay)
        3. Verzerrungs matrix berechnen
        4. Für beide Bilder aus Ursprungsbild neues Bild erzeugen

        """
        with open("testwarp.npz","w+b") as file:
            np.savez(file,self.points,o_warper.points)

        points = self.warp_steps(steps,o_warper.allPoints(o_warper.getBoxes()),self.allPoints(self.getBoxes()))
        step1 = self.warp_points(steps,points,np.copy(self.pic),np.copy(o_warper.pic),list())

        #points2 = self.warp_steps(steps,self.allPoints(self.getBoxes()),o_warper.allPoints(self.pointse[0]))
        #img1 = step1[1]
        #img2 = step1[0]
        #points = self.warp_steps(steps,self.allPoints(self.getBoxes()),o_warper.allPoints(o_warper.getBoxes()))
        #step2 = self.warp_points(steps,points,np.copy(img1),np.copy(img2),step1)
        return step1

    def warp_points(self,steps,points,img1,img2,results):
        dpoints = []
        print(points.shape)
        images = results
        spoints = points[:,0,:2]
        epoints = points[:,steps,:2]
        self.pointse = [spoints,epoints]
        result_img = np.copy(img1)
        oresult_img = np.copy(img2)
        for i in range(0,steps):
            dpoints = points[:,i,:2]
            delaunay = spatial.Delaunay(dpoints)
            #Wird später zum erstellen der Plots benötigt
            self.delauny.append([delaunay,np.copy(dpoints)])

            triangles = np.asarray(list(self.triangle_matrix(
                delaunay.simplices, spoints , dpoints)))

            trianglesd = np.asarray(list(self.triangle_matrix(
                delaunay.simplices, epoints , dpoints)))

            self.warping(trianglesd, self.grid,img1, delaunay, result_img)
            self.warping(triangles,self.grid,img2, delaunay, oresult_img)
            images.extend([np.copy(oresult_img),np.copy(result_img)])
        return images

def test():
    import matplotlib.pyplot as plt
    import pickle

    testdata = np.load("testwarp25.npz")
    plt1 = warp(testdata['arr_0'][ : ,:2].astype(np.float),"angela-merkel.jpg")
    plt2 = warp(testdata['arr_1'][ : ,:2].astype(np.float),"Horst-Seehofer.jpg")

    pics = plt1.warp_sequence(plt2,5)

    plt3 = warp(testdata['arr_0'][ : ,:2].astype(np.float),"angela-merkel.jpg")
    plt4 = warp(testdata['arr_1'][ : ,:2].astype(np.float),"Horst-Seehofer.jpg")

    animation = plt3.warp_sequence(plt4,10)
    ani = []
    print(len(animation))
    for i in range(0,len(animation),2):
        ani.append([np.copy(animation[i]),np.copy(animation[len(animation) - 1 -i ])])

    exportGIFFile(ani,"animation.gif")
    plotextra(pics,plt1,plt2)

def plotextra(pics,plt1,plt2):
    fig,axs = plt.subplots(2,3,sharey=True,sharex=True,figsize=(9,8))
    ax = fig.axes
    j = 0
    animation = []
    anum = 0
    for i in range(0,len(pics),2):
        if j < 3:
            ax[j].imshow(np.copy(pics[i]))
            ax[j + 3].imshow(np.copy(pics[i+1]))
        animation.append([np.copy(pics[i]),np.copy(pics[len(pics) - 1 -i ])])
        j = j +1

    ax[2].imshow(np.copy(pics[-2]))
    ax[2+ 3].imshow(np.copy(pics[-1]))
    j = 0
    plt.tight_layout()
    fig.show()
    fig.savefig("morphing_einzeln.jpg")
    fig,axs = plt.subplots(2,5,sharey=True,sharex=True,figsize=(15,5))
    fig3,ax3 = plt.subplots(2,5,figsize=(15,5))
    ax = fig.axes
    anum =5
    ep = plt1.pointse[0]
    sp = plt1.pointse[1]
    for tri in plt1.delauny:
        if j < 5:
            print(tri[1])

            ax[anum + j].triplot(tri[1][:,1],tri[1][:,0],tri[0].simplices.copy(),linewidth=0.5,linestyle='dashed',color='red')
            ax[anum + j].plot(tri[1][:,1],tri[1][:,0], 'o')
            ax[anum + j].plot(sp[:,1],sp[:,0], 'x')

            ax3[0][j].triplot(ep[:,1],ep[:,0] ,tri[0].simplices.copy(),linewidth=0.5,linestyle='dashed',color='red')
            ax3[0][j].plot(ep[:,1],ep[:,0], 'o')
            ax3[0][j].plot(sp[:,1],sp[:,0], 'x')

            ax3[1][j].plot(tri[1][:,1],tri[1][:,0], 'x')
            ax3[1][j].plot(sp[:,1],sp[:,0], 'o')
            ax3[1][j].plot(ep[:,1],ep[:,0], 'o')
            ax3[1][j].set_xlim(xmin=200,xmax=500)
            ax3[1][j].set_ylim(ymin=100,ymax=500)
        j = j + 1
    fig3.savefig("delauny.jpg")
    j = 0
    anum = 5
    linear  = np.linspace(0,1,len(animation))
    fig2,ax2 = plt.subplots(2,5,sharey=True,figsize=(15,5))

    for frame in zip(animation,linear):
        if j < 5:
            ax[ j].imshow(np.array(frame[1] * frame[0][1] + (1-frame[1]) * frame[0][0]).astype(np.uint8))
            ax[anum + j].imshow(np.array(frame[1] * frame[0][1] + (1-frame[1]) * frame[0][0]).astype(np.uint8))

            fig2.axes[ j].imshow(np.array(frame[1] * frame[0][0] + (1-frame[1]) * frame[0][1]).astype(np.uint8))
            fig2.axes[anum + j].imshow(np.array(frame[1] * frame[0][1] + (1-frame[1]) * frame[0][0]).astype(np.uint8))
        j = j+1
    plt.tight_layout()
    fig.savefig("morphing überblenden.jpg")
    fig2.savefig("morphing2")
    plt.show()


def exportGIFFile(pics,filename):
        print("Exporting gif")
        frames = []
        linear  = np.linspace(0,1,len(pics))
        for frame in zip(pics,linear):
            img1 = np.array(frame[1] * frame[0][1] + (1-frame[1]) * frame[0][0]).astype(np.uint8)
            frames.append(Image.fromarray(img1))
        pics.reverse()
        for frame in zip(pics,linear):
            img = np.array(frame[1] * frame[0][0] + (1-frame[1]) * frame[0][1]).astype(np.uint8)
            frames.append(Image.fromarray(img))

        frames[0].save(filename, format='GIF', append_images=frames[1:], save_all=True, duration=150, loop=0)
        frames[0].save(filename.rstrip("gif") + "webp", format='WebP', append_images=frames[1:], save_all=True, duration=150, loop=0)

if __name__ == "__main__":
    test()
