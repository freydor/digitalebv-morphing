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

    def allPoints(self):
        res = []
        for point in self.points:
            res.append([point[1],point[0]])
        res.append([self.cog[1],self.cog[0]])
        for point in self.boundingbox:
            res.append([point[1],point[0]])
        res.extend([[0,0],[self.size[0]-2,0],[self.size[0]-2,self.size[1]-2],[0,self.size[1]-2]])
        return res

    def biinterpolate(self,img,point):
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
            result[x,y] = np.ndarray.copy(self.biinterpolate(img, out_coords))

    def triangle_matrix(self,vert,s_points,d_points):
            ones = [1, 1, 1]
            for tri_indices in vert:
                    src_tri = np.vstack((s_points[tri_indices, :].T, ones))
                    dst_tri = np.vstack((d_points[tri_indices, :].T, ones))
                    mat = np.dot(src_tri, np.linalg.inv(dst_tri))[:2, :]
                    yield mat

    def warp_steps(self,steps,o_warper):
        spoints = self.allPoints()
        dpoints = o_warper.allPoints()
        res = []
        points_step = []
        for point in zip(spoints,dpoints):
            line = [point[0]]
            x = (point[1][0] - point[0][0])/steps
            y = (point[1][1] - point[0][1])/steps
            line.append([x,y])
            res.append(line)
        return res

    def warp_sequence(self,o_warper,steps,dtype=np.uint8):
        points = self.warp_steps(steps,o_warper)
        with open("testwarp1.npz","w+b") as file:
            np.savez(file,self.points,o_warper.points)
        images = []
        result_img = np.copy(o_warper.pic)
        oresult_img = np.copy(self.pic)
        for i in range(0,steps):
            spoints = []
            dpoints = []
            num_chans = 3
            for point in points:
                dpoints.append([point[0][0] + (i+1)*point[1][0],point[0][1] + (i+1)*point[1][1]])
                spoints.append([point[0][0] + i*point[1][0],point[0][1] + i*point[1][1]])
            dpoints = np.array(dpoints)
            spoints = np.array(spoints)
            delaunay = spatial.Delaunay(dpoints)
            delaunay_s = spatial.Delaunay(spoints)
            self.delauny.append([delaunay_s,delaunay])

            triangles = np.asarray(list(self.triangle_matrix(
                delaunay.simplices, spoints , dpoints)))

            trianglesd = np.asarray(list(self.triangle_matrix(
                delaunay.simplices, dpoints , spoints)))

            self.warping(triangles, self.grid,np.copy(result_img), delaunay, result_img)
            self.warping(trianglesd,self.grid,np.copy(oresult_img), delaunay, oresult_img)
            images.extend([np.copy(oresult_img),np.copy(result_img)])
        return images

def test():
    import matplotlib.pyplot as plt
    import pickle
    fig,ax = plt.subplots(5,10,sharey='row',figsize=(25,5))
    fig.subplots_adjust(left=0.1, bottom=0, right=0.9, top=0.9,hspace=0.01,wspace=0.1)
    testdata = np.load("testwarp1.npz")
    plt1 = warp(testdata['arr_0'][ : ,:2].astype(np.float),"angela-merkel.jpg")
    plt2 = warp(testdata['arr_1'][ : ,:2].astype(np.float),"Horst-Seehofer.jpg")
    pics = plt1.warp_sequence(plt2,9)
    points = plt1.warp_steps(3,plt2)

    plotextra(pics,ax)
    j = 0
    for tri in plt1.delauny:
        print(tri)
        if j < 10:
            spatial.delaunay_plot_2d(tri[1],ax[4][j])
        j = j + 1
    plt.show()

def plotextra(pics,ax):
        j = 0
        for i in range(0,len(pics),2):
            if j < 10:
                ax[0][j].imshow(np.copy(pics[i]))
                ax[1][j].imshow(np.copy(pics[i+1]))
                img = np.copy(pics[i])
                ax[2][j].imshow(img.astype(np.uint8))
            j = j +1


if __name__ == "__main__":
    test()
