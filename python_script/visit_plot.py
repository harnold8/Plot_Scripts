#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import os
import math
from os import *
import matplotlib.pyplot as plt

def clean():
	print("Clean environment")
	remove(homedir+"/bin/plotten/plotdata_options.py")
	if path.exists(homedir+'/bin/plotten/plotdata_error.py') :
		remove(homedir+'/bin/plotten/plotdata_error.py')
	if path.exists(homedir+'/bin/plotten/plotdata_latex.tex') :
		remove(homedir+'/bin/plotten/plotdata_latex.tex')
	if path.exists(homedir+'/bin/plotten/plotdata_latex.sty') :
		remove(homedir+'/bin/plotten/plotdata_latex.sty')
	print("Done and finished")
	sys.exit();
	
print(" ")
print("________________________")
print("PlotDataTool")
print("________________________")
print(" ")

homedir = os.environ['HOME']

print("Which kind of plotskript? (has to be same name than folder in bin/plotten/ and files within)")
print("Available are : ")
os.system("ls "+homedir+"/bin/plotten/")
plotscript = raw_input()
print(" ")

optiondir = homedir + "/bin/plotten/"+plotscript+"/"

execfile(optiondir + plotscript+".py")


# below reads current folder automatically as filename
import commands
status, namefiles = commands.getstatusoutput("echo ${PWD##*/}")


time = raw_input("Please insert timestep (5 numbers!) : ")

print(" ")
fieldnumberstr = raw_input("Number of fields to plot : ")
print(" ")


#just a quick plot of one field property or more
if int(fieldnumberstr) == 1:
	field_type_to_plot = int(raw_input(" Predefined field (number) or field name (0/1)?"))
	thisfield = raw_input("Which field to plot? : ")
	print(" ")
else:
	thisfield = 42 #die antwort auf alles ;)

fieldnumber = int(fieldnumberstr)

#setting output paths
outputPathlatex = outputPath
outputPath = outputPath + "visit/"
os.system("mkdir "+outputPath)
outputPath = outputPath+plotscript+"TL"+ time +"/"
#delete old files, if existing
os.system("rm -r "+outputPath)
os.system("mkdir "+outputPath)

#preparing visit
print("Create VisIt config file")
optionfile = file(homedir+'/bin/plotten/plotdata_options.py', 'w') 
optionfile.write('simulationname = "'+name+'"\n')
optionfile.write('timestep = "'+time+ '"\n')
optionfile.write('plotscript = "'+plotscript+'"\n')
optionfile.write('fieldnumberstr ="'+fieldnumberstr+'"\n')
optionfile.write('thisfield ="'+str(thisfield)+'"\n')
optionfile.write('namefiles = "'+namefiles+'" \n')
optionfile.write('outputPathPlots = "'+outputPath+'" \n')
optionfile.close()


if int(fieldnumberstr) == 1:
	if field_type_to_plot == 1:
		thisfield = 1


print("Starting VisIt")
os.system( '/usr/local/packages/visit/bin/visit -cli -nowin -s '+optiondir+'visit_'+plotscript+'.py')

if path.exists(optiondir+'plotdata_error.py') :
	print("Es gab Fehler!")




print("Prepare Latex")
#for size of pdf
width = 7


#delete old files, creating new directory
chdir(outputPath)

#plotting the moon in the center of the plot
for i in range(fieldnumber):
    fileName=namefiles+"_"+fields[i]+"0000"
    xmin=-4
    xmax=8
    zmin=-6
    zmax=6
    rfactor=1.0
    imgdata = plt.imread(fileName+".png")
    imgmerc = plt.imread(homedir+"/bin/Europa2.png")
    plt.imshow(imgmerc, zorder=12, extent=[-1, 1, -1, 1])
    plt.imshow(imgdata, zorder=10, extent=[-5.5, 11.9, -9.5, 8.6])
    plt.axis('off')
    save=fileName+".png"
    plt.savefig(save,bbox_inches='tight',dpi=170)
    plt.close()



figure=[None]*fieldnumber  

if int(thisfield) == 42:
	fieldnumbermin = 0
	fieldnumbermax = fieldnumber
else:
	fieldnumbermin = int(thisfield) - 1
	fieldnumbermax = int(thisfield)

#creating the latex pdf files
for i in range(fieldnumbermin,fieldnumbermax):
	latexfile = file('plotdata_latex.tex', 'w')
	string = ""
	sty_string = ""
	string += " \includegraphics[width="+str(width)+"cm]{"+outputPathlatex+namefiles+"_"+fields[i]+"0000} "
	latexfile.write(string)
	latexfile.close()
	latexstylefile = file('plotdata_latex.sty','a')
	if thisfield == 42 :
		sty_string += " \\renewcommand{\\unit}{"+unitsSI[i]+"} \n "
		sty_string += " \\renewcommand{\\unitxpos}{"+str(unitxpos[i])+"} \n "
	if fieldsCrossSection[i] == "Y":
			sty_string += " \\renewcommand{\\xlabelpos}{"+str(xlabelposY)+"} \n "
	else:
			sty_string += " \\renewcommand{\\xlabelpos}{0.5} \n "
	sty_string += " \\renewcommand{\\plottedflyby}{"+str(flybyarrow[i])+"} \n "
	latexstylefile.write(sty_string)
	latexstylefile.close()
	print("Starting Latex")
	os.system("cp "+optiondir+"header_"+plotscript+".tex " " header_"+plotscript+".tex")
	os.system("pdflatex header_"+plotscript+".tex")
	os.system("mv header_"+plotscript+".pdf "+namefiles+"_"+fields[i]+"_TL"+time+".pdf")


#count = 1
if fieldnumber > 1:
	latexfile = file('plot_overview.tex', 'w')
	string = ""
	for j in range(fieldnumber):
		string+= " \subfigure["+fieldslatex[j]+"]{\includegraphics[width=5.5cm]{"+namefiles+"_"+fields[j]+"_TL"+time+"}} "
		#orientation portrat (%2) or landscape (%3)
		if (j+1)%2 != 0:
			string+= " & \n "
		else:
			string+= " \\\ \\hline \n"

	latexfile.write(string)
	latexfile.close()
	os.system("cp "+optiondir+"overview_"+plotscript+".tex " " overview_"+plotscript+".tex")
	os.system("echo 'Here'")
	os.system("pdflatex overview_"+plotscript+".tex >/dev/null")
	os.system("mv overview_"+plotscript+".pdf "+namefiles+"_overview.pdf")
	os.system("rm *.log *.aux")
	os.system("okular "+namefiles+"_overview.pdf &")
else :
	thisfield = int(thisfield) -1
	os.system("okular "+namefiles+"_"+fields[int(thisfield)]+"_TL"+time+".pdf &")

clean()
