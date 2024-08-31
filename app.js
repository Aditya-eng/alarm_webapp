const awsIot = require('aws-iot-device-sdk');

const device = awsIot.device({
    keyPath: 'certs/private.pem.key',
    certPath: 'certs/device.pem.crt',
    caPath: 'certs/rootCA.pem',
    clientId: 'your-raspberry-pi-client-id',
    host: 'aftnrjs54yfev-ats.iot.eu-north-1.amazonaws.com'
});

device.on('connect', () => {
    console.log('Connected to AWS IoT');
});

//////////////////////////////


const express = require('express');
const app = express();
const port = 3000;

// Middleware to serve static files
app.use(express.static('public'));

// Default route
app.get('/', (req, res) => {
    res.send('Welcome to the Alarm Web App!');
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});

/////////////////////////////
app.use(express.json());

app.post('/set-alarm', (req, res) => {
    const alarmTime = req.body.alarmTime;

    // Publish alarm time to AWS IoT
    device.publish('alarm/set', JSON.stringify({ time: alarmTime }));

    res.json({ message: `Alarm set for ${alarmTime}` });
});