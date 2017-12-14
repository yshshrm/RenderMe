import os
from pandas import read_pickle
import makehuman
makehuman.set_sys_path()
import human
import files3d
import wavefront
import humanmodifier
# import mh

humanoid = human.Human(files3d.loadMesh(human.getSysDataPath("3dobjs/base.obj")))
genmod = humanmodifier.MacroModifier('macrodetails','Gender')
agemod = humanmodifier.MacroModifier('macrodetails','Age')
musclemod = humanmodifier.MacroModifier('macrodetails-universal','Muscle')
weightmod = humanmodifier.MacroModifier('macrodetails-universal','Weight')
heightmod = humanmodifier.MacroModifier('macrodetails-height','Height')
heightmod.setHuman(humanoid)
agemod.setHuman(humanoid)
genmod.setHuman(humanoid)
weightmod.setHuman(humanoid)
musclemod.setHuman(humanoid)

humanoid.setDetail(os.path.abspath(os.curdir) + '/data/targets/nose/nose-volume-decr.target', 0.88)
humanoid.applyAllTargets()

# def applyTarget(self, targetName, power):
# 	self.setDetail(os.path.abspath(os.curdir) + '/data/targets/' + targetName + '.target', power)
# 	self.applyAllTargets()

# fpa = 'C:\Users\\nabeel\Desktop\\objs\\'
fpa = os.path.abspath(os.curdir) + '/mhclient/static/mhclient/assets/models/'

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

def saviour(agee,gendere,weighte,musclee,heighte,ide):
	if (gendere == 1):
		humanoid.setHeight(mcmtofr(heighte, agee))
	else:
		humanoid.setHeight(fcmtofr(heighte, agee))
	humanoid.setAgeYears(agee)
	humanoid.setWeight(weighte)
	humanoid.setGender(gendere)
	humanoid.setMuscle(musclee)
	wavefront.writeObjFile(fpa + str(ide) + '.obj' , humanoid.mesh)

def updator(agee,gendere,weighte,musclee,heighte,ide):
	if (gendere == 1):
		humanoid.setHeight(mcmtofr(heighte, agee))
	else:
		humanoid.setHeight(fcmtofr(heighte, agee))
	humanoid.setAgeYears(agee)
	humanoid.setWeight(weighte)
	humanoid.setGender(gendere)
	humanoid.setMuscle(musclee)
	delete_obj(ide)
	wavefront.writeObjFile(fpa + str(ide) + '.obj' , humanoid.mesh)

def delete_obj(ide):
	os.remove(fpa + str(ide) + '.obj')
	os.remove(fpa + str(ide) + '.mtl')