import sys
from zipfile import ZipFile
import glob

version = ""
if len(sys.argv) > 1:
    version = "_" + sys.argv[1]

zipObj = ZipFile('build/cellworld_py' + version + '.zip', 'w')

g = glob.glob("./cellworld_py/*.py")
for f in g:
    zipObj.write(f)

zipObj.close()
