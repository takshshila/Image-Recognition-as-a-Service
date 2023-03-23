// Load the AWS SDK for Node.js
const { sqs, requestQueueURL } = require('../instance_base');
const fs = require("fs");
// Set the region

var receiptParams = {
    AttributeNames: [
        "SentTimestamp"
    ],
    MaxNumberOfMessages: 1,
    MessageAttributeNames: [
        "All"
    ],
    QueueUrl: requestQueueURL,
    VisibilityTimeout: 30
};

function receiveSQSMessage() {
    return new Promise(function (resolve, reject) {
        var imageArr = [];
        console.log("entered");
        sqs.receiveMessage(receiptParams, function (err, data) {
            if (err) {
                console.log("Receive Error", err);
                reject(err);
            } else if (data.Messages) {
                data.Messages.forEach(function (message) {
                    // console.log(message);
                    var imageObj = {};
                    var messageBodyObj = JSON.parse(message.Body);
                    if (Object.keys(messageBodyObj).length > 0)
                        var imageName = Object.keys(messageBodyObj)[0];
                    if (imageName && messageBodyObj[imageName]) {
                        var imgTxt = messageBodyObj[imageName];
                        imageObj.name = imageName;
                        imageObj.imgTxt = imgTxt;
                        imageObj.receiptHandle = message.ReceiptHandle;
                        //  console.log(imageObj);

                        //reviving and storing the image     
                        const buffer = Buffer.from(imageObj.imgTxt, "base64");
                        imageObj.path = '/home/ec2-user';
                        fs.writeFileSync(imageObj.path + '/' + imageObj.name, buffer);
                        imageArr.push(imageObj);
                    }
                });


                // running facial-recognition
            }
            resolve(imageArr);
        });
    });
}


exports.receiveMessage = receiveSQSMessage;

