import os
from pandas import read_pickle
import makehuman
makehuman.set_sys_path()
import human
import files3d
import wavefront
import humanmodifier

import json
from pybetaface import api

humanoid = human.Human(files3d.loadMesh(human.getSysDataPath("3dobjs/base.obj")))

genmod = humanmodifier.MacroModifier('macrodetails','Gender')
agemod = humanmodifier.MacroModifier('macrodetails','Age')
musclemod = humanmodifier.MacroModifier('macrodetails-universal','Muscle')
weightmod = humanmodifier.MacroModifier('macrodetails-universal','Weight')
heightmod = humanmodifier.MacroModifier('macrodetails-height','Height')
body_proportionmod = humanmodifier.MacroModifier('macrodetails-proportions', 'BodyProportions')
africanmod = humanmodifier.MacroModifier('macrodetails','African')
asianmod = humanmodifier.MacroModifier('macrodetails','Asian')
caucasianmod = humanmodifier.MacroModifier('macrodetails','Caucasian')


heightmod.setHuman(humanoid)
agemod.setHuman(humanoid)
genmod.setHuman(humanoid)
weightmod.setHuman(humanoid)
musclemod.setHuman(humanoid)
body_proportionmod.setHuman(humanoid)
africanmod.setHuman(humanoid)
caucasianmod.setHuman(humanoid)
asianmod.setHuman(humanoid)

# def applyTarget(self, targetName, power):
# 	self.setDetail(os.path.abspath(os.curdir) + '/data/targets/' + targetName + '.target', power)
# 	self.applyAllTargets()

# fpa = 'C:\Users\\nabeel\Desktop\\objs\\'
fpa = os.path.abspath(os.curdir) + '/api_prod/static/api_prod/assets/models/'
dpa = os.path.abspath(os.curdir) + '/data/targets/'

dfma = read_pickle('ma.p')
dffem = read_pickle('fem.p')

def mcmtofr(hcm, agee):
	a2 = 0
	for i in range(0,101,2):
		if dfma[i][agee] > hcm:
			a2 = i
			break
	b2 = dfma[a2][agee]
	b1 = dfma[(a2 - 2)][agee]
	conv = (hcm - b1)/(b2 - b1)
	return ((a2 - 2)*(1- conv) + (a2)*(conv))/100.0

def fcmtofr(hcm, agee):
	a2 = 0
	for i in range(0,101,2):
		if dffem[i][agee] > hcm:
			a2 = i
			break
	b2 = dffem[a2][agee]
	b1 = dffem[(a2 - 2)][agee]
	conv = (hcm - b1)/(b2 - b1)
	return ((a2 - 2)*(1- conv) + (a2)*(conv))/100.0


		
def saviour(age, gendere, weighte, body_proportion, heighte, name, key_string, image_path, chest_cm, waist_cm, skin_color):

	if(skin_color == '1'):
		humanoid.setCaucasian(1)
	elif(skin_color == '2'):
		humanoid.setCaucasian(0.7)
	elif(skin_color == '4'):
		humanoid.setAsian(0.5)
	elif(skin_color == '5'):
		humanoid.setAfrican(0.6)
	elif(skin_color == '6'):
		humanoid.setAfrican(0.7)
	
	if (gendere == 1):
		humanoid.setHeight(mcmtofr(heighte, age))
	else:
		humanoid.setHeight(fcmtofr(heighte, age))

	humanoid.setAgeYears(age)
	humanoid.setGender(gendere)

	# setting muscle to zero is the only way after which we can add fat to the body (by increasing weight, through calculating BMI)
	humanoid.setMuscle(0)

	BMI = weighte / ((heighte/100) * (heighte/100))

	if (BMI > 30):
		humanoid.setWeight(0.9)
	elif (BMI > 26):
		humanoid.setWeight(0.7)
	elif (BMI > 18.5):
		humanoid.setWeight(0.5)
	else:
		humanoid.setWeight(0.3)

	## Modelling the face using BetaFaceAPI
	if(len(image_path) > 1):

		print "Inside facial modelling"
		photo_instance = api.BetaFaceAPI()
		photo_info = photo_instance.upload_face(image_path, 'modestreet@internet')

		for info in photo_info:
			prop = info['name'].encode('utf-8')
			value = info['value'].encode('utf-8')
			
			if(float(info['confidence'].encode('utf-8')) < 0.5):
				continue

			### eyes
			if(prop == 'eyes distance'):
				if(value == 'extra far'):
					humanoid.setDetail(dpa + 'eyes/l-eye-trans-out.target', 0.6)
					humanoid.setDetail(dpa + 'eyes/r-eye-trans-out.target', 0.6)
				elif(value == 'far'):
					humanoid.setDetail(dpa + 'eyes/l-eye-trans-out.target', 0.3)
					humanoid.setDetail(dpa + 'eyes/r-eye-trans-out.target', 0.3)
				elif(value == 'close'):
					humanoid.setDetail(dpa + 'eyes/l-eye-trans-in.target', 0.3)
					humanoid.setDetail(dpa + 'eyes/r-eye-trans-in.target', 0.3)
				elif(value == 'extra close'):
					humanoid.setDetail(dpa + 'eyes/l-eye-trans-in.target', 0.6)
					humanoid.setDetail(dpa + 'eyes/r-eye-trans-in.target', 0.6)

			elif(prop == 'eyes position'):
				if(value == 'extra low'):
					humanoid.setDetail(dpa + 'eyes/l-eye-trans-down.target', 0.6)
					humanoid.setDetail(dpa + 'eyes/r-eye-trans-down.target', 0.6)
				elif(value == 'low'):
					humanoid.setDetail(dpa + 'eyes/l-eye-trans-down.target', 0.3)
					humanoid.setDetail(dpa + 'eyes/r-eye-trans-down.target', 0.3)
				elif(value == 'high'):
					humanoid.setDetail(dpa + 'eyes/l-eye-trans-up.target', 0.3)
					humanoid.setDetail(dpa + 'eyes/r-eye-trans-up.target', 0.3)
				elif(value == 'extra high'):
					humanoid.setDetail(dpa + 'eyes/l-eye-trans-up.target', 0.6)
					humanoid.setDetail(dpa + 'eyes/r-eye-trans-up.target', 0.6)
			
			elif(prop == 'eyes shape'):
				if(value == 'extra round'):
					humanoid.setDetail(dpa + 'eyes/l-eye-height2-incr.target', 0.6)
					humanoid.setDetail(dpa + 'eyes/r-eye-height2-incr.target', 0.6)
				elif(value == 'round'):
					humanoid.setDetail(dpa + 'eyes/l-eye-height2-incr.target', 0.3)
					humanoid.setDetail(dpa + 'eyes/r-eye-height2-incr.target', 0.3)
				elif(value == 'thin'):
					humanoid.setDetail(dpa + 'eyes/l-eye-height2-decr.target', 0.3)
					humanoid.setDetail(dpa + 'eyes/r-eye-height2-decr.target', 0.3)
				elif(value == 'extra thin'):
					humanoid.setDetail(dpa + 'eyes/l-eye-height2-decr.target', 0.6)
					humanoid.setDetail(dpa + 'eyes/r-eye-height2-decr.target', 0.6)

			### mouth
			elif(prop == 'mouth corners'):
				if(value == 'extra low'):
					humanoid.setDetail(dpa + 'mouth/mouth-angles-down.target', 0.6)
				elif(value == 'low'):
					humanoid.setDetail(dpa + 'mouth/mouth-angles-down.target', 0.3)
				elif(value == 'raised'):
					humanoid.setDetail(dpa + 'mouth/mouth-angles-up.target', 0.3)
				elif(value == 'extra raised'):
					humanoid.setDetail(dpa + 'mouth/mouth-angles-up.target', 0.6)

			elif(prop == 'mouth height'):
				if(value == 'extra thick'):
					humanoid.setDetail(dpa + 'mouth/mouth-scale-vert-incr.target', 0.6)
				elif(value == 'thick'):
					humanoid.setDetail(dpa + 'mouth/mouth-scale-vert-incr.target', 0.3)
				elif(value == 'thin'):
					humanoid.setDetail(dpa + 'mouth/mouth-scale-vert-decr.target', 0.3)
				elif(value == 'extra thin'):
					humanoid.setDetail(dpa + 'mouth/mouth-scale-vert-decr.target', 0.6)

			elif(prop == 'mouth width'):
				if(value == 'extra wide'):
					humanoid.setDetail(dpa + 'mouth/mouth-scale-horiz-incr.target', 0.6)
				elif(value == 'wide'):
					humanoid.setDetail(dpa + 'mouth/mouth-scale-horiz-incr.target', 0.3)
				elif(value == 'small'):
					humanoid.setDetail(dpa + 'mouth/mouth-scale-horiz-decr.target', 0.3)
				elif(value == 'extra small'):
					humanoid.setDetail(dpa + 'mouth/mouth-scale-horiz-decr.target', 0.6)


			### nose
			elif(prop == 'nose width'):
				if(value == 'extra wide'):
					humanoid.setDetail(dpa + 'nose/nose-scale-horiz-incr.target', 0.6)
				elif(value == 'wide'):
					humanoid.setDetail(dpa + 'nose/nose-scale-horiz-incr.target', 0.3)
				elif(value == 'narrow'):
					humanoid.setDetail(dpa + 'nose/nose-scale-horiz-decr.target', 0.3)
				elif(value == 'extra narrow'):
					humanoid.setDetail(dpa + 'nose/nose-scale-horiz-decr.target', 0.6)
			
			elif(prop == 'nose shape'):
				if(value == 'extra straight'):
					humanoid.setDetail(dpa + 'nose/nose-width1-incr.target', 0.6)
				elif(value == 'straight'):
					humanoid.setDetail(dpa + 'nose/nose-width1-incr.target', 0.3)
				elif(value == 'triangle'):
					humanoid.setDetail(dpa + 'nose/nose-width1-decr.target', 0.3)
				elif(value == 'extra triangle'):
					humanoid.setDetail(dpa + 'nose/nose-width1-decr.target', 0.6)
				
			## head
			elif(prop == 'chin size'):
				if(value == 'extra large'):
					humanoid.setDetail(dpa + 'chin/chin-width-incr.target', 0.6)
				elif(value == 'large'):
					humanoid.setDetail(dpa + 'chin/chin-width-incr.target', 0.3)
				elif(value == 'small'):
					humanoid.setDetail(dpa + 'chin/chin-width-decr.target', 0.3)
				elif(value == 'extra small'):
					humanoid.setDetail(dpa + 'chin/chin-width-decr.target', 0.6)

			elif(prop == 'head shape'):
				if(value == 'extra heart'):
					humanoid.setDetail(dpa + 'head/head-invertedtriangular.target', 0.5)
				elif(value == 'heart'):
					humanoid.setDetail(dpa + 'head/head-invertedtriangular.target', 0.3)
				elif(value == 'rect'):
					humanoid.setDetail(dpa + 'head/head-rectangular.target', 0.3)
				elif(value == 'extra rect'):
					humanoid.setDetail(dpa + 'head/head-rectangular.target', 0.5)
	
	## move ear wings inwards, looks better with ears adjusted
	humanoid.setDetail(dpa + 'ears/l-ear-wing-decr.target', 0.5)
	humanoid.setDetail(dpa + 'ears/r-ear-wing-decr.target', 0.5)

	humanoid.applyAllTargets()

	print humanoid.targetsDetailStack
	wavefront.writeObjFile(fpa +  name + '.obj', humanoid.mesh)

def delete_obj(ide):
	os.remove(fpa + str(ide) + '.obj')
	os.remove(fpa + str(ide) + '.mtl')