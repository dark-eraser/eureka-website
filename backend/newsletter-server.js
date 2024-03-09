require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const { body, validationResult } = require('express-validator');
const winston = require('winston');

// Logger configuration
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  defaultMeta: { service: 'user-service' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ],
});

// Connect to MongoDB
mongoose.connect(process.env.MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => logger.info('Connected to MongoDB'))
  .catch(err => logger.error('Could not connect to MongoDB...', err));

// Define a schema for the email
const emailSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    index: true // Adding an index for better performance
  }
});

const Email = mongoose.model('Email', emailSchema);

const app = express();

app.use(bodyParser.urlencoded({ extended: true }));

// Newsletter subscription route
app.post('/subscribe', 
  body('email').isEmail().withMessage('Enter a valid email address'),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(422).json({ errors: errors.array() });
    }

    let email = new Email({ email: req.body.email });
    email.save()
    .then(() => res.send('Thank you for subscribing!'))
    .catch(err => {
      logger.error('Error: Could not add to the newsletter list.', err);
      console.error(err); // This line will print the error details to the console
      res.status(500).send('Error: Could not add to the newsletter list.');
    });
  
});

const port = process.env.PORT || 3000;
app.listen(port, () => logger.info(`Listening on port ${port}...`));
