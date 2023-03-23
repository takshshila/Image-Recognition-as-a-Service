var AWS = require('aws-sdk');
const REGION = "us-east-1";
AWS.config.update({region: REGION});

var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

var ec2 = new AWS.EC2({apiVersion: '2016-11-15'});

const PythonShell = require('python-shell').PythonShell;


var requestQueueURL = "https://sqs.us-east-1.amazonaws.com/056322993900/sqs_request";
var responseQueueURL = "https://sqs.us-east-1.amazonaws.com/056322993900/sqs_response";

module.exports = { AWS, sqs, ec2, requestQueueURL, responseQueueURL, PythonShell };