const { AWS, ec2 } = require('../instance_base');

var instanceMetaData = new AWS.MetadataService();

function terminateEC2Instance() {
  return new Promise(function (resolve, reject) {
    instanceMetaData.request("/latest/meta-data/instance-id", function (err, data) {
      var instanceId = data;
      var params = {
        InstanceIds: [
          instanceId
        ]
      };
      ec2.terminateInstances(params, function (err, data) {
        if (err) {
          reject(err); // an error occurred
        }
        else {
          resolve(data);
        }       // successful response
      });
    });
  });
}

exports.terminateInstance = terminateEC2Instance;