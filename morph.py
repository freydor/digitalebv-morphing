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
    result_pic = []
    boundingbox = []

    def __init__(self,points,filename):
        self.points = points
        self.offset = 20
        self.delauny = []
        self.loadimage(filename)
        self.bbox()

    def loadimage(self,imagefile):
        self.pic = Image.open(imagefile)
        self.pic = np.array(self.pic)
        self.size = self.pic.shape[:2]

    def updatePoints(self, points):
        self.points = points
        self.bbox()


    def bbox(self):
        xmin = self.points[0][0]
        xmax = self.points[0][0]
        ymin = self.points[0][1]
        ymax = self.points[0][1]
        xsum = 0
        ysum = 0
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
        print("Grid size: {} ".format(self.size))
        self.bbox_size = [xmax-xmin, ymax-ymin]
        self.center = [xmin + self.bbox_size[0]/2, ymin + self.bbox_size[1]/2,'y']
        self.cog = [xsum/len(points),ysum/len(points),'o']
        self.boundingbox = [[xmin,ymin,'b'],[xmax,ymin,'b'],[xmax,ymax,'b'],[xmin,ymax,'b']]
        return self.boundingbox

    def scale(self,w,h):
        w_ratio = w/self.size[0]
        h_ratio = h/self.size[1]
        if w_ratio > h_ratio :
            return w_ratio
        else:
            return h_ratio

    def biinterpolate(self,img,point):
            int_coords = np.int32(point)
            y, x = int_coords
            dx, dy = point - int_coords
            q11 = img[y, x]
            q21 = img[y, x+1]
            q12 = img[y+1, x]
            q22 = img[y+1, x+1]
            btm = q21.T * dx + q11.T * (1 - dx)
            top = q22.T * dx + q12.T * (1 - dx)
            inter_pixel = top * dy + btm * (1 - dy)
            return inter_pixel.T

    def warping(self,triangles,o_warper,delaunay,result,oresult):
        grid = o_warper.grid
        print(grid)
        tri_index = delaunay.find_simplex(o_warper.grid)
        for simplex in range(len(delaunay.simplices)):
            pos = grid[tri_index == simplex]
            out_coords = np.dot(triangles[simplex],
                                np.vstack((pos.T, np.ones(len(pos)))))
            x, y = pos.T
            #print("pos: {},out: {},".format(len(x),len(y)))
            result[x,y] = np.ndarray.copy(self.biinterpolate(self.pic, out_coords))
            oresult[x,y] = np.ndarray.copy(self.biinterpolate(o_warper.pic, out_coords))

    def triangle_matrix(self,vert,s_points,d_points):
            ones = [1, 1, 1]
            for tri_indices in vert:
                    src_tri = np.vstack((s_points[tri_indices, :].T, ones))
                    dst_tri = np.vstack((d_points[tri_indices, :].T, ones))
                    mat = np.dot(src_tri, np.linalg.inv(dst_tri))[:2, :]
                    yield mat

    def getPoints(self,points):
        res = []
        for point in points:
            res.append([point[0],point[1]])
        return res

    def allPoints(self):
        res = []
        for point in self.points:
            res.append([point[1],point[0]])
        res.append([self.cog[1],self.cog[0]])
        for point in self.boundingbox:
            res.append([point[1],point[0]])
        # res.append([0,0])
        # res.append([self.size[0]-2,0])
        # res.append([self.size[0]-2,self.size[1]-2])
        # res.append([0,self.size[1]-2])
        return res

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
        for i in range(0,steps):
            spoints = []
            dpoints = []
            num_chans = 3
            #            result_img = np.zeros((self.pic.shape[0],self.pic.shape[1], num_chans), dtype)
            #            oresult_img = np.zeros((self.pic.shape[0],self.pic.shape[1], num_chans), dtype)
            result_img = np.copy(self.pic)
            oresult_img = np.copy(o_warper.pic)
            for point in points:
                dpoints.append([point[0][0] + (i+1)*point[1][0],point[0][1] + (i+1)*point[1][1]])
                spoints.append([point[0][0] + i*point[1][0],point[0][1] + i*point[1][1]])
            dpoints = np.array(dpoints)
            spoints = np.array(spoints)
            delaunay = spatial.Delaunay(dpoints)
            self.delauny.append([spatial.Delaunay(spoints),delaunay])
            print("Line: {} -> {}".format(dpoints,delaunay.simplices))
            triangles = np.asarray(list(self.triangle_matrix(
                delaunay.simplices, spoints , dpoints)))
            self.warping(triangles, o_warper, delaunay, result_img, oresult_img)

            images.extend([oresult_img,result_img])
        return images

    def warp_img(self,o_warper, dtype=np.uint8):
        num_chans = 3
        #src_img = src_img[:, :, :3]
        #rows, cols = dest_shape[:2]
        result_img = np.zeros((self.pic.shape[0],self.pic.shape[1], num_chans), dtype)
        dpoints = np.array(o_warper.allPoints())
        spoints = np.array(self.allPoints())
        delaunay = spatial.Delaunay(dpoints)
        triangles = np.asarray(list(self.triangle_matrix(
            delaunay.simplices, spoints , dpoints)))

        self.warping( triangles, o_warper, delaunay,result_img)

        return result_img

def test():
    import matplotlib.pyplot as plt
    import pickle
    fig,ax = plt.subplots(5,10,sharey='row',figsize=(25,5))
    fig.subplots_adjust(left=0.1, bottom=0, right=0.9, top=0.9,hspace=0.01,wspace=0.1)
    testdata = np.load("testwarp1.npz")
    plt1 = warp(testdata['arr_0'][ : ,:2].astype(np.float),"angela-merkel.jpg")
    plt2 = warp(testdata['arr_1'][ : ,:2].astype(np.float),"Horst-Seehofer.jpg")
    pics = plt1.warp_sequence(plt2,8)
    points = plt1.warp_steps(3,plt2)

    # for i in range(0,3):
    #     spoints = []
    #     dpoints = []
    #     for point in points:
    #         spoints.append([point[0][0] + i*point[1][0],point[0][1] + i*point[1][1]])
    #         dpoints.append([point[0][0] + i+1*point[1][0],point[0][1] + i+1*point[1][1]])
    #     dpoints = np.array(dpoints)
    #     spoints = np.array(spoints)
    #     d1 = spatial.Delaunay(dpoints)
    #     d2 = spatial.Delaunay(spoints)
    #    dfig = spatial.delaunay_plot_2d(d1)
    #    dfig = spatial.delaunay_plot_2d(d2)
    plotextra(pics,ax)
    j = 0
    for tri in plt1.delauny:
        print(tri)
        spatial.delaunay_plot_2d(tri[0],ax[3][j])
        spatial.delaunay_plot_2d(tri[1],ax[4][j])
        j = j + 1
    plt.show()
    #for i in range(0,9):
    #    plt.subplot(3,3,i+1,label=str(i))
    #    plt.imshow(pics[i])

def plotextra(pics,ax):
        print(pics)
        j = 0
        for i in range(0,len(pics),2):
            if j < 10:
                ax[0][j].imshow(np.copy(pics[i]))
                ax[1][j].imshow(np.copy(pics[i+1]))
                img = (j/10) *np.copy(pics[i]) + (1-(j/10))* np.copy(pics[i+1])
                ax[2][j].imshow(img.astype(np.uint8))
            j = j +1

if __name__ == "__main__":
    test()
