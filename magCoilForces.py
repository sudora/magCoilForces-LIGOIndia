import os, time
import numpy as np
import scipy as sci
from scipy import special
from scipy import constants as c
import matplotlib.pyplot as plt
from multiprocessing import Pool

#Collecting user inputs from magCoilConfig.txt
mmTometre = 0.001
f=open("magCoilConfig.txt","r")
config=f.read()
config=[con[:con.find('#')].strip() for con in config.split('\n')]
param={}
for c in config:
    key, val = c.split(' ')[0], np.float(c.split(' ')[-1])
    param[key]=val

Rm = param['Rm'] * mmTometre # L(mm) Magnet Radius
lm = param['lm'] * mmTometre # L(mm) Magnet Length
Nm = param['Nm'] # (num) Magnet 'turns'
Br = param['Br'] # (Tesla) Magnet remanence
rc = param['rc'] * mmTometre # L(mm) Coil inner radius
Rc = param['Rc'] * mmTometre # L(mm) Coil Outer radius
lc = param['lc'] * mmTometre # L(mm) Coil Length
Nz = param['Nz'] # (num) Coil turns in axial direction
Nr = param['Nr'] # (num) Coil turns in radial direction
I = param['I'] # (Ampere) Coil current
zmin = param['zmin'] # (mm) Origin is at center of the coil. Leftmost position of magnet from center of coil
zmax = param['zmax'] # (mm) Rightmost position of magnet from center of coil
step = param['step'] # (num) steps in which you want to split the zmax-zmin distance. Granularity
zRange = np.arange(zmin, zmax, step) * mmTometre

def Ff(r1, r2, z):
    term1=I*z*Br*lm/Nm
    m=4*r1*r2/((r1+r2)**2 + z**2)
    term2=m/(4*r1*r2)
    term2=np.power(term2,0.5)
    term3=special.ellipk(m)
    term4=((0.5*m)-1)/(m-1)
    term5=special.ellipe(m)
    Ff=term1*term2*(term3-(term4*term5))
    return Ff

def r(nr):
	term1=(nr-1)/(Nr-1)
    return rc+(term1*(Rc-rc))

def L(nm, nz):
    term1=(nz-1)/(Nz-1)
    term2=(nm-1)/(Nm-1)
    return (-0.5*(lm+lc))+(term1*lc)+(term2*lm)

def ForceFilament(z):
    F=0.0
    for nm in range(1,int(Nm)+1):
        for nr in range(1,int(Nr)+1):
            for nz in range(1,int(Nz)+1):
                rnr=r(nr)
                zL=z+L(nm, nz)
                f=Ff(rnr, Rm, zL)
                F+=f
    return F

if __name__=="__main__":
	Force=[]
	for v in zRange:
		Force.append(FoceFilament(v))
	print("Max Force (N) : ",np.amax(Force),"Min Force (N) : ",np.amin(Force))
	print("Sweet Spots (mm) : ",zRange[np.argmin(Force)]*1e3, zRange[np.argmax(Force)]*1e3)
	fig=plt.figure(num=None, figsize=(10,5), dpi=100)
	ax = SubplotZero(fig, 111)
	fig.add_subplot(ax)
	for direction in ["xzero","yzero"]:
	    ax.axis[direction].set_axisline_style("-|>")
	    ax.axis[direction].set_visible(True)

	plt.text(zmax/8,np.amax(Force),"Force(N)")
	plt.text(zmin,np.amin(Force)/4, "z(mm)")

	for direction in ["left", "right", "bottom", "top"]:
	    ax.axis[direction].set_visible(False)
	        
	plt.plot(zRange*1e3,Force)
	plt.savefig("MagCoilForceFigure.jpg")