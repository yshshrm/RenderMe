import os
from pandas import read_pickle
import makehuman
makehuman.set_sys_path()
import human
import files3d
import wavefront
import humanmodifier

import pybetaface

humanoid = human.Human(files3d.loadMesh(human.getSysDataPath("3dobjs/base.obj")))
genmod = humanmodifier.MacroModifier('macrodetails','Gender')
agemod = humanmodifier.MacroModifier('macrodetails','Age')
musclemod = humanmodifier.MacroModifier('macrodetails-universal','Muscle')
weightmod = humanmodifier.MacroModifier('macrodetails-universal','Weight')
heightmod = humanmodifier.MacroModifier('macrodetails-height','Height')
body_proportionmod = humanmodifier.MacroModifier('macrodetails-proportions', 'BodyProportions')
heightmod.setHuman(humanoid)
agemod.setHuman(humanoid)
genmod.setHuman(humanoid)
weightmod.setHuman(humanoid)
musclemod.setHuman(humanoid)
body_proportionmod.setHuman(humanoid)

# def applyTarget(self, targetName, power):
# 	self.setDetail(os.path.abspath(os.curdir) + '/data/targets/' + targetName + '.target', power)
# 	self.applyAllTargets()

# fpa = 'C:\Users\\nabeel\Desktop\\objs\\'
fpa = os.path.abspath(os.curdir) + '/api_prod/static/api_prod/assets/models/'

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

def saviour(agee, gendere, weighte, body_proportion, heighte, name, key_string, image_path):
	if (gendere == 1):
		humanoid.setHeight(mcmtofr(heighte, agee))
	else:
		humanoid.setHeight(fcmtofr(heighte, agee))
	humanoid.setAgeYears(agee)
	humanoid.setWeight(weighte)
	humanoid.setGender(gendere)
	humanoid.setBodyProportions(body_proportion)
	if len(image_path) > 1:
		photo_instance = pybetaface.api.BetaFaceAPI()
		photo_info = photo_instance.upload_face(image_path, 'modestreet@internet')
		humanoid.setDetail()
		humanoid.applyAllTargets()

	wavefront.writeObjFile(fpa + name + '.obj' , humanoid.mesh)

def delete_obj(ide):
	os.remove(fpa + str(ide) + '.obj')
	os.remove(fpa + str(ide) + '.mtl')