const express = require('express');
const router = express.Router();
const { PythonShell } = require('python-shell');
const path = require('path');
const fs = require('fs');

// Deep Learning Grade A Prediction endpoint
router.post('/', async (req, res) => {
  try {
    const inputData = req.body;

    // Validate required fields
    const requiredFields = [
      'Stream', 'Subject', 'Gender', 'Medium', 'Social Media Platform',
      'Daily Usage', 'Notification Status', 'Distraction Level',
      'Sleep Hours', 'Timing Behavior', 'Study Hours', 'Consistency',
      'Recent Past Paper', 'Past Papers Count', 'Avg Five Papers'
    ];

    const missingFields = requiredFields.filter(field => !(field in inputData));
    if (missingFields.length > 0) {
      return res.status(400).json({
        success: false,
        error: `Missing required fields: ${missingFields.join(', ')}`
      });
    }

    // Check if model exists
    const modelPath = path.join(__dirname, '..', 'models', 'grade_a_predictor.h5');
    if (!fs.existsSync(modelPath)) {
      return res.status(404).json({
        success: false,
        error: 'Deep learning model not found. Please ensure grade_a_predictor.h5 is in the models folder.',
        modelPath: modelPath
      });
    }

    // Prepare Python shell options
    const options = {
      mode: 'json',
      pythonPath: process.env.PYTHON_PATH || 'python',
      pythonOptions: ['-u'],
      scriptPath: path.join(__dirname, '..', 'python'),
      args: [
        '--input', JSON.stringify(inputData)
      ]
    };

    // Run prediction
    const results = await PythonShell.run('predict_dl.py', options);
    const prediction = results[0];

    if (prediction.error) {
      return res.status(500).json({
        success: false,
        error: prediction.error
      });
    }

    res.json({
      success: true,
      prediction: prediction
    });

  } catch (error) {
    console.error('Deep learning prediction error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Deep learning prediction failed'
    });
  }
});

module.exports = router;
