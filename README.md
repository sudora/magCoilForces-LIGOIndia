# Calculation of Magnetic Force between a coil and a permanent Magnet
This repo holds a python script as well as a jupyter notebook to calculate magnetic forces as mentioned in the header above using the Filament method given in this paper : https://ieeexplore.ieee.org/document/6184314  <br><br>
For usage, you need to set the parameters of your system appropriately in the .json file hosted in the repo. The descriptions of all parameters are as given below -  
Rm : Lenght (mm) Magnet Radius  
lm : Length (mm) Magnet Length  
Nm : Number (num) Magnet 'turns'  
Br : (Tesla) Magnet remanence  
rc : Length (mm) Coil inner radius  
Rc : Length L(mm) Coil Outer radius  
lc : Length (mm) Coil Length  
Nz : Number (num) Coil turns in axial direction  
Nr : Number (num) Coil turns in radial direction  
I : (Ampere) Coil current  
zmin : Lenght (mm) Origin is at center of the coil. Leftmost position of   magnet from center of coil  
zmax : Length (mm) Rightmost position of magnet from center of coil  
step : Number (num) steps in which you want to split the zmax-zmin distance. Granularity  
<br><br>
Please set all parameters in the correct units as mentioned in this readme file. 
After setting these parameters you can simply run the magCoilForces.py python script on a linux or windows shell. \
Make sure the .json file is in the same location as the script. 
The script will automatically pick up the parameters and print the sweet spot at which the d/dx of Force is 0, the force at the sweet spot and also generate a graph of force against distance. 
Note that the z in this graph is the distance from the center of the magnet to the center of the coil.
