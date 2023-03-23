const { sqs, requestQueueURL, PythonShell } = require('../instance_base');

function pushDataToS3(imageObj){
  return new Promise(function(resolve, reject){
    var s3Options = {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: '/home/ec2-user/AppTier/s3',
        args: [JSON.stringify(imageObj)]
    };    
    
    PythonShell.run('dataToS3.py', s3Options, function (err, results) {
        if (err){
            reject(err);
            throw err;
        }
        // Results is an array consisting of messages collected during execution
        console.log('results: %j', results);
        var deleteParams = {
            QueueUrl: requestQueueURL,
            ReceiptHandle: imageObj.receiptHandle
        };
        // store in S3 bucket
        sqs.deleteMessage(deleteParams, function (err, data) {
            if (err) {
                reject(err);
            } else {
                resolve("Results saved to S3 and message deleted");
            }
        });
    });
  });  
}

exports.pushDataToS3 = pushDataToS3;