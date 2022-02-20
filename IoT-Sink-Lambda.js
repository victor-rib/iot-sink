const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
    console.log('Message being processed : '+JSON.stringify(event));
    var message = new SensorMessage(event.value, event.voltage, event.temperature, event.deviceid, event.timestamp, event.provider, event.group);
    const params = { TableName : 'sensor-data', Item: message };
    putObjectToS3('sensor-data-backup-001',message.deviceid+'-'+message.timestamp, JSON.stringify(event));
    await docClient.put(params).promise();
    return 200;
};


class SensorMessage {
  constructor(value , voltage, temperature, deviceid, timestamp, provider, group) {
    this.value = value;
    this.voltage = voltage;
    this.temperature = temperature;
    this.deviceid = deviceid;
    this.timestamp = timestamp;
    this.provider = provider;
    this.group = group;
  }
}

function putObjectToS3(bucket, fileName, data){
    var s3 = new AWS.S3();
        var params = {
            Bucket : bucket,
            Key : fileName,
            Body : data
        }
        s3.putObject(params, function(err, data) {
          if (err) console.log(err, err.stack); // an error occurred
          else     console.log(data);           // successful response
        });
}