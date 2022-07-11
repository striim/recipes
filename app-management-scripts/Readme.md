## Python script start_applications.py
1. Create virtual environment 
    virtualenv venv
2. Source virtual environment
    source venv/bin/activate
3. Install requests
    pip install requests
4. Call python script
   
   python3 start_applications.py localhost admin test
   
   “[admin.HoptekLocation,admin.HoptekTruck]”
        Script command line arguments:
        
            1st arg: script name in this case start_applications.py
            2nd arg: hostname where the application is running in this case localhost
            3rd arg: login for striim url, in this case admin
            4th arg: password for striim url, in this case test
            5th arg: application name(s) with namescape, in this case [admin.HoptekLocation,admin.HoptekTruck] script will loop over each comma delimited value and deploy and start application
            
## Script logic:
1. Script will capture the login token and call the get endpoint to capture the current status of the application.
2. If the current status of the application is

    RUNNING: Script will
    
        1. Stop application
        2. Undeploy application
        3. Deploy application
        4. Start application
        
    HALT or STOPPED: script will
    
        1. Undeploy application
        2. Deploy application
        3. Start application
        
## Python script export_apps.py

1.	This script will export all applications from Striim and export them to a said directory with passphrase “admin”.
2.	If the directory does not exists script will create a directory under said path
3.	Call python script:
python3 export_apps.py localhost admin test /Users/srdandvanajscak/Downloads/StriimApps/
Script command line arguments:

            1st arg: script name in this case export_apps.py
            2nd arg: hostname where the application is running in this case localhost
            3rd arg: login for striim url, in this case admin
            4th arg: password for striim url, in this case test
            5th arg: said directory to export all Striim applications

## Python script import_apps.py

1.	This script will import all applications into Striim from said directory with passphrase “admin”.
2.	Script will only capture .tql files and import them into Striim
3.	Call python script:
python3 import_apps.py localhost admin test /Users/srdandvanajscak/Downloads/StriimApps/
Script command line arguments:

            1st arg: script name in this case import_apps.py
            2nd arg: hostname where the application is running in this case localhost
            3rd arg: login for striim url, in this case admin
            4th arg: password for striim url, in this case test
            5th arg: said directory that include all .tql files to import into Striim



