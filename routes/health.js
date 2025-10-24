const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

// Health check endpoint
router.get('/', (req, res) => {
  res.json({
    success: true,
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// Check model availability
router.get('/models', (req, res) => {
  try {
    const modelDir = path.join(__dirname, '..', process.env.MODEL_DIR || 'models');
    
    if (!fs.existsSync(modelDir)) {
      return res.json({
        success: true,
        models: [],
        message: 'Models directory does not exist yet'
      });
    }

    const files = fs.readdirSync(modelDir);
    const modelFiles = files.filter(f => f.endsWith('.pkl'));
    
    const models = modelFiles.map(file => {
      const subject = file.replace('_model.pkl', '');
      const filePath = path.join(modelDir, file);
      const stats = fs.statSync(filePath);
      
      return {
        subject: subject,
        file: file,
        size: `${(stats.size / (1024 * 1024)).toFixed(2)} MB`,
        modified: stats.mtime
      };
    });

    res.json({
      success: true,
      count: models.length,
      models: models
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;
