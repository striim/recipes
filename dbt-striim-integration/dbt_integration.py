#!/usr/bin/python3
import requests
import json
from time import sleep
import subprocess

def getUserInputs():
  user_inputs = []

  pId = input("Enter Project ID: ")

  print("Choose dbt command")
  print("0. dbt run")
  print("1. dbt source freshness")
  print("2. Full")
  dbt_op_type = int(input("Enter value (0-2): "))

  while dbt_op_type < 0 or dbt_op_type > 2:
    op_type = int(input("Invalid value. Please choose value 0-2: "))

  print("Choose type of operation")
  print("0. Delete")
  print("1. DDLs")
  print("2. PKUpdates")
  print("3. Updates")
  print("4. Inserts")
  print("5. Time Interval")
  op_type = int(input("Enter value (0-5): "))
  
  while op_type < 0 or op_type > 5:
    op_type = int(input("Invalid value. Please choose value 0-5: "))

  if op_type != 5:
    op_count = int(input("Enter scheduling count: "))
  else:
    op_count = int(input("Enter time interval to check in seconds: "))

  if op_type == 0:
    op_type = 'Deletes'
  elif op_type == 1:
    op_type = 'DDLs'
  elif op_type == 2:
    op_type = 'PKUpdates'
  elif op_type == 3:
    op_type = 'Updates'
  elif op_type == 4:
    op_type = 'Inserts'
  else:
    op_type = 'Timed'

  user_inputs.append(op_type)
  user_inputs.append(op_count)
  user_inputs.append(dbt_op_type)
  user_inputs.append(pId)

  return(user_inputs)

def getOperationCounts():
  url = 'https://gcp-us.striim.dev/***/api/v2/tungsten'
  payload = 'MON dbt.dbt_pg_source;'
  headers = {
    'Authorization': 'STRIIM-TOKEN ssssssssssPT0J.rQZzZfmmmmmm***mn',
    'Content-Type': 'text/plain'
    }
  
  response = requests.post(url, data=payload, headers=headers)
  r_status = json.loads(response.text)[0]['executionStatus']
  r_json = json.loads(json.loads(response.text)[0]['output']['cdcOperation'])
  operationCounts = {
    'Status': r_status,
    'Deletes': r_json['No of Deletes'],
    'DDLs': r_json['No of DDLs'],
    'PKUpdates': r_json['No of PKUpdates'],
    'Updates': r_json['No of Updates'],
    'Inserts': r_json['No of Inserts']
  }

  return operationCounts

def runDBTOperations(pId, operation):
  url = f"https://cloud.getdbt.com/api/v2/accounts/****/jobs/{pId}/run/"

  if operation == 0:
    payload = '{ \
      "cause": "API Post", \
      "steps_override": [ \
        "dbt run" \
      ] \
    }'
  elif operation == 1:
    payload = '{ \
      "cause": "API Post", \
      "steps_override": [ \
        "dbt source freshness" \
      ] \
    }'
  else:
    payload = '{ \
      "cause": "API Post", \
      "steps_override": [ \
        "dbt source freshness", \
        "dbt run" \
      ] \
    }'
  
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 29c************806d14****dcbd'
  }

  response = requests.post(url, data=payload, headers=headers).json()
  run_status = {
    'Status': response['status']['code'],
    'Dbt Operations': response['data']['trigger']['steps_override']
  }
  return run_status


def monCDCOperations():
  user_inputs = getUserInputs()
  op_type = user_inputs[0]
  op_count = user_inputs[1]
  dbt_op_type = user_inputs[2]
  pId = user_inputs[3]
  mon_cdc = False

  cdc_op_count = getOperationCounts()
  sleep(2)
  if cdc_op_count['Status'] == 'Success':
    mon_cdc = True
  else:
    print('Please check on your cdc source app')
    return

  if op_type != 'Timed':
    prev = cdc_op_count[op_type]
    next_check = prev + op_count
    print("####################\tChecking Striim CDC Operations\t####################")
    while mon_cdc:
      print(f"####################\tRunning when {op_type} hits {next_check}\t####################")
      cdc_op_count = getOperationCounts()
      sleep(2)
      print(cdc_op_count)
      if cdc_op_count[op_type] >= prev + op_count:

        if dbt_op_type == 0:
          print("Running dbt run")
          # subprocess.run(['dbt', 'run', '-m', 'models/staging/*'])
          dbt_run_res = runDBTOperations(pId, dbt_op_type)

        if dbt_op_type == 1:
          print("Running dbt freshness")
          # subprocess.run(['dbt', 'source', 'freshness'])
          dbt_run_res = runDBTOperations(pId, dbt_op_type)

        if dbt_op_type == 2:
          print("Running dbt run and dbt source freshness")
          dbt_run_res = runDBTOperations(pId, dbt_op_type)
        
        sleep(2)
        if dbt_run_res['Status'] == 200:
          print(f"{dbt_run_res} SUCCESSFUL")
        else:
          print(f"{dbt_run_res} FAILED. Please check on your cloud job.")
          return

        prev = prev + op_count
        next_check = prev + op_count
      sleep(5)
  else:
    print(f"####################\tRunning dbt every {op_count} seconds \t####################")
    while mon_cdc:
      dbt_run_res = runDBTOperations(pId, dbt_op_type)
      if dbt_run_res['Status'] == 200:
        print(f"{dbt_run_res} SUCCESSFUL")
      else:
        print(f"{dbt_run_res} FAILED. Please check on your cloud job.")
        return

      sleep(op_count)

  return
  

monCDCOperations()
