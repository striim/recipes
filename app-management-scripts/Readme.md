Python script start_applications.py</br>

1. Create virtual environment</br> 
    virtualenv venv</br>
2. Source virtual environment</br>
    source venv/bin/activate</br>
3. Install requests</br>
    pip install requests</br>
4. Call python script</br>
    python3 start_applications.py localhost admin test “[admin.AppTest1,admin.AppTest2]”</br>
        Script command line arguments:</br>
            1st arg: script name in this case start_applications.py </br>
            2nd arg: hostname where the application is running in this case localhost</br>
            3rd arg: login for striim url, in this case admin</br>
            4th arg: password for striim url, in this case test</br>
            5th arg: application name(s) with namespace, in this case “[admin.AppTest1,admin.AppTest2]” script will loop over each comma delimited value and deploy and start application</br>

Script logic:</br>
1. Script will capture the login token and call the get endpoint to capture the current status of the application.</br>
2. If the current status of the application is</br>
    RUNNING: Script will</br>
        1. Stop application</br>
        2. Undeploy application</br>
        3. Deploy application</br>
        4. Start application</br>
    HALT or STOPPED: script will</br>
        1. Undeploy application</br>
        2. Deploy application</br>
        3. Start application</br>

Python script export_apps.py</br>

1.	This script will export all applications from Striim and export them to a said directory with passphrase “admin”.</br>
2.	If the directory does not exists script will create a directory under said path</br>
3.	Call python script:</br>
python3 export_apps.py localhost admin test /Users/<username>/Downloads/StriimApps/</br>
Script command line arguments:</br>
            1st arg: script name in this case export_apps.py</br>
            2nd arg: hostname where the application is running in this case localhost</br>
            3rd arg: login for striim url, in this case admin</br>
            4th arg: password for striim url, in this case test</br>
            5th arg: said directory to export all Striim applications</br>

Python script import_apps.py</br>

1.	This script will import all applications into Striim from said directory with passphrase “admin”.</br>
2.	Script will only capture .tql files and import them into Striim</br>
3.	Call python script:</br>
python3 import_apps.py localhost admin test /Users/<username>/Downloads/StriimApps/</br>
Script command line arguments:</br>
            1st arg: script name in this case import_apps.py</br>
            2nd arg: hostname where the application is running in this case localhost</br>
            3rd arg: login for striim url, in this case admin</br>
            4th arg: password for striim url, in this case test</br>
            5th arg: said directory that include all .tql files to import into Striim</br>

