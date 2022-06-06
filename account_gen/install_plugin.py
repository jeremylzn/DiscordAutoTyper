import urllib.request
import zipfile

url = 'https://antcpt.com/anticaptcha-plugin.zip'
# download the plugin
filehandle, _ = urllib.request.urlretrieve(url)
# unzip it
with zipfile.ZipFile(filehandle, "r") as f:
    f.extractall("plugin")

from pathlib import Path
import zipfile
import os

# set API key in configuration file
api_key = "2a6b07b13f06fc3123da2d8f58168978"
file = Path('./plugin/js/config_ac_api_key.js')
file.write_text(file.read_text().replace("antiCapthaPredefinedApiKey = ''", "antiCapthaPredefinedApiKey = '{}'".format(api_key)))

# zip plugin directory back to plugin.zip
zip_file = zipfile.ZipFile('./plugin.zip', 'w', zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk("./plugin"):
        for file in files:
            path = os.path.join(root, file)
            zip_file.write(path, arcname=path.replace("./plugin/", ""))
zip_file.close()