#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Script for Visit
# visit read file and creates png images in outputPath
import sys
import os
from os import *

homedir = os.environ['HOME']
Source(homedir + "/bin/plotten/plotdata_options.py")

optiondir = homedir + "/bin/plotten/"+plotscript+"/"


# changed!!!!!!!!!!!!!!!!!!!!!!!
Source(homedir + "/bin/plotten/"+plotscript+"/"+plotscript+".py")

fieldnumber = int(fieldnumberstr)


usefile = 1


if usefile == 0:
	print(" ")
	typeofdata = raw_input("Data files : 2d or 3d : ")
	print(" ")
else :
	typeofdata = typeofdata_infile

#Input file 
#Input from simulation folder
if typeofdata == "2d":
	 inputPath= curdir + "/data/silo/" + simulationname + "_"+typeofdata+"_p00000_TL" + timestep+".silo"
elif typeofdata == "3d" :
	 inputPath= curdir + "/data/silo_3D/" + simulationname + "_"+typeofdata+"_p00000_TL" + timestep+".silo"
print(inputPath)

#check if input file exists
if not path.exists(inputPath) :
	print("ERROR: Missing file!")
	optionfile = file(optiondir+'plotdata_error.py', 'w') 
	optionfile.write("1")
	optionfile.close()
	exit()

#check if directory for output still exists
if not path.exists(outputPath+ "visit") :
	mkdir(outputPath + "visit")
if not path.exists(outputPathPlots) :
	mkdir(outputPathPlots)

#do not change
outputPath = outputPathPlots
print(outputPath)
HideToolbars(1)
OpenDatabase(inputPath)

xaxislabel = CreateAnnotationObject("Text2D")
yaxislabel = CreateAnnotationObject("Text2D")

#creating each plot
for i in range(fieldnumber):
		#if the user decides to not use our parameters file, here some example values/properties
		if usefile == 0:
			print(" ")
			field = raw_input("Field (or 'Expression' or 'SIFactor' o Mesh) : ")
			print(" ")
			if field == "B":
				SIFactor = 325
			if field == "BEven":
				SIFactor = 325
			elif field == "Rho" :
				SIFactor = 70.5
			elif field == "s1_rho" :
				SIFactor = 70.5
			else :
				SIFactor = 1
				SIFactor = raw_input("SI conversion factor: ")
			if field == "Rho" :
				component = "Rho"
			elif field == "s1_rho" :
				component = "s1_rho"
			else :
				print(" ")
				component = raw_input("Component : ")
			print(" ")
			crosssec = raw_input("Cross-Section? (X, Y, Z, 'arbitrary') : ")
			print(" ")
			if typeofdata == "3d":
				interception = float(input("Cross-Section at : "))
			if crosssec == "arbitrary":
				normalx = input("normal vector x : ")
				normaly = input("normal vector y : ")
				normalz = input("normal vector z : ")
			
			if typeofdata == "2d":
				DefineScalarExpression("SI", "<"+field+"/"+crosssec+"_CrossSection/"+component+">*"+str(SIFactor))
			elif typeofdata == "3d":
				DefineScalarExpression("SI", component+"*"+str(SIFactor))
			if field == "Expression":
				DefineScalarExpression("SI", expression[i])
	

			if field == "Mesh":
				AddPlot("Mesh","Mesh3D")
			else:
				AddPlot("Pseudocolor", "SI")
				AddOperator("Clip", 0)
				SetActivePlots(0)
				SetActivePlots(0)
				ClipAtts = ClipAttributes()
				ClipAtts.quality = ClipAtts.Fast  # Fast, Accurate
				ClipAtts.funcType = ClipAtts.Sphere  # Plane, Sphere
				ClipAtts.plane1Status = 1
				ClipAtts.plane2Status = 0
				ClipAtts.plane3Status = 0
				ClipAtts.plane1Origin = (0, 0, 0)
				ClipAtts.plane2Origin = (0, 0, 0)
				ClipAtts.plane3Origin = (0, 0, 0)
				ClipAtts.plane1Normal = (1, 0, 0)
				ClipAtts.plane2Normal = (0, 1, 0)
				ClipAtts.plane3Normal = (0, 0, 1)
				ClipAtts.planeInverse = 0
				ClipAtts.planeToolControlledClipPlane = ClipAtts.Plane1  # None, Plane1, Plane2, Plane3
				ClipAtts.center = (0, 0, 0)
				ClipAtts.radius = 1
				ClipAtts.sphereInverse = 0
				SetOperatorOptions(ClipAtts, 1)
			if typeofdata == "3d":
				AddOperator("Slice")
				sliceopts = SliceAttributes()
				if crosssec == "X":
					sliceopts.axisType = sliceopts.XAxis
				elif crosssec == "Y":
					sliceopts.axisType = sliceopts.YAxis
				elif crosssec == "Z":
					sliceopts.axisType = sliceopts.ZAxis
				elif crosssec == "arbitrary":
					sliceopts.axisType = sliceopts.Arbitrary
					sliceopts.normal = (normalx, normaly, normalz)
				sliceopts.originIntercept = interception
				SetOperatorOptions(sliceopts)


		#the interesting part, setting visit to the parameters from the file
		else :
			field = fieldname[i] 
			crosssec = fieldsCrossSection[i]
			interception = interception_3d[i]
			DefineScalarExpression("SI", expression[i])
			AddPlot("Pseudocolor", "SI")

			if typeofdata == "3d":
				AddOperator("Slice")
				sliceopts = SliceAttributes()
				if crosssec == "X":
					sliceopts.axisType = sliceopts.XAxis
					#print(crosssec)
				elif crosssec == "Y":
					sliceopts.axisType = sliceopts.YAxis
				elif crosssec == "Z":
					sliceopts.axisType = sliceopts.ZAxis
				sliceopts.originIntercept = interception
				SetOperatorOptions(sliceopts)

		DrawPlots()
	
		pL = GetPlotList()
		
		if field == "Mesh":
			legend = GetAnnotationObject(pL.GetPlots(0).plotName)
			legend.legendFlag = 0

		#setting min/max values for the plot and the legend format
		else:
			legend = GetAnnotationObject(pL.GetPlots(0).plotName)
			legend.xScale = 1.2
			legend.yScale = 2.9
			legend.drawTitle = 0
			legend.drawMinMax = 0
			Query("MinMax")
			tempMinMax =GetQueryOutputValue()
			MinMax = tempMinMax[1]-tempMinMax[0]
			if MinMax < 0.5:
				legend.numberFormat = "%#-9.2f"
			elif MinMax > 0.5 and MinMax < 2.5:
				legend.numberFormat = "%#-9.1f"
			else :
				legend.numberFormat = "%-9.0f"
                        if field == "Rho" or field == "s0_rho" or field == "s1_rho" or field == "s2_rho" or field == "rho_ne":
                                legend.numberFormat = "%-9.2f"
			legend.fontBold = 1
			legend.fontHeight = 0.05
			legend.managePosition = 0
			#legend.position = (0.823, 0.9)
                        legend.position = (0.823, 0.9)
		
	
		plot = PseudocolorAttributes()
		plot.min, plot.minFlag= fields_min[i], 1
		plot.max, plot.maxFlag= fields_max[i], 1
		if usefile == 1:
			plot.min, plot.minFlag= fields_min[i], 1
			plot.max, plot.maxFlag= fields_max[i], 1
			plot.scaling = fields_scale[i]
		if (field=="B" or field=="BEven"):

                        plot.colorTableName = "YlGnBu"
                elif (field=="Bx" or field=="By" or field=="Bz"):
                        plot.colorTableName = "difference"
		else:

			plot.colorTableName = "hot_desaturated"
		SetPlotOptions(plot)

	
		annotation = AnnotationAttributes()
		annotation.userInfoFlag = 0
		annotation.databaseInfoFlag = 0
		annotation.legendInfoFlag = 1
		annotation.axes2D.lineWidth = 1
		annotation.axes2D.tickAxes = annotation.axes2D.All
		
		
		#setting the tickrate, has to be adjusted
		annotation.axes2D.autoSetTicks =0
		annotation.axes2D.xAxis.tickMarks.minorSpacing = 1
		annotation.axes2D.xAxis.tickMarks.majorSpacing = 10
		annotation.axes2D.yAxis.tickMarks.minorSpacing = 1
		annotation.axes2D.yAxis.tickMarks.majorSpacing = 5
		
		
		annotation.axes2D.tickLocation = annotation.axes2D.Both
		annotation.axes2D.xAxis.title.visible = 0
		annotation.axes2D.yAxis.title.visible = 0
		annotation.axes2D.xAxis.label.font.scale = 3
		annotation.axes2D.yAxis.label.font.scale = 3
		annotation.axes2D.xAxis.label.font.italic = 0
		annotation.axes2D.yAxis.label.font.italic = 0
		annotation.axes2D.xAxis.label.font.bold = 1
		annotation.axes2D.yAxis.label.font.bold = 1
		annotation.axes2D.xAxis.label.font.font = annotation.axes2D.xAxis.label.font.Arial
		annotation.axes2D.yAxis.label.font.font = annotation.axes2D.yAxis.label.font.Arial
		SetAnnotationAttributes(annotation)
	
		ResetView()
		view = GetView2D()
		view.viewportCoords = (0.12, 0.8, 0.15, 0.9) 
		view.fullFrameActivationMode = view.On
		xaxislabel.text = ""
		yaxislabel.text = ""
		width = 7
		paperheight = 7

		#settings for the LaTex file
		latexstylefile = file(outputPath+'plotdata_latex.sty','w')
		sty_string = " \\setlength{\\paperwidth}{"+str(width+0.5)+"cm}\n"
		sty_string += " \\setlength{\\paperheight}{"+str(paperheight+0.25)+"cm}\n"
		sty_string += "\\areaset{"+str(width)+"cm}{"+str(paperheight)+"cm}\n"
		sty_string += " \\newcommand{\\xlabelpos}{0.5} \n "
		if crosssec == "X":
			sty_string += " \\newcommand{\\xlabel}{y $[R_C]$} \n "
			sty_string += " \\newcommand{\\ylabel}{z $[R_C]$} \n "
			# Zoom box in here!
                        #view.windowCoords = (-10,10,-20,20)
		elif crosssec == "Y":
			xmin=-4
			xmax=8
			zmin=-6
			zmax=6
			ratio=1.#abs(2.*xmin)/abs(2.*zmin)
			xstart=0.1
			view.viewportCoords = (xstart, xstart+0.65*ratio, 0.2, 0.85)
			legend.position = (xstart+0.65*ratio+0.05, 0.85)
			annotation.axes2D.yAxis.tickMarks.minorSpacing = 1
			annotation.axes2D.yAxis.tickMarks.majorSpacing = 2
			annotation.axes2D.xAxis.tickMarks.minorSpacing = 1
			annotation.axes2D.xAxis.tickMarks.majorSpacing = 2
			annotation.axes2D.yAxis.tickMarks.majorMinimum = zmin
			annotation.axes2D.yAxis.tickMarks.majorMaximum = zmax
			annotation.axes2D.xAxis.tickMarks.majorMinimum = xmin
			annotation.axes2D.xAxis.tickMarks.majorMaximum = xmax
			SetAnnotationAttributes(annotation)
			sty_string += " \\newcommand{\\ylabel}{z $[R_E]$} \n "
			sty_string += " \\newcommand{\\xlabel}{x $[R_E]$} \n "
			view.windowCoords = (xmin+.01,xmax+.01,zmin-.01,zmax+.01)
		elif crosssec == "Z":
			sty_string += " \\newcommand{\\xlabel}{x $[R_C]$} \n "
			sty_string += " \\newcommand{\\ylabel}{y $[R_C]$} \n "
			#view.windowCoords = (-8,8,-8,8)
			#view.windowCoords = (-9.4117647,9.4117647,-9.4117647,9.4117647)
                        view.windowCoords = (-9.4117647,14.11764706,-11.76470588,11.76470588)
		if usefile == 0:
			if field == "B" :
				sty_string += " \\newcommand{\\unit}{[nT]} \n "
			elif field == "BEven" :
				sty_string += " \\newcommand{\\unit}{[nT]} \n "
			elif field == "Rho" :
				sty_string += " \\newcommand{\\unit}{[e$\cdot$cm$^{-3}$]} \n "
			sty_string += " \\newcommand{\\unitxpos}{0.85} \n "
		else :
			sty_string += " \\newcommand{\\unit}{"+unitsSI[i]+"} \n "
			sty_string += " \\newcommand{\\unitxpos}{"+str(unitxpos[i])+"} \n "    
			sty_string += " \\newcommand{\\plottedflyby}{"+str(-1)+"} \n "			
		latexstylefile.write(sty_string)
		latexstylefile.close()

		SetView2D(view)
		#i want 4 equidistant ticks for log
		if plot.scaling == 1:
		  legend.numTicks = 5


	
		#Draw Moon/Planet
		if typeofdata == "3d":
			if crosssec == "Y":
				AddPlot("Mesh","Mesh3D")
				moon = MeshAttributes()
				moon.legendFlag = 0
				moon.lineWidth = 1
				moon.meshColor = (0,0,0,255)
				SetPlotOptions(moon)	
				AddOperator("Clip")
				ClipAtts = ClipAttributes()
				ClipAtts.funcType = ClipAtts.Sphere
				ClipAtts.sphereInverse = 1
				SetOperatorOptions(ClipAtts)
				AddOperator("Slice")
				circle = SliceAttributes()			
				if crosssec == "X":
					circle.axisType = circle.XAxis
				elif crosssec == "Y":
					circle.axisType = circle.YAxis
				elif crosssec == "Z":
					circle.axisType = circle.ZAxis
				elif crosssec == "arbitrary":
					circle.axisType = circle.Arbitrary
					circle.normal = (normalx, normaly, normalz)
				SetOperatorOptions(circle)
				DrawPlots()
			elif crosssec == "Z":
				AddPlot("Mesh","Mesh3D")
				moon = MeshAttributes()
				moon.legendFlag = 0
				moon.lineWidth = 1
				moon.meshColor = (0,0,0,255)
				SetPlotOptions(moon)	
				AddOperator("SphereSlice", 0)
				SphereSliceAtts = SphereSliceAttributes()
				SphereSliceAtts.origin = (0, 0, 0)
				SphereSliceAtts.radius = 1
				SetOperatorOptions(SphereSliceAtts, 0)
				AddOperator("Slice", 0)
				SliceAtts = SliceAttributes()
				SliceAtts.originType = SliceAtts.Intercept  # Point, Intercept, Percent, Zone, Node
				SliceAtts.originPoint = (0, 0, 0)
				SliceAtts.originIntercept = 0
				SliceAtts.originPercent = 0
				SliceAtts.originZone = 0
				SliceAtts.originNode = 0
				SliceAtts.normal = (0, 0, 1)
				SliceAtts.axisType = SliceAtts.ZAxis  # XAxis, YAxis, ZAxis, Arbitrary, ThetaPhi
				SliceAtts.upAxis = (0, 1, 0)
				SliceAtts.project2d = 1
				SliceAtts.interactive = 1
				SliceAtts.flip = 0
				SliceAtts.originZoneDomain = 0
				SliceAtts.originNodeDomain = 0
				SliceAtts.meshName = "Mesh3D"
				SliceAtts.theta = 0
				SliceAtts.phi = 90
				SetOperatorOptions(SliceAtts, 0)
				DrawPlots()

		#2D plots, same procedure as above
		elif typeofdata == "2d":
				AddPlot("Pseudocolor", "B/Z_CrossSection/B_Magnitude", 1, 0)
				AddOperator("Clip", 0)
				SetActivePlots(1)
				SetActivePlots(1)
				ClipAtts = ClipAttributes()
				ClipAtts.quality = ClipAtts.Fast  # Fast, Accurate
				ClipAtts.funcType = ClipAtts.Sphere  # Plane, Sphere
				ClipAtts.plane1Status = 1
				ClipAtts.plane2Status = 0
				ClipAtts.plane3Status = 0
				ClipAtts.plane1Origin = (0, 0, 0)
				ClipAtts.plane2Origin = (0, 0, 0)
				ClipAtts.plane3Origin = (0, 0, 0)
				ClipAtts.plane1Normal = (1, 0, 0)
				ClipAtts.plane2Normal = (0, 1, 0)
				ClipAtts.plane3Normal = (0, 0, 1)
				ClipAtts.planeInverse = 0
				ClipAtts.planeToolControlledClipPlane = ClipAtts.Plane1  # None, Plane1, Plane2, Plane3
				ClipAtts.center = (0, 0, 0)
				ClipAtts.radius = 1
				ClipAtts.sphereInverse = 1
				SetOperatorOptions(ClipAtts, 0)
				PseudocolorAtts = PseudocolorAttributes()
				PseudocolorAtts.scaling = PseudocolorAtts.Linear  # Linear, Log, Skew
				PseudocolorAtts.skewFactor = 1
				PseudocolorAtts.limitsMode = PseudocolorAtts.OriginalData  # OriginalData, CurrentPlot
				PseudocolorAtts.minFlag = 1
				PseudocolorAtts.min = 0
				PseudocolorAtts.maxFlag = 1
				PseudocolorAtts.max = 0.01
				PseudocolorAtts.centering = PseudocolorAtts.Natural  # Natural, Nodal, Zonal
				PseudocolorAtts.colorTableName = "xray"
				PseudocolorAtts.invertColorTable = 0
				PseudocolorAtts.opacityType = PseudocolorAtts.FullyOpaque  # ColorTable, FullyOpaque, Constant, Ramp, VariableRange
				PseudocolorAtts.opacityVariable = ""
				PseudocolorAtts.opacity = 1
				PseudocolorAtts.opacityVarMin = 0
				PseudocolorAtts.opacityVarMax = 1
				PseudocolorAtts.opacityVarMinFlag = 0
				PseudocolorAtts.opacityVarMaxFlag = 0
				PseudocolorAtts.pointSize = 0.05
				PseudocolorAtts.pointType = PseudocolorAtts.Point  # Box, Axis, Icosahedron, Octahedron, Tetrahedron, SphereGeometry, Point, Sphere
				PseudocolorAtts.pointSizeVarEnabled = 0
				PseudocolorAtts.pointSizeVar = "default"
				PseudocolorAtts.pointSizePixels = 2
				PseudocolorAtts.lineType = PseudocolorAtts.Line  # Line, Tube, Ribbon
				PseudocolorAtts.lineStyle = PseudocolorAtts.SOLID  # SOLID, DASH, DOT, DOTDASH
				PseudocolorAtts.lineWidth = 0
				PseudocolorAtts.renderSurfaces = 1
				PseudocolorAtts.renderWireframe = 0
				PseudocolorAtts.renderPoints = 0
				PseudocolorAtts.smoothingLevel = 0
				PseudocolorAtts.legendFlag = 0
				PseudocolorAtts.lightingFlag = 1
				SetPlotOptions(PseudocolorAtts)
				DrawPlots()

		if crosssec == "Y" and ( field=="B" or field=="BEven") :
			if typeofdata == "2d":
#				AddPlot("Mesh","Trajectories/Y_CrossSection/C10_reformat")
				flyby = MeshAttributes()
				flyby.legendFlag = 0
				flyby.pointSizePixels = 5
				flyby.meshColor = (0,0,0,255)
				SetPlotOptions(flyby)	
				DrawPlots()
			elif typeofdata == "3d":
				AddPlot("Mesh","Trajectories/T70_tiis_1s")
				flyby = MeshAttributes()
				flyby.legendFlag = 0
				flyby.pointSizePixels = 5
				flyby.meshColor = (0,0,0,255)
				SetPlotOptions(flyby)	
				AddOperator("Project")
				ProjectAtts = ProjectAttributes()
				ProjectAtts.projectionType = ProjectAtts.XZCartesian  # ZYCartesian, XZCartesian, XYCartesian, XRCylindrical, YRCylindrical, ZRCylindrical
				ProjectAtts.vectorTransformMethod = ProjectAtts.AsDirection  # None, AsPoint, AsDisplacement, AsDirection
				SetOperatorOptions(ProjectAtts)
				DrawPlots()
				AddPlot("Mesh","Trajectories/T70_tiis_1s")
				flyby = MeshAttributes()
				flyby.legendFlag = 0
				flyby.pointSizePixels = 5
				flyby.meshColor = (0,0,0,255)
				SetPlotOptions(flyby)	
				AddOperator("Project")
				ProjectAtts = ProjectAttributes()
				ProjectAtts.projectionType = ProjectAtts.XZCartesian  # ZYCartesian, XZCartesian, XYCartesian, XRCylindrical, YRCylindrical, ZRCylindrical
				ProjectAtts.vectorTransformMethod = ProjectAtts.AsDirection  # None, AsPoint, AsDisplacement, AsDirection
				SetOperatorOptions(ProjectAtts)

				DrawPlots()
		elif crosssec == "Z" : #and ( field=="B" or field=="BEven") :
			if typeofdata == "2d":
				AddPlot("Mesh","Trajectories/Z_CrossSection/C23_reformat")
				flyby = MeshAttributes()
				flyby.legendFlag = 0
				flyby.pointSizePixels = 7
				flyby.meshColor = (0,0,0,255)
				SetPlotOptions(flyby)
				DrawPlots()

			elif typeofdata == "3d":
				if interception > 0:
					    AddPlot("Mesh","Trajectories/E12_detrended_neu")
				elif interception < -4 :
					    AddPlot("Mesh","Trajectories/E8_detrended_neu")
					    flyby = MeshAttributes()
					    flyby.legendFlag = 0
					    flyby.pointSizePixels = 5
					    flyby.meshColor = (0,0,0,255)
					    SetPlotOptions(flyby)	
					    AddOperator("Project")
					    ProjectAtts = ProjectAttributes()
					    ProjectAtts.projectionType = ProjectAtts.XYCartesian  # ZYCartesian, XZCartesian, XYCartesian, XRCylindrical, YRCylindrical, ZRCylindrical
					    ProjectAtts.vectorTransformMethod = ProjectAtts.AsDirection  # None, AsPoint, AsDisplacement, AsDirection
					    SetOperatorOptions(ProjectAtts)
					    if fields[i] == "Bx_ZCS_E8" :
							AddPlot("Mesh","Trajectories/E8_Bx_Points")
							flyby = MeshAttributes()
							flyby.legendFlag = 0
							flyby.pointSizePixels = 20
							flyby.meshColor = (0,0,0,255)
							SetPlotOptions(flyby)	
							AddOperator("Project")
							ProjectAtts = ProjectAttributes()
							ProjectAtts.projectionType = ProjectAtts.XYCartesian  # ZYCartesian, XZCartesian, XYCartesian, XRCylindrical, YRCylindrical, ZRCylindrical
							ProjectAtts.vectorTransformMethod = ProjectAtts.AsDirection  # None, AsPoint, AsDisplacement, AsDirection
							SetOperatorOptions(ProjectAtts)
					    if fields[i] == "By_ZCS_E8" :
							AddPlot("Mesh","Trajectories/E8_By_Points")
							flyby = MeshAttributes()
							flyby.legendFlag = 0
							flyby.pointSizePixels = 20
							flyby.meshColor = (0,0,0,255)
							SetPlotOptions(flyby)	
							AddOperator("Project")
							ProjectAtts = ProjectAttributes()
							ProjectAtts.projectionType = ProjectAtts.XYCartesian  # ZYCartesian, XZCartesian, XYCartesian, XRCylindrical, YRCylindrical, ZRCylindrical
							ProjectAtts.vectorTransformMethod = ProjectAtts.AsDirection  # None, AsPoint, AsDisplacement, AsDirection
							SetOperatorOptions(ProjectAtts)
					    AddPlot("Mesh","Trajectories/E11_detrended_neu")
				else:
					    AddPlot("Mesh","Trajectories/E9_detrended_neu")
					    flyby = MeshAttributes()
					    flyby.legendFlag = 0
					    flyby.pointSizePixels = 5
					    SetPlotOptions(flyby)	
					    AddOperator("Project")
					    ProjectAtts = ProjectAttributes()
					    ProjectAtts.projectionType = ProjectAtts.XYCartesian  # ZYCartesian, XZCartesian, XYCartesian, XRCylindrical, YRCylindrical, ZRCylindrical
					    ProjectAtts.vectorTransformMethod = ProjectAtts.AsDirection  # None, AsPoint, AsDisplacement, AsDirection
					    SetOperatorOptions(ProjectAtts)
					    AddPlot("Mesh","Trajectories/E7_detrended_neu")
				flyby = MeshAttributes()
				flyby.legendFlag = 0
				flyby.pointSizePixels = 5
				flyby.meshColor = (0,0,0,255)
				SetPlotOptions(flyby)	
				AddOperator("Project")
				ProjectAtts = ProjectAttributes()
				ProjectAtts.projectionType = ProjectAtts.XYCartesian  # ZYCartesian, XZCartesian, XYCartesian, XRCylindrical, YRCylindrical, ZRCylindrical
				ProjectAtts.vectorTransformMethod = ProjectAtts.AsDirection  # None, AsPoint, AsDisplacement, AsDirection
				SetOperatorOptions(ProjectAtts)
				DrawPlots()



		#Abfrage auf Vektorfeld
		if fieldsVector[i] == 1:
			AddPlot("Vector", fieldsVectorName[i])
			vectors = VectorAttributes()
			vectors.useLegend = 0
			vectors.colorByMag = 0
			vectors.glyphLocation = vectors.UniformInSpace  # AdaptsToMeshResolution, UniformInSpace
			vectors.nVectors = 700
			vectors.autoScale = 1
			vectors.scale = 0.35
			vectors.lineWidth = 2
			SetPlotOptions(vectors)
			if typeofdata == "3d":
				AddOperator("Slice")
				sliceopts = SliceAttributes()
				if crosssec == "X":
					sliceopts.axisType = sliceopts.XAxis
				elif crosssec == "Y":
					sliceopts.axisType = sliceopts.YAxis
				elif crosssec == "Z":
					sliceopts.axisType = sliceopts.ZAxis
				sliceopts.originIntercept = interception
				SetOperatorOptions(sliceopts)
			DrawPlots()

		#setting the resolution for the png output
		s = SaveWindowAttributes()
		s.format = s.PNG
		s.fileName = namefiles +"_"+ fields[i]
		s.saveTiled = 0
		s.width = 1600
		s.height = 1600
		s.screenCapture = 0
		s.quality = 150
		s.outputToCurrentDirectory = 0
		s.outputDirectory = outputPath
		SetSaveWindowAttributes(s)
		SaveWindow()
		DeleteAllPlots()
	
exit()
