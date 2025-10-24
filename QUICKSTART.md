# Quick Start Guide

Get your ML backend up and running in 5 minutes!

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.8 or higher)
- Trained ML model files

## Step 1: Install Dependencies

```bash
# Install Node.js packages
npm install

# Install Python packages
pip install -r requirements.txt
```

## Step 2: Export Your Model

1. Open your notebook: `accountingdt_advanced_fe.ipynb`
2. **Restart the kernel** (click Restart button)
3. **Run all cells** (click Run All)
4. Wait for training to complete
5. The last cell will export the model to `E:\NIBM\HDSE\ML\ensenarBE\models\accounting_model.pkl`

## Step 3: Start the Server

```bash
npm start
```

You should see:
```
============================================================
🚀 Ensenar ML Backend is running on port 5000
📊 Environment: development
🔗 API URL: http://localhost:5000
📁 Model Directory: ./models
============================================================
```

## Step 4: Test the API

### Option A: Use the Test Script

```bash
node test/test_api.js
```

### Option B: Use curl

```bash
curl -X POST http://localhost:5000/api/predict/accounting \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

### Option C: Use Postman

1. Create a new POST request
2. URL: `http://localhost:5000/api/predict/accounting`
3. Headers: `Content-Type: application/json`
4. Body: Use the JSON above
5. Click Send

## Expected Response

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

## Troubleshooting

### "Model not found" Error

**Solution:**
1. Go to your notebook
2. Restart kernel
3. Run all cells
4. Make sure the export cell runs successfully
5. Check that `models/accounting_model.pkl` exists

### Python Import Errors

**Solution:**
```bash
pip install pandas numpy scikit-learn imbalanced-learn xgboost
```

### Port Already in Use

**Solution:**
Change the port in `.env`:
```
PORT=3000
```

### Server Won't Start

**Solution:**
1. Check Node.js version: `node --version` (should be v14+)
2. Reinstall dependencies: `npm install`
3. Check for error messages in console

## Next Steps

1. **Export more models**: Repeat Step 2 for other subjects (physics, chemistry, etc.)
2. **Integrate with frontend**: Use the API endpoints in your React/Vue/Angular app
3. **Deploy**: Deploy to Heroku, AWS, or your preferred cloud platform

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Check server health |
| GET | `/api/predict/subjects` | Get available subjects |
| POST | `/api/predict/:subject` | Make prediction |

## Need Help?

- Check the full README.md for detailed documentation
- Review the error messages in the console
- Make sure all required fields are provided in the request

Happy Predicting! 🎓
