# importing the requests library
#sample call: python3 deploy_app.py localhost admin test "[admin.HoptekLocation,admin.HoptekTruck]"   
from cmath import log
import requests
import sys

#capture token for logins

l = len(sys.argv[4])
li = sys.argv[4][1:l-1].split(',')

for application in li:
    print('Start application '+application)

    login_url = "http://"+sys.argv[1]+":9080/security/authenticate"
    get_status_url="http://"+sys.argv[1]+":9080/api/v2/applications/"+application
    deploy_url= "http://"+sys.argv[1]+":9080/api/v2/applications/"+application+"/deployment"
    start_url= "http://"+sys.argv[1]+":9080/api/v2/applications/"+application+"/sprint"
    
    try:
        login_get_token_response = requests.post(login_url, data ={'username': ''+sys.argv[2]+'', 'password': ''+sys.argv[3]+''})
        login_get_token_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    login_token=login_get_token_response.json()['token']
    print('TOKEN:'+str(login_token))

    try:
        print('Capturing current status of application')
        headers = {
        "authorization": "STRIIM-TOKEN "+str(login_token),
        "content-type": "application/json"
        }
        get_status_response = requests.get(get_status_url,headers=headers)
        status = get_status_response.json()['status']
        print('Current application status = '+status)
        get_status_response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    if status == 'RUNNING':
        print('Applicaiton is in RUNNING status, Stopping and Undeploying application')
        try:
            print('Stopping Application')
            stop_export = requests.delete(start_url,headers=headers)
            if stop_export.status_code == 200:
                print ('Application '+application+' stopped succesfully!')
            else:
                print ('Application '+application+' stopped unsuccessful!')
                stop_export.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        try:
            print('Undeploying Application')
            undeploy_export = requests.delete(deploy_url,headers=headers)
            if undeploy_export.status_code == 200:
                print ('Application '+application+' undeployed succesfully!')
            else:
                print ('Application '+application+' undeployed unsuccessful!')
                undeploy_export.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    elif status == 'HALT' or status == 'STOPPED':
        print('Application is in '+status+' status, Undeploying application')
        try:
            print('Undeploying Application')
            undeploy_export = requests.delete(deploy_url,headers=headers)
            if undeploy_export.status_code == 200:
                print ('Application '+application+' undeployed succesfully!')
            else:
                print ('Application '+application+' undeployed unsuccessful!')
                undeploy_export.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    #Call rest api to deploy application
    try:
        headers = {
        "authorization": "STRIIM-TOKEN "+str(login_token),
        "content-type": "application/json"
        }
        deploy_export = requests.post(deploy_url, data ='{"deploymentGroupName": "default","deploymentType": "ANY", "flows": []}',headers=headers)
        if deploy_export.status_code == 200:
            print ('Application '+application+' deployed succesfully!')
        else:
            try:
                print('Deploy Application')
                deploy_export = requests.post(deploy_url, data ='{"deploymentGroupName": "default","deploymentType": "ANY", "flows": []}',headers=headers)
                if deploy_export.status_code == 200:
                    print ('Application '+application+' deployed succesfully!')
                else:
                    print ('Application '+application+' deployed unsuccessful!')
                    deploy_export.raise_for_status()
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    #Call rest api to start application
    try:
        headers = {
        "authorization": "STRIIM-TOKEN "+str(login_token),
        }
        post_login = requests.post(start_url,headers=headers)
        if post_login.status_code == 200:
            print ('Application '+application+' started succesfully!')
        else:
            print('Please make sure your application is not already deployed.')
            post_login.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
