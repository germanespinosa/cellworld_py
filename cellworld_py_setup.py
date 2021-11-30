import zipfile
import requests
import os

def download(url, path=None):
    web_get = requests.get(url)
    if not path:
        path = url.split("/")[-1]
    with open(path, "wb") as f:
        f.write(web_get.content)


def extract(file_name):
    zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
    zip_ref.extractall(".")  # extract file to dir
    zip_ref.close()  # close file


def install(version="", force=False):
    is_installed = False
    try:
        import cellworld_py
    except:
        pass
    try:
        if cellworld_py.version() == version:
            is_installed = True
    except:
        pass

    if is_installed and not force:
        return

    version_v = ""

    if version:
        version_v = "_" + version

    url = "https://github.com/germanespinosa/cellworld_py/raw/master/build/cellworld_py" + version_v + ".zip?rnd=" + str(random.Random())
    try:
        download(url, "cellworld_py.zip")
    except:
        raise ValueError('cellworld_py version ' + version + 'installation from "' + url + '" failed')

    extract("cellworld_py.zip")
    os.remove("cellworld_py.zip")
    print('cellworld_py version ' + version + ' installed')
