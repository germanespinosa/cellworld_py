import zipfile
import requests


def download (url, path = None):
    web_get = requests.get(url)
    if not path:
        path = url.split("/")[-1]
    with open(path, "wb") as f:
        f.write(web_get.content)


def extract(file_name):
    zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
    zip_ref.extractall(".")  # extract file to dir
    zip_ref.close()  # close file


def install(version = ""):
    if version:
        version = "_" + version
    download("https://github.com/germanespinosa/cellworld_py/raw/master/build/cellworld_py" + version + ".zip", "cellworld_py.zip")
    extract("cellworld_py.zip")