const express = require('express');
const router = express.Router();
const { PythonShell } = require('python-shell');
const path = require('path');
const fs = require('fs');

// Available subjects
const AVAILABLE_SUBJECTS = [
  'accounting', 'physics', 'chemistry', 'biology',
  'ict', 'economics', 'agriculture', 'combinedmaths',
  'bstatistics', 'bstudies'
];

// Get available subjects
router.get('/subjects', (req, res) => {
  const modelDir = path.join(__dirname, '..', process.env.MODEL_DIR || 'models');
  
  let availableSubjects = [];
  if (fs.existsSync(modelDir)) {
    const files = fs.readdirSync(modelDir);
    availableSubjects = files
      .filter(f => f.endsWith('.pkl'))
      .map(f => f.replace('_model.pkl', ''));
  }

  res.json({
    success: true,
    subjects: AVAILABLE_SUBJECTS,
    availableModels: availableSubjects,
    message: availableSubjects.length === 0 ? 
      'No models found. Please train and export models first.' : 
      `${availableSubjects.length} model(s) available`
  });
});

// Prediction endpoint
router.post('/:subject', async (req, res) => {
  try {
    const subject = req.params.subject.toLowerCase();
    const inputData = req.body;

    // Validate subject
    if (!AVAILABLE_SUBJECTS.includes(subject)) {
      return res.status(400).json({
        success: false,
        error: `Invalid subject. Available subjects: ${AVAILABLE_SUBJECTS.join(', ')}`
      });
    }

    // Check if model exists
    const modelPath = path.join(__dirname, '..', 'models', `${subject}_model.pkl`);
    if (!fs.existsSync(modelPath)) {
      return res.status(404).json({
        success: false,
        error: `Model for ${subject} not found. Please train and export the model first.`,
        modelPath: modelPath
      });
    }

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

    // Prepare Python shell options
    const options = {
      mode: 'json',
      pythonPath: process.env.PYTHON_PATH || 'python',
      pythonOptions: ['-u'],
      scriptPath: path.join(__dirname, '..', 'python'),
      args: [
        '--subject', subject,
        '--input', JSON.stringify(inputData)
      ]
    };

    // Run prediction
    const results = await PythonShell.run('predict.py', options);
    const prediction = results[0];

    if (prediction.error) {
      return res.status(500).json({
        success: false,
        error: prediction.error
      });
    }

    res.json({
      success: true,
      subject: subject,
      prediction: prediction
    });

  } catch (error) {
    console.error('Prediction error:', error);
    res.status(500).json({
      success: false,
      error: error.message || 'Prediction failed'
    });
  }
});

module.exports = router;
