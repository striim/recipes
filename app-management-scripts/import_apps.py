"""
1.  This script will import all applications into Striim from said directory with the passphrase “admin”.
2.  Script will only capture .tql files and import them into Striim
3.  Call python script:

python3 import_apps.py localhost admin test /Users/<username>/Downloads/StriimApps/
Script command-line arguments:
            1st arg: script name in this case import_apps.py
            2nd arg: hostname where the application is running in this case localhost
            3rd arg: login for Striim URL, in this case, admin
            4th arg: password for Striim URL, in this case, test
            5th arg: said directory that includes all .tql files to import into Striim
"""

from cmath import log
import requests
import os
import sys

login_url = "http://"+sys.argv[1]+":9080/security/authenticate"
export_url= "http://"+sys.argv[1]+":9080/api/v2/tungsten"
write_directory=sys.argv[4]

try:
    login_get_token_response = requests.post(login_url, data ={'username': ''+sys.argv[2]+'', 'password': ''+sys.argv[3]+''})
    login_get_token_response.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
login_token=login_get_token_response.json()['token']
print('TOKEN:'+str(login_token))

for filename in os.listdir(write_directory):
    f = os.path.join(write_directory,filename)
    if f.endswith('.tql') and os.path.isfile(f):
        print(f)
        try:
            headers = {
            "authorization": "STRIIM-TOKEN "+str(login_token),
            "content-type": "text/plain"
            }
            post_export = requests.post(export_url, data ="@"+f+" passphrase=admin;",headers=headers)
            if post_export.status_code == 200:
                print ('Application created succesfully!')
            else:
                print ('Application was not created!')
                post_export.raise_for_status()
            post_export.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

