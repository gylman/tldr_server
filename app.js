const express = require('express');
const morgan = require('morgan');
const helmet = require('helmet');
const hpp = require('hpp');
const path = require('path');
const compression = require('compression');
const sanitizer = require('express-mongo-sanitize');
const xss = require('xss-clean');
const RateLimit = require('express-rate-limit');
const errorHandler = require('./controllers/errorHandlerController');
const dataRoutes = require('./routes/dataRoutes');

const app = express();

app.use(morgan('dev'));
const limiter = RateLimit({
  max: 1000,
  windowMs: 1000 * 60 * 60,
  message: 'Too many requests, please try later'
});

app.use('/api', limiter);
app.use(helmet());
app.use(sanitizer());
app.use(xss());
app.use(hpp());
app.use(compression());
app.use(express.json({ limit: '10kb' }));

app.use((req, res, next) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'Origin, X-Requested-With, Content-Type, Accept,authorization '
  );
  res.setHeader(
    'Access-Control-Allow-Methods',
    'GET, POST, PATCH, DELETE'
  );
  next();
});
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/api/v1/data', dataRoutes);

app.all('*', (req, res, next) => {
  next(new AppError(`can not find ${req.originalUrl} route`, 404));
});

app.use(errorHandler);

module.exports = app;
