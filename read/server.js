const express = require('express');
const { exec } = require('child_process');
const path = require('path');  // 引入 path 模块
const app = express();
const port = 3000;

// 根路径路由，发送 index.html 文件
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));  // 返回 index.html 文件
});

// 处理 /rfid 请求，运行 read.py 并返回结果
app.get('/rfid', (req, res) => {
    exec('python3 read.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send('Error reading RFID');
        }
        res.send(stdout);  // 将 RFID 数据发送回客户端
    });
});

// 监听端口
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});

