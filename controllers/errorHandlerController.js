const AppError = require("./../utils/appError");

const handleCastError = (err) => {
  const message = `Invalid ${err.path}: ${err.value}`;
  return new AppError(message, 400);
};

const handleDublicatedFieldErrors = (err) => {
  const value = err.errmsg.match(/"([^"]*)"/)[0];
  const message = `dublicated value ${value}, Please us another value`;

  return new AppError(message, 400);
};
const handleValidationErrorDB = (err) => {
  const errors = Object.values(err.errors).map((error) => error.message);
  const message = `invalid input data${errors.join(". ")}`;

  return new AppError(message, 400);
};
const handleJsonWebTokenError = (err) =>
  new AppError("invalid credentials, please log in again", 401);
const handleTokenExpiredError = (err) =>
  new AppError("expired token credentials, please log in again", 401);
const sendErrorProd = (err, req, res) => {
  console.log("====================================");
  console.log(err);
  console.log("====================================");
  if (err.isOperational) {
    res.status(err.statusCode).json({
      status: err.status,
      message: err.message,
    });
  } else {
    res.status(500).json({
      status: "error",
      message: "something went wrong",
    });
  }
};

const sendErrorDev = (err, req, res) => {
  res.status(err.statusCode).json({
    status: err.status,
    message: err.message,
    error: err,
    stack: err.stack,
  });
};

module.exports = (err, req, res, next) => {
  err.statusCode = err.statusCode || 500;
  err.status = err.status || "error";

  if (process.env.NODE_ENV.trim() === "production") {
    let error = { ...err };
    error.message = err.message;
    if (error.name === "CastError") error = handleCastError(error);
    if (error.name === "ValidationError")
      error = handleValidationErrorDB(error);
    if (error.name === "JsonWebTokenError")
      error = handleJsonWebTokenError(error);
    if (error.name === "TokenExpiredError")
      error = handleTokenExpiredError(error);
    if (error.code === 11000) error = handleDublicatedFieldErrors(error);

    sendErrorProd(error, req, res);
  } else {
    sendErrorDev(err, req, res);
  }
};
