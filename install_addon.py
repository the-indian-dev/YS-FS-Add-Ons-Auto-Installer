import sys
import os
import shutil
import subprocess
import zipfile
import itertools
import threading
import time
import platform
'''
Of course you need to have Python installed on your system to use this script.
This script has been tested with Python 3.6.  It may run with Python 2.x, but I haven't tested.

BSD License.  Free for re-distribution.  Please feel free to customize for your own add-on package and bundle with package.

Usage:
    python install_addon.py package_zip_file.zip
     or
    python install_addon.py package_zip_file.zip install_directory
If you do not specify the install_directory, the script installs to the default YSFLIGHT user directory (~/Documents/YSFLIGHT.COM/YSFLIGHT)
'''



def DefaultFileList():
	return [
	]




def IsCommandAvailable(cmd):
	# From http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
	for path in os.environ["PATH"].split(os.pathsep):
		path=path.strip('"')
		#print("Searching "+cmd+" in "+path)
		exe_file=os.path.join(path,cmd)
		if os.path.isfile(exe_file) and os.access(exe_file,os.X_OK):
			return True
	#try:
	#	subprocess.Popen([cmd]).communicate()
	#except:
	#	return False
	return False



# srcPath/abc will be copied to dstPath/abc
# Also returns a list of copied files.
def ForceCopyTree(srcPath,instDir,dstPath):
	if not os.path.isdir(dstPath):
		os.makedirs(dstPath)

	copiedList=[]
	for fName in os.listdir(srcPath):
		srcFul=os.path.join(srcPath,fName)
		dstFul=os.path.join(instDir,dstPath,fName)

		if os.path.isfile(dstFul):
			os.remove(dstFul)

		if os.path.isdir(srcFul):
			if not os.path.isdir(dstFul):
				os.makedirs(dstFul)
			copiedList=copiedList+ForceCopyTree(srcFul,instDir,os.path.join(dstPath,fName))
		else:
			shutil.copyfile(srcFul,dstFul)
			copiedList.append(os.path.join(dstPath,fName).replace('\\','/'))

	return copiedList



# srcPath will be copied to dstPath.  dstPath must be a complete file name, not a directory name.
def ForceCopyFile(srcPath,dstPath):
	if os.path.isfile(dstPath):
		os.remove(dstPath)
	shutil.copyfile(srcPath,dstPath)



def FindUserDir(dir):
	for fName in os.listdir(dir):
		ful=os.path.join(dir,fName)
		if fName=="User" or fName=='user':
			return [ful,fName]
		elif os.path.isdir(ful):
			found=FindUserDir(ful)
			if []!=found:
				return found
	return []



def FindListFile(dir):
	lstFile=[]
	for fName in os.listdir(dir):
		ful=os.path.join(dir,fName)
		if os.path.isdir(ful):
			lstFile=lstFile+FindListFile(ful)
		else:
			ext=os.path.splitext(fName)[1].lower()
			if ext==".lst":
				lstFile.append([ful,fName])
	return lstFile



# Need to nuke a working directory after installation.
# Also I don't want to make a copied files read-only.
def MakeTreeWritable(dir):
	for fName in os.listdir(dir):
		ful=os.path.join(dir,fName)
		os.chmod(ful,0o777)
		if os.path.isdir(ful):
			MakeTreeWritable(ful)


def InstallAddOn(zipFName,instDir):
	airDir=os.path.join(instDir,"aircraft")
	gndDir=os.path.join(instDir,"ground")
	scnDir=os.path.join(instDir,"scenery")
	for dir in [airDir,gndDir,scnDir]:
		if not os.path.isdir(dir):
			os.makedirs(dir)


	workDir=os.path.join(instDir,"tempDir")
	if os.path.isdir(workDir):
		shutil.rmtree(workDir)
	os.makedirs(workDir)

	pushd=os.getcwd()


	print("________________________________________________________________")
	print("Add-On Name: "+zipFName)
	print("________________________________________________________________")
	print('')
	zip=zipfile.ZipFile(zipFName,"r")

	os.chdir(workDir)
	zip.extractall()
	MakeTreeWritable(os.getcwd())

	userDir=FindUserDir(workDir)
	print("Found user dir: ")
	print(userDir)

	lstFile=FindListFile(workDir)
	print("Found list files:")
	print(lstFile)

	if []==userDir:
		print(f"{bcolors.FAIL}ERROR : Cannot Find User Directory{bcolors.ENDC}")
		return

	dataFile=ForceCopyTree(userDir[0],instDir,userDir[1])

	leftUninstalled=[]
	installedAirList=[]
	installedGndList=[]
	installedScnList=[]
	for lst in lstFile:
		if lst[1]=='scenary.lst' or lst[1]=='scenery.lst' or lst[1]=='aircraft.lst' or lst[1]=='ground.lst':
			# Sorry for misspelling 'scenary'!
			print("Skipping a generic .lst name:"+lst[1])
			print("Probably intended to overwrite the default .lst file?")
			continue

		if lst[1].startswith("air"):
			print("Installing "+lst[1]+" to aircraft")
			ForceCopyFile(lst[0],os.path.join(airDir,lst[1]))
			installedAirList.append(os.path.join(airDir,lst[1]))
		elif lst[1].startswith("gro"):
			print("Installing "+lst[1]+" to ground")
			ForceCopyFile(lst[0],os.path.join(gndDir,lst[1]))
			installedGndList.append(os.path.join(gndDir,lst[1]))
		elif lst[1].startswith("sce"):
			print("Installing "+lst[1]+" to scenery")
			ForceCopyFile(lst[0],os.path.join(scnDir,lst[1]))
			installedScnList.append(os.path.join(scnDir,lst[1]))
		else:
			leftUninstalled.append(lst[1])
			print("Warning!  Cannot identify the .lst file type ("+lst[1]+")");
			print("          This .lst file hasn't been installed.")

	if 0<len(leftUninstalled):
		print("Following .lst files haven't been installed.")
		print(leftUninstalled)



	FixCapitalization(instDir,installedAirList,installedGndList,installedScnList,dataFile)



	os.chdir(pushd)
	shutil.rmtree(workDir)



def InstallMultiAddOn(zipDirName,instDir):
	for zipFName in os.listdir(zipDirName):
		ext=os.path.splitext(zipFName)[1].lower()
		if ext=='.zip':
			zipFul=os.path.join(zipDirName,zipFName)
			print("["+zipFName+"]")
			InstallAddOn(zipFul,instDir)



################################################################################


def TryCorrectFileName(fName,lowerToActual):
	actual=lowerToActual.get(fName.lower().replace('"',''))
	if actual==None:
		if fName.startswith("aircraft/") or fName.startswith("ground/") or fName.startswith("scenery/"):
			print("File "+fName+" is probably a reference to a default file.")
		else:
			print("Warning: File "+fName+" does not exist.")
		return (False,fName)

	if None!=actual and fName!=actual:
		print("Correcting Capitalization: "+fName+" to "+actual)
		return (True,actual)
	else:
		return (False,fName)



def FixCapitalizationPerDatFile(datFName,lowerToActual,keywordDict):
	try:
		fp=open(datFName,"r")
	except:
		print("File "+datFName+" does not exist.")
		return

	updated=False
	fileContent=[]
	for s in fp:
		argv=s.split()
		if 0<len(argv) and None!=keywordDict.get(argv[0].upper()):
			(tf,newFName)=TryCorrectFileName(argv[1],lowerToActual)
			if True==tf:
				updated=True;
				s=s.replace(argv[1],newFName)
		fileContent.append(s)

	fp.close()

	if True==updated:
		print("Writing "+datFName)
		fp=open(datFName,"w")
		for s in fileContent:
			fp.write(s+"\n")
		fp.close()



def FixCapitalizationPerListFile(listFName,lowerToActual,skipFirstArg):
	txt=[]
	ifp=open(listFName,"r")
	for s in ifp:
		txt.append(s)
	ifp.close()

	newTxt=[]
	updated=False

	for s in txt:
		argv=s.split()
		first=True
		for arg in argv:
			if True==first and True==skipFirstArg:
				first=False
				continue

			(tf,actual)=TryCorrectFileName(arg,lowerToActual)
			if True==tf:
				updated=True
				print("Correcting Capitalization: "+arg+" to "+actual)
				s=s.replace(arg,actual)

			first=False

		newTxt.append(s)

	if True==updated:
		print("Updating: "+listFName)
		ofp=open(listFName,"w")
		for s in newTxt:
			ofp.write(s+"\n")
		ofp.close()




def FixCapitalization(instDir,airListFName,gndListFName,scnListFName,dataFile):
	lowerToActual=dict()
	for f in dataFile:
		lowerToActual[f.lower()]=f

	for fName in airListFName:
		FixCapitalizationPerListFile(fName,lowerToActual,False)

	for fName in gndListFName:
		FixCapitalizationPerListFile(fName,lowerToActual,False)

		try:
			fp=open(fName,"r")
		except:
			print("Cannot open "+fName)
			continue

		for s in fp:
			argv=s.split()
			if 0<len(argv):
				datFName=os.path.join(instDir,argv[0])
				datFName=os.path.expanduser(datFName)
				FixCapitalizationPerDatFile(datFName,lowerToActual,{"CARRIER":0})
		fp.close()

	for fName in scnListFName:
		FixCapitalizationPerListFile(fName,lowerToActual,True)
# Colours :)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
################################################################################



def main():
	if platform.release() == 'Windows' :
		os.system('cls')
	else:
		os.system('clear')
	if len(sys.argv)<2:
		print("Usage: python install_addon.py input_zip_file.zip install_destination_directory")
		print("            or,")
		print("       python install_addon.py input_zip_file.zip")
		print("  If you don't specify the destination, it uses ~/YSFLIGHT.COM/YSFLIGHT as the")
		print("  default YSFLIGHT user-data install location.")
	elif 3<=len(sys.argv):
		if not os.path.isdir(sys.argv[2]):
			os.makedirs(sys.argv[2])
		instDir=sys.argv[2]
	else:
		instDir=os.path.join("~","Documents","YSFLIGHT.COM","YSFLIGHT")
		instDir=os.path.expanduser(instDir)
	InstallAddOn(sys.argv[1],instDir)
	print(f"{bcolors.OKGREEN}Installation Done!{bcolors.ENDC}")
	print(f"{bcolors.OKBLUE}Enjoy :){bcolors.ENDC}")

if __name__=="__main__":
	try :
		main()
	except :
		print(f"{bcolors.FAIL}Installation Failed :( {bcolors.ENDC}")
