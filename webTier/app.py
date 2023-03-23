from flask import Flask, request, jsonify
app = Flask(__name__)
import json
# import sys
import boto3
import base64
import io
import ast

i=0
dic={}
sqs_client = boto3.client('sqs', region_name='us-east-1', aws_access_key_id='AKIAQ2HI4V3WNTGN7OXI',
                          aws_secret_access_key='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')

@app.route("/", methods=['GET'])
def health_check():
    return "Health Ok!"

@app.route("/receive_image", methods=['POST'])
def receive_image():
    global i
    global dic
    print(i)
    print(dic)
    i+=1
    key=list(request.files.keys())[0]
    file = request.files[key]
    img_as_byte = base64.b64encode(file.read())
    img_as_string = img_as_byte.decode('UTF-8')

    response=send2Queue(key,img_as_string)
    if response['ResponseMetadata']['HTTPStatusCode']!=200:
        return "Error while putting msg in queue"
    # else:
    #     return response
    result=receive_response(key)
    if i==0:
        dic={}
        print(dic)
    # print(result)
    return result

def send2Queue(key,value):
    # msg_attributes = {
    #     key: {
    #         'DataType': 'String',
    #         'StringValue': value
    #     }
    # }
    message = {key: value}
    message = json.dumps(message)
    # msg_body = 'Sending images to App Tier'
    response = sqs_client.send_message(QueueUrl='https://sqs.us-east-1.amazonaws.com/056322993900/sqs_request',
                            MessageBody=message)

    return response

@app.route("/receive_response", methods=['GET'])
def receive_response(key):
    global dic
    global i
    while(True):
        if key in dic:
            val=dic[key]
            # del dic[key]
            i-=1
            return val
        else:
            response = sqs_client.receive_message(
                QueueUrl='https://sqs.us-east-1.amazonaws.com/056322993900/sqs_response',
                # AttributeNames=[
                #     'All'
                #     # | 'Policy' | 'VisibilityTimeout' | 'MaximumMessageSize' | 'MessageRetentionPeriod' | 'ApproximateNumberOfMessages' | 'ApproximateNumberOfMessagesNotVisible' | 'CreatedTimestamp' | 'LastModifiedTimestamp' | 'QueueArn' | 'ApproximateNumberOfMessagesDelayed' | 'DelaySeconds' | 'ReceiveMessageWaitTimeSeconds' | 'RedrivePolicy' | 'FifoQueue' | 'ContentBasedDeduplication' | 'KmsMasterKeyId' | 'KmsDataKeyReusePeriodSeconds' | 'DeduplicationScope' | 'FifoThroughputLimit' | 'RedriveAllowPolicy' | 'SqsManagedSseEnabled',
                # ],
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=10,
                VisibilityTimeout=5,
                WaitTimeSeconds=0,
                # ReceiveRequestAttemptId='string'
            )
            if (list(response.keys())[0] == 'Messages'):
                print(response['Messages'][0])
                for message in response['Messages']:
                    tmp = ast.literal_eval(message['Body'])
                    localkey = list(tmp.keys())[0]
                    val = tmp[localkey]
                    dic[localkey] = val
                    sqs_client.delete_message(
                        QueueUrl='https://sqs.us-east-1.amazonaws.com/056322993900/sqs_response',
                        ReceiptHandle=message['ReceiptHandle']
                    )
    # print(response)
    # return response

            # receive_response(key)
        # return response
if __name__ == "__main__":
	app.run(host = '0.0.0.0')
    # host = '0.0.0.0'
    # debug = True
