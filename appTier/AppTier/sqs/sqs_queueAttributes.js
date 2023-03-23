const { sqs, requestQueueURL } = require('../instance_base');

function getQueueParams() {
    var queueParams = {
        QueueUrl: requestQueueURL, /* required */
        AttributeNames: [
            "All"
            /* more items */
        ]
    };

    return new Promise(function (resolve, reject) {
        var queueAttributes = {};
        sqs.getQueueAttributes(queueParams, function (err, data) {
            if (err) {
                console.log(err, err.stack); // an error occurred
                reject(err);
            }
            else {
                queueAttributes = data;
                console.log(queueAttributes);
                var messagePendingInQueue = (parseInt(queueAttributes.Attributes.ApproximateNumberOfMessages) > 0 && parseInt(queueAttributes.Attributes.ApproximateNumberOfMessagesNotVisible) < parseInt(queueAttributes.Attributes.ApproximateNumberOfMessages));
                resolve(messagePendingInQueue);
            }
        });
    });
}

exports.getQueueAttributes = getQueueParams;