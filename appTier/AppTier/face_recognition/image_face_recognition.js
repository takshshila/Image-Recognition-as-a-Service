const { PythonShell } = require('../instance_base');

function runFaceRecognition(imageObj){
    return new Promise(function(resolve, reject){

        var options = {
            mode: 'text',
            pythonOptions: ['-u'],
            scriptPath: '/home/ec2-user',
            args: [imageObj.path + '/' + imageObj.name]
        };
        
        PythonShell.run('face_recognition.py', options, function (err, results) {
            if (err){
                reject(err);
                throw err;
            }
            // Results is an array consisting of messages collected during execution
            console.log('results: %j', results);
            imageObj.result = results[0];
            resolve(imageObj);
        });

    });
}

exports.runFaceRecognition = runFaceRecognition;