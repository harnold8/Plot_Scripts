# -*- coding: utf-8 -*-
#normalization file
import sys
import os
from os import * 
import math

#Normalization
mu_0=4 * math.pi * 1.e-7
e=1.602e-19
#parameters
SI_B0 = 450.
SI_n0 = 60e6
SI_m0 = 18.5*1.672631e-27

#calculation
SI_v0=SI_B0*1e-12/math.sqrt(mu_0*SI_n0*SI_m0)
SI_E0=SI_v0*SI_B0*1e-3
SI_x0 = SI_v0*SI_m0/(e*SI_B0)
SI_n0=SI_n0*1e-6



#Number of vectors in vector plots
numberVectors = 125

typeofdata_infile = "2d"

name = "Europa"

AxisScaling="R_E"


xlabelposY = 0.42

caption = " "
#" Gyroradius in normalized units, i.e. u/B. The Cross-Section is at z=-1.4RE, which is about the value of E7 and E9. "


fieldname=(   "$B_x$", "$B_y$", "$B_z$","$|u|$",
	       
               "$n_{up}$",
              "$n_{ionosphere}$","$n_{H_2O}$","E"

)


# for 3D
# Change normalization parameters to display in SI
# Velocities are Alfven Velocity
expression=("<B/Y_CrossSection/B_X>*"+str(SI_B0),
	    "<B/Y_CrossSection/B_Y>*"+str(SI_B0),
	    "<B/Y_CrossSection/B_Z>*"+str(SI_B0),
	    "<U/Y_CrossSection/U_Magnitude>*"+str(SI_v0),
	    
	    
	    "<s0_rho/Y_CrossSection/s0_rho>*"+str(SI_n0),
	    "<s1_rho/Y_CrossSection/s1_rho>*"+str(SI_n0),
	    "<s2_rho/Y_CrossSection/s2_rho>*"+str(SI_n0),
	    "<E/Y_CrossSection/E_Magnitude>*"+str(SI_E0)
)






#Field scale
#0: linear
#1: log
fields_scale=(	0,0,
                0,0,
                0,1,
                1,0,

                1,1,
                0,0,
                1
)

fieldMesh=(	0,0,0,
	   	0,0,0,
		0,0,0,
		0,0,0,
		0,0,0,
		0,0,0,
		0,0,0)
		
flybyarrow=(	0,0,0,
	   	0,0,0,
		0,0,0,
		0,0,0,
		0,0,0,
		0,0,0,
		0,0,0)		
		
	    
fieldDomain=(0,0,0,
	    0,0,0,0,0,0,0,0,0,0,0,0,
		0,0,0,
		0,0,0)
	      
#Field min values 
fields_min=(-200, -20,
	    -500,   0,
               0,  .1,
             0.1,   0,
                
                0.1, 0.03,
                0, 0,
                0.01)


#Field max values
fields_max=(    200, 20, 
	       -400,150,
                100,1000,
                1000,60,
                30000,
                30, 30,
                300, 300,
                50)


#Field names for saves
fields=("Bx", "By",
        "Bz","U",
        "nup","nio",
        "nh2o","E"
)

fieldslatex=("$B_x$", "$B_y$","$B_z$","$|u|$",
	       
               "$n_{up}$",
              "$n_{io}$","$n_{H_2O}$","$E$"
)
             

unitsSI=("\\textnormal{B_x}\\textnormal{[nT]}",
	 "\\textnormal{B_y}\\textnormal{[nT]}",
	 "\\textnormal{B_z}\\textnormal{[nT]}",
	 "$|$\\textnormal{\\textbf{U}}$|$\\textnormal{[km/s]}",
	 "\\textnormal{$n_{\\textnormal{up}}$}\\textnormal{[cm$^{-3}$]}",
         "\\textnormal{$n_{O_2}$}\\textnormal{[cm$^{-3}$]}",
         "\\textnormal{$n_\mathrm{H_2O}$}\\textnormal{[cm$^{-3}$]}",
         "$|$\\textnormal{\\textbf{E}}$|$\\textnormal{[mV/m]}",
         
         "\\textnormal{$n_{\\textnormal{up}}$}\\textnormal{[cm$^{-3}$]}",
         "\\textnormal{$n_{\\textnormal{io}}$}\\textnormal{[cm$^{-3}$]}",
         "\\textnormal{$n_{\\textnormal{H_2O}}$}\\textnormal{[cm$^{-3}$]}"
)


#Fieldtyps
# 1 = Vector field
# 0 = scalar field
fieldsVector=(0,0,0,
	      0,0,0,
	      0,0,0,
	      0,0,0,
	      0,0,0,
	      1,1,0,
	      1,0,0)

#=(1,0,0,1,1,0,0)

# Fieldnames for vector plots
fieldsVectorName=("B/Y_CrossSection/B_XZvec", "", "",
		  "", "", "",
		  "", "", "",
		  "s0_u/Y_CrossSection/s0_u_XZvec", "s1_u/Y_CrossSection/s1_u_XZvec", "B/Y_CrossSection/B_XZvec",
		  "", "", "E/Z_CrossSection/E_XYvec",
		  "E/E_vec", "s0_u/s0_u_vec", "B/Z_CrossSection/B_XYvec",
		  "E/E_vec", "E/E_vec", "B/Z_CrossSection/B_XYvec")
	

fieldsCrossSection=("Y","Y","Y",
		    "Y","Y","Y",
		    "Y","Y")

interception_3d=(0,0,0,
		 0,0,0,
		 -1.5,-1.5,-1.5,
		 -4,-4,-4,
		 -7.3,-7.3,-7.3,
		 -4,-4,-4,
		 -4,0,-4)

# Streamlineplot related
fieldstreamline=(	0,0,0,
			0,0,0,
			0,0,0,
			0,0,0,
			0,0,0,
			0,0,0)
fieldstreamline_xstart=(-5,-5)
fieldstreamline_xend=(10,10)
fieldstreamline_ystart=(20,2)
fieldstreamline_yend=(20,20)
fieldstreamline_zstart=(0,0)
fieldstreamline_zend=(0,0)
fieldstreamline_length=(60,60)
fieldstreamline_Nr_of_Lines=(10,10)

unitxpos=(0.87,0.87,0.87,
	  0.87,0.87,0.87,
	  0.87,0.87,0.87,
	  0.87,0.87,0.87,
	  0.87,0.87,0.87,
	  0.8,0.8,0.6,
	  0.8,0.8,0.6)

	
#Output in special directory different form current directory
#output in curent directory
outputPath = curdir + "/"

#output in special directory
#outputPath = homedir +"/Auswertung2/"
