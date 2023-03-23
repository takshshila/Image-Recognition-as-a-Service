import boto3
from ec2_metadata import ec2_metadata
import time

ec2 = boto3.client("ec2", region_name='us-east-1', aws_access_key_id='AKIAQ2HI4V3WNTGN7OXI',
                   aws_secret_access_key='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')
# print(ec2)
user_data='''#!/bin/bash
source ~/.nvm/nvm.sh
node -e "console.log('Running Node.js ' + process.version)"
cd /home/ec2-user
node instance_manager.js
'''

def create_ec2_instance(num):
    try:
        ec2.run_instances(
            ImageId="ami-0fb5b309158aece3f",
            UserData=user_data,
            MinCount=1,
            MaxCount=1,
            InstanceType = 't2.micro',
            KeyName='TakshshilaWebTier1',
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'appTier'+str(num)
                        },
                    ]
                },
            ],
        )
    except Exception as e:
        print(e)

def get_num_app_instances():
    instanceCount=0
    reservations = ec2.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running","pending"],
        }
    ]).get("Reservations")
    # print(reservations)
    for reservation in reservations:
        for instance in reservation["Instances"]:
            if(instance["InstanceId"]!=ec2_metadata.instance_id):
                instanceCount+=1
    return instanceCount

def get_num_messages_queue():
    client = boto3.client('sqs', region_name='us-east-1', aws_access_key_id='AKIAQ2HI4V3WNTGN7OXI',
                          aws_secret_access_key='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')
    queueUrl=client.get_queue_url(QueueName='sqs_request')['QueueUrl']
    approximateNumberOfMessages = int(client.get_queue_attributes(QueueUrl=queueUrl,AttributeNames=['ApproximateNumberOfMessages'])['Attributes']['ApproximateNumberOfMessages']) - \
                                  int(client.get_queue_attributes(QueueUrl=queueUrl,AttributeNames=['ApproximateNumberOfMessagesNotVisible'])['Attributes']['ApproximateNumberOfMessagesNotVisible'])
    if(approximateNumberOfMessages<0):
        return 0
    return approximateNumberOfMessages

def scaleInScaleOut():
    while(True):
            msgs_queue=get_num_messages_queue()
            app_instances=get_num_app_instances()
            if(msgs_queue>0 and msgs_queue>app_instances):
                rem_app_instances=19-app_instances
                if(rem_app_instances>0):
                    req_instances=msgs_queue-app_instances
                    # print([req_instances,rem_app_instances])
                    create_instances=min(req_instances,rem_app_instances)
                    for i in range(create_instances):
                        create_ec2_instance(i+1)
            time.sleep(3)

scaleInScaleOut()






