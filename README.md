# Ensenar ML Backend

Express.js backend for hosting machine learning grade prediction models.

## Features

- ✅ RESTful API for grade predictions
- ✅ Support for multiple subjects (Accounting, Physics, Chemistry, etc.)
- ✅ Advanced feature engineering
- ✅ Python integration for ML predictions
- ✅ CORS enabled for frontend integration
- ✅ Error handling and validation

## Project Structure

```
ensenarBE/
├── server.js              # Main Express server
├── routes/
│   ├── health.js         # Health check endpoints
│   └── prediction.js     # Prediction endpoints
├── python/
│   └── predict.py        # Python prediction script
├── models/               # ML model files (.pkl)
├── test/                 # Test scripts
├── package.json          # Node dependencies
└── requirements.txt      # Python dependencies
```

## Installation

### 1. Install Node.js Dependencies

```bash
npm install
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### 1. Train and Export Models

Run your Jupyter notebooks to train models and export them:
- The export cell in each notebook will save models to `./models/`
- Models must be named as `{subject}_model.pkl`

### 2. Start the Server

```bash
npm start
```

For development with auto-reload:
```bash
npm run dev
```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check

**GET** `/api/health`

Returns server health status.

**Response:**
```json
{
  "success": true,
  "status": "healthy",
  "timestamp": "2025-10-24T10:30:00.000Z",
  "uptime": 123.456
}
```

### Get Available Subjects

**GET** `/api/predict/subjects`

Returns list of available subjects and models.

**Response:**
```json
{
  "success": true,
  "subjects": ["accounting", "physics", "chemistry", ...],
  "availableModels": ["accounting", "physics"],
  "message": "2 model(s) available"
}
```

### Make Prediction

**POST** `/api/predict/:subject`

Makes a grade prediction for the specified subject.

**Parameters:**
- `subject` (path): Subject name (e.g., "accounting", "physics")

**Request Body:**
```json
{
  "Stream": "Commerce",
  "Subject": "Accounting",
  "Gender": "Female",
  "Medium": "English",
  "Social Media Platform": "Facebook",
  "Daily Usage": "1-2 hours",
  "Notification Status": "Always turned off",
  "Distraction Level": 1,
  "Sleep Hours": "7-8 hours",
  "Timing Behavior": "Always completed within the allocated time limit",
  "Study Hours": "More than 8 hours",
  "Consistency": 5,
  "Recent Past Paper": "70-85%",
  "Past Papers Count": "More than 40 papers",
  "Avg Five Papers": "Above 85%"
}
```

**Response:**
```json
{
  "success": true,
  "subject": "accounting",
  "prediction": {
    "predicted_grade": "A",
    "confidence": 0.92,
    "probabilities": {
      "A": 0.92,
      "B": 0.05,
      "C": 0.02,
      "S": 0.01
    },
    "model_accuracy": 0.95,
    "features_used": 45
  }
}
```

## Required Input Fields

All prediction requests must include these fields:

- **Stream**: "Commerce", "Science", "Arts", etc.
- **Subject**: "Accounting", "Physics", etc.
- **Gender**: "Male", "Female"
- **Medium**: "English", "Sinhala", "Tamil"
- **Social Media Platform**: "Facebook", "Instagram", "TikTok", etc.
- **Daily Usage**: "Less than 1 hour", "1-2 hours", "2-3 hours", "3-4 hours", "More than 4 hours"
- **Notification Status**: "Always turned off", "Sometimes turned off", "Usually kept on", "Always kept on"
- **Distraction Level**: 1-5 (integer)
- **Sleep Hours**: "Less than 5 hours", "5-6 hours", "6-7 hours", "7-8 hours", "More than 8 hours"
- **Timing Behavior**: "Often exceeded the time limit", "Sometimes exceeded the time limit", "Usually completed within the time limit", "Always completed within the allocated time limit", "Always took longer than the allocated time"
- **Study Hours**: "Less than 2 hours", "2-4 hours", "4-6 hours", "6-8 hours", "More than 8 hours"
- **Consistency**: 1-5 (integer)
- **Recent Past Paper**: "Below 40%", "40-55%", "55-70%", "70-85%", "Above 85%"
- **Past Papers Count**: "0-10 papers", "11-20 papers", "21-30 papers", "31-40 papers", "More than 40 papers"
- **Avg Five Papers**: "Below 40%", "40-55%", "55-70%", "70-85%", "Above 85%"

## Testing

Test the API with the provided test script:

```bash
node test/test_api.js
```

Or use curl:

```bash
curl -X POST http://localhost:5000/api/predict/accounting \
  -H "Content-Type: application/json" \
  -d @test_data.json
```

## Frontend Integration

### JavaScript/React Example

```javascript
async function predictGrade(subject, inputData) {
  try {
    const response = await fetch(`http://localhost:5000/api/predict/${subject}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(inputData)
    });
    
    const result = await response.json();
    
    if (result.success) {
      console.log('Predicted Grade:', result.prediction.predicted_grade);
      console.log('Confidence:', result.prediction.confidence);
    }
  } catch (error) {
    console.error('Prediction error:', error);
  }
}
```

## Environment Variables

Create a `.env` file:

```env
PORT=5000
NODE_ENV=development
PYTHON_PATH=python
MODEL_DIR=./models
```

## Troubleshooting

### Model Not Found Error

If you get "Model not found" error:
1. Make sure you've run the notebook and executed the export cell
2. Check that the model file exists in `./models/{subject}_model.pkl`
3. Verify the subject name matches the filename

### Python Import Errors

If you get Python import errors:
1. Install required packages: `pip install -r requirements.txt`
2. Verify Python path in `.env` file
3. Make sure you're using Python 3.8+

### KeyError in Prediction

If you get KeyError about missing columns:
1. Make sure the notebook has been trained with the latest code
2. Restart kernel and run all cells in the notebook
3. Re-export the model

## License

ISC
