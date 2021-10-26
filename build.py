from zipfile import ZipFile
import glob
zipObj = ZipFile('cellworld_py.zip', 'w')

g = glob.glob("./cellworld_py/*.py")
for f in g:
    zipObj.write(f)

zipObj.close()
