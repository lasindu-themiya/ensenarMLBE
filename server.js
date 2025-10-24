const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
require('dotenv').config();

const predictionRoutes = require('./routes/prediction');
const healthRoutes = require('./routes/health');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Routes
app.use('/api/health', healthRoutes);
app.use('/api/predict', predictionRoutes);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Ensenar ML Backend API',
    version: '1.0.0',
    endpoints: {
      health: '/api/health',
      predict: '/api/predict/:subject',
      subjects: '/api/predict/subjects'
    }
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: 'Endpoint not found'
  });
});

// Error handler
app.use((err, req, res, next) => {
  console.error('Error:', err.stack);
  res.status(500).json({
    success: false,
    error: err.message || 'Internal server error'
  });
});

// Start server
app.listen(PORT, () => {
  console.log('='.repeat(60));
  console.log(`🚀 Ensenar ML Backend is running on port ${PORT}`);
  console.log(`📊 Environment: ${process.env.NODE_ENV || 'development'}`);
  console.log(`🔗 API URL: http://localhost:${PORT}`);
  console.log(`📁 Model Directory: ${process.env.MODEL_DIR || './models'}`);
  console.log('='.repeat(60));
  console.log('\n📋 Available Endpoints:');
  console.log(`   GET  http://localhost:${PORT}/api/health`);
  console.log(`   GET  http://localhost:${PORT}/api/predict/subjects`);
  console.log(`   POST http://localhost:${PORT}/api/predict/:subject`);
  console.log('='.repeat(60));
});
