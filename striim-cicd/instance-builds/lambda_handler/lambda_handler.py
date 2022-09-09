import boto3

ec2 = boto3.client('ec2')
rds = boto3.client('rds')

ec2_instances = []

rds_response = rds.describe_db_instances()
                    
def rds_instance(response, state):
    
    # Locate all instances that are tagged ttl.
    for instance in rds_response["DBInstances"]:
        
        if instance['DBInstanceStatus'] == state:
            
            tags = rds.list_tags_for_resource(ResourceName=instance["DBInstanceArn"])
                    
            for tag in tags["TagList"]:
                if tag['Key'] == 'Auto-Start':
                    if tag['Value'] == 'true':
                            
                        if state == 'available':

                            rds.stop_db_instance(DBInstanceIdentifier=instance["DBInstanceIdentifier"])
                            print("Stopped RDS Instance: ", instance["DBInstanceIdentifier"])
                        
                        elif state == 'stopped':
                            
                            rds.start_db_instance(DBInstanceIdentifier=instance["DBInstanceIdentifier"])
                            print("Started RDS Instance: ", instance["DBInstanceIdentifier"])

def describe_ec2_instances(state):

    response = ec2.describe_instances(Filters=[
            {
                'Name': 'tag:Auto-Start',
                'Values': [
                    'true',
                ]
            },
        ])
    
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance['State']['Name'] == state:
                ec2_instances.append(instance["InstanceId"])
    return ec2_instances

def stop(event, context):
    ec2_instances = describe_ec2_instances('running')
    rds_instance(rds_response, 'available')
    
    if ec2_instances:
        ec2.stop_instances(InstanceIds=ec2_instances)
        print('Stopped EC2 instances: ' + str(ec2_instances))
    else: 
        print('No Instances with Auto-Start tag.')
        
def start(event, context):
    ec2_instances = describe_ec2_instances('stopped')
    rds_instance(rds_response, 'stopped')
    
    if ec2_instances:
        ec2.start_instances(InstanceIds=ec2_instances)
        print('Started EC2 instances: ' + str(ec2_instances))
    else: 
        print('No Instances with Auto-Start tag.')
