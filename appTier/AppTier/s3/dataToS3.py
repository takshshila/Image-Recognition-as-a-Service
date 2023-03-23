import boto3
#import glob
import sys
import json



def bucketCreation(bucketName):
    response = s3_client.create_bucket(Bucket=bucketName)
    return response

def checkingExistingBuckets():
    s3_cl = boto3.resource('s3', region_name=region)
    list(s3_cl.buckets.all())
    buckets = []
    for bucket in s3_cl.buckets.all():
        buckets.append(bucket.name)
    return buckets

#checkingExistingBuckets()

def storingDataToBucket(data, in_bucket, out_bucket, extraArgs=None):
    '''
    fileName: name of the file
    bucket: bucketname
    objectname:  s3 file name(Key)
    extraArgs: custom arguments
    '''
    existBucket=checkingExistingBuckets()
    if in_bucket not in existBucket:
        bucketCreation(in_bucket)

    if out_bucket not in existBucket:
        bucketCreation(out_bucket)


    response_in = s3_client.upload_file(data['path'] + '/' + data['name'], in_bucket, data['name'], extraArgs)
    print(response_in)


    outputFileName = data['name'].split('.')[0]
    with open(outputFileName, 'w') as f:
        f.write(data['result'])

    response_out = s3_client.upload_file(outputFileName, out_bucket, outputFileName, extraArgs)
    #response_out=s3_client.put_object(Body=data['result'], Bucket=out_bucket, Key=data['name'])
    print(response_out)

def retriveingOutputDataFromBucket(bucket, key):
    s3_client_resource = boto3.resource('s3')
    obj = s3_client_resource.Object(bucket, key)
    return obj.get()['Body'].read().decode('utf-8')


if __name__ == "__main__":
    region = "us-east-1"
    #aws_id = 'AKIASDCJETV5ZJHXDWLT'
    #aws_key = 'ro8whlB6DDKt7ihFvKAD7eoDbt1IzAKUwTcySmD4'
    s3_client = boto3.client("s3", region_name=region)
    s3_rsr = boto3.resource("s3", region_name=region)
    inputBucket = 'ccpimageinput'
    outputBucket = 'ccpimageoutput'

    #print(sys.argv)
    data = json.loads(sys.argv[1])
    #print(data)
    args = {'ACL': 'public-read'}
    storingDataToBucket(data, inputBucket, outputBucket, args)
    #print(data)


    #data = {"name": 'instance_lifecycle.png',"path": 'data',"result": 'Lifecycle'}