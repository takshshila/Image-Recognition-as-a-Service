const { getQueueAttributes } = require('./AppTier/sqs/sqs_queueAttributes');
const { receiveMessage } = require('./AppTier/sqs/sqs_receivemessage');
const { runFaceRecognition } = require('./AppTier/face_recognition/image_face_recognition');
const { sendMessage } = require('./AppTier/sqs/sqs_sendmessage');
const { pushDataToS3 } = require('./AppTier/s3/pushDataToS3');
const { terminateInstance } = require('./AppTier/ec2/ec2_terminateInstance');

async function processRequests() {
    var messagePresentInQueue = await getQueueAttributes();
    do {
        var imageArr = await receiveMessage();
        //  console.log(imageArr);
        for (var i = 0; i < imageArr.length; i++) {
            var imageObj = imageArr[i];
            await runFaceRecognition(imageObj);
            var messageSentConfirmation = await sendMessage(imageObj);
            console.log(messageSentConfirmation);
            var resultConfirmationFromS3 = await pushDataToS3(imageObj);
            console.log(resultConfirmationFromS3);
        }
        messagePresentInQueue = await getQueueAttributes();
    } while (messagePresentInQueue > 0);
    console.log("finished manageInstance");
}

function sleep(secs) {
    return new Promise(function (resolve, reject) {
        setTimeout(function () {
            console.log('after sleep for ' + secs + ' sec.s');
            resolve();
        }, secs * 1000);
    });
}

//template

async function manageInstance() {

    while (true) {
        await processRequests();
        var delayMessage = await sleep(10);
        var messagePresentInQueue = await getQueueAttributes();
        if (!messagePresentInQueue) {
            var instanceTerminationResponse = await terminateInstance();
            console.log(instanceTerminationResponse);
            break;
        }
    }
}

manageInstance().then(function () {
    console.log("completed execution");
});





