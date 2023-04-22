const express = require('express')
const cors = require('cors');

const app = express()

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));


const apiRouter = require('./build/routes/api');
app.use('/api', apiRouter);
app.use(express.static('./dist'));

app.listen(process.env.PORT, function() {});