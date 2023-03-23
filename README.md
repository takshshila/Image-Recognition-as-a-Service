# Cloud-Computing-Proj1
# Image Recognition as a Service

Image recognition is a go-to functionality in this digital era to mark attendance, authorization, etc. With the increase in the number of users, a normal system will not work efficiently due to various reasons: dynamically run out of memory, computation powers, high workload, etc. We are building an Infrastructure as a Service on Amazon web service to provide consistent service with auto-scalable functionality. Every request will be guaranteed served with Amazon Simple Queue Service(SQS).

![alt text](IAAS.png)


## Architecture Description
### Web Tier 
The Web Tier is the starting component of this service with the responsibility of constantly listening to user requests and sending messages onto the queue. Once outputs are populated in the response queue the web tier collects them, matches them with corresponding requests and displays the results to the user.

### SQS Queues
There are two queues in our application. The SQS request queue sends the image for face-recognition from the web tier to the app tier. The SQS response queue sends the image face-recognition result back to the web tier.

### App Tier 
The app-tier is responsible for picking up the message from the SQS request queue, performing the face-recognition task on the image and sending the results back to the SQS response queue after storing the image and its face-recognition result in the S3 buckets.
###  S3 
Amazon Simple Storage Service (S3) stores huge amounts of data (even in terabytes) and dynamically grows as per the requirement. We are using S3 to store images and image output. Similar to Figure 1, the App Tier provides an image and its output for storage. Within the Apptier instance, we are creating two s3 buckets: input(ccpimageinput) and output(ccpimageoutput). Input bucket is used to store images with the image name as the key and output bucket for storing image results with image name (without .jpg extension) as key. 


<!-- ### AWS Credentials
    Access key ID: AKIAQ2HI4V3WNTGN7OXI
    Secret access key: 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
    Region: US East (N. Virginia) us-east-1

### Web Tier URL
    - ec2-54-236-188-51.compute-1.amazonaws.com
    - http://54.236.188.51:5000/receive_image
    
### SQS Names
    Request Queue:
        - Name: sqs_request
        - Url: https://sqs.us-east-1.amazonaws.com/056322993900/sqs_request
    Response Queue:
        - Name: sqs_response
        - Url: https://sqs.us-east-1.amazonaws.com/056322993900/sqs_response

### S3 Bucket Names
    -Input Bucket: ccpimageinput
    -Output Bucket: ccpimageoutput


### Team:57
    Mani Sai Tejaswy Valluri (mvallur2@asu.edu)
    Pavan Mallina (pmallina@asu.edu)
    Takshshila Rawat (trawat2@asu.edu) -->

