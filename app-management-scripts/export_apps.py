# importing the requests library
#1.  This script will export all applications from Striim and export them to a directory with the passphrase “admin”.
#2.  If the directory does not exist script will create a directory under the said path
#3.  Call python script:
#
#python3 export_apps.py localhost admin test /Users/srdandvanajscak/Downloads/StriimApps/
#Script command-line arguments:
#            1st arg: script name in this case export_apps.py
#            2nd arg: hostname where the application is running in this case localhost
#            3rd arg: login for Striim URL, in this case, admin
#            4th arg: password for Striim URL, in this case, test
#            5th arg: said directory to export all Striim applications

from cmath import log
import requests
import zipfile
import os
import sys

login_url = "http://"+sys.argv[1]+":9080/security/authenticate"
export_url= "http://"+sys.argv[1]+":9080/api/v2/tungsten"
write_zip_directory=sys.argv[4]+"/AllAppsBackups.zip"
write_directory=sys.argv[4]

try:
    login_get_token_response = requests.post(login_url, data ={'username': ''+sys.argv[2]+'', 'password': ''+sys.argv[3]+''})
    login_get_token_response.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
login_token=login_get_token_response.json()['token']
print('TOKEN:'+str(login_token))

try:
    headers = {
    "authorization": "STRIIM-TOKEN "+str(login_token),
    "content-type": "text/plain"
    }
    print('Writing files to directory:'+write_directory)
    post_export = requests.post(export_url, data ="EXPORT APPLICATION ALL passphrase=admin;",headers=headers)
    post_export.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

os.makedirs(os.path.dirname(write_zip_directory), exist_ok=True)
with open(write_zip_directory, 'wb') as f:
    f.write(post_export.content)

with zipfile.ZipFile(write_zip_directory,"r") as zip_ref:
    zip_ref.extractall(write_directory)
    print('Files written and unzipped to:'+write_directory)
    try:
        headers = {
        "authorization": "STRIIM-TOKEN "+str(login_token),
        "content-type": "text/plain"
        }
        print('Writing files to directory:'+write_directory)
        post_export = requests.post(export_url, data ="EXPORT APPLICATION ALL passphrase=test;",headers=headers)
        post_export.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)