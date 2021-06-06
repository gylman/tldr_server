const dotenv = require('dotenv');
const mongoose = require('mongoose');

process.on('uncaughtException', (err) => {
  console.log('uncaughtException');

  console.log(err.name, err.message);

  process.exit();
});

const app = require('./app');

dotenv.config({ path: './config.env' });

const port = process.env.PORT || 3000;
const server = app.listen(port, () => {
  console.log('data app running');
});

process.on('unhandledRejection', (err) => {
  console.log('uncaughtException');

  console.log(err.name, err.message);

  server.close(() => {
    process.exit();
  });
});
