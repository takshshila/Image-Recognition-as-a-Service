const { sqs, requestQueueURL, responseQueueURL } = require('../instance_base');

function sendSQSMessage(imageObj) {
  return new Promise(function (resolve, reject) {
    var responseObj = {};
    responseObj[imageObj.name] = imageObj.result;

    var params = {
      MessageBody: JSON.stringify(responseObj),
      QueueUrl: responseQueueURL
    };

    sqs.sendMessage(params, function (err, data) {
      if (err) {
        reject(err);
      } else {
        resolve("Message sent successfully: " + data.MessageId);
      }
    });
  });
}


exports.sendMessage = sendSQSMessage;




