import os
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, atan, pi
from PIL import Image


def rectangle_with_angle(x, y, w, h, angle):

    xv=[x, x+w, x+w, x, x]
    yv=[y, y, y+h, y+h, y]

    xv = [i - x for i in xv]
    yv = [i - y for i in yv]

    R = np.array([xv, yv])

    alpha = angle * 2 * np.pi / 360
    rotation_matrix = np.array([[np.cos(alpha), -np.sin(alpha)], [np.sin(alpha), np.cos(alpha)]])
    XY = np.matmul(rotation_matrix, R)

    # XY = XY + np.array([[x]*5, [y]*5])
    XY = XY + np.tile(np.array([[x], [y]]), (1, 5))

    plt.plot(XY[0,:],XY[1,:], color='r', linewidth=2)
    # plt.axis([0, 640, 0, 480])
    
    return XY

# set up path
imgDataDir = 'data/Images/'
annoDataDir = 'data/Annotations/'
imgFiles = [f for f in sorted(os.listdir(imgDataDir)) if f.endswith('.png')]

# main loop
for imgidx in range(len(imgFiles)):
    # open image and annotation 
    imgName = imgFiles[imgidx]
    imgname, _ = os.path.splitext(imgName)
    im = Image.open(os.path.join(imgDataDir, imgName))
    annofile = open(os.path.join(annoDataDir, imgname + '_annotations.txt'), 'w')

    # open gui
    fig, ax = plt.subplots(1)
    ax.imshow(im)

    coords = []
    width_angle = []

    def onclick(event):
        x = event.xdata
        y = event.ydata
        coords.append((x, y))

        if len(coords) == 1:
            ax.plot(x, y, 'ro', markersize=2)
            fig.canvas.draw()
        elif len(coords) == 2:
            x2, y2 = coords[1]
            x1, y1 = coords[0]
            width = sqrt((x1-x2)**2 + (y1-y2)**2)
            angle = atan((y2-y1)/(x2-x1))
            angle = angle/pi*180
            width_angle.append(width)
            width_angle.append(angle)
            ax.plot([x1, x2], [y1, y2], '-ro', markersize=2, linewidth=2)
            fig.canvas.draw()
        elif len(coords) == 3:
            x2, y2 = coords[1]
            x3, y3 = coords[2]
            height = sqrt((x3-x2)**2 + (y3-y2)**2)

            # draw rotated rectangle
            XY = rectangle_with_angle(coords[0][0], coords[0][1], width_angle[0], height, width_angle[1])

            fig.canvas.draw()

            # write to file
            for idx in range(4):
              annofile.write('{} {}\n'.format(XY[0,idx], XY[1,idx]))


            coords.clear()
            width_angle.clear()



    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    annofile.close()

