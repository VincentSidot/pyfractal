## Fractale
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import random as rnd

# nombre de racine
p = 7
epsilon = 1e-8
#taille grille en pixel
size = (4000,4000)
#equivalent sur le plan complexe
plan = (4,4)
max_iter = 1000
max_count = 30

def f(x):
    global p
    return (x**p)-1

def df(x):
    global p
    return p*(x**(p-1))
    
def imageToPlan(x,y):
    global size
    global plan
    return complex((x/size[0]*plan[0])-2,(y/size[1]*plan[1])-2)

def roundc(z,n=6):
    return complex(round(z.real,6),round(z.imag,6))

def newton(u0,f,df,epsilon,max_iter):
    u = u0
    n = 0
    error = epsilon + 1
    while abs(error)>epsilon and n <= max_iter:
        if df(u) == 0:
            return u,n
        error = f(u)/df(u)
        n+=1
        u = u - error
    return u,n

def map(value,imin,imax,omin,omax):
    igap = imax - imin
    ogap = omax - omin
    return (value-imin)/igap*ogap + omin
    
color = [ (255,0,0),(0,255,0),(0,0,255),(255,0,127),(255,255,0),(255,128,0),(127,0,255),(0,255,255),(255,0,255),(0,128,255) ]

# On genere une couleur par racine possible
colordict = {}
colordict[0] = (0,0,0,0)
for k in range(p):
    z = np.exp(2j*k*np.pi/p)
    z = roundc(z,6)
    if k < len(color):
        colordict[z] = (color[k][0],color[k][1],color[k][2],0)
    else:
        colordict[z] = (rnd.randint(0,256),rnd.randint(0,256),rnd.randint(0,256),0)

    
image = np.zeros((size[0],size[1],4),dtype = np.uint8) # image
    
for i in range(len(image)):
    for j in range(len(image[0])):
        u0 = imageToPlan(i,j)
        z,n = newton(u0,f,df,epsilon,max_iter)
        #print(n)
        image[i,j] = colordict[roundc(z,6)]
        image[i,j,3] = int(map(n,0,max_count,0,255))
        

image = ndimage.rotate(image,90)
plt.imshow(image)
plt.grid(False)

plt.show()
