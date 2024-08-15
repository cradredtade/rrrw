const express = require('express');
const { PythonShell } = require('python-shell');
const app = express();
const port = 3000;

app.use(express.static('public'));

app.get('/write', (req, res) => {
    const data = req.query.data;
    let options = {
        scriptPath: './',
        args: [data]
    };

    PythonShell.run('write.py', options)
        .then(results => {
            res.send(results.join('\n'));
        })
        .catch(err => {
            console.error('PythonShell Error:', err);
            res.status(500).send(err.toString());
        });
});

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/public/index.html');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

