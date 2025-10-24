# Deep Learning Grade A Prediction API

## 🧠 Overview

This endpoint uses a **5-layer deep neural network** to predict whether a student will achieve Grade A and provides **personalized recommendations** for improvement.

## 📍 Endpoint

**POST** `http://localhost:5000/api/deeplearning`

## 🎯 What It Predicts

- **Grade A Probability**: Likelihood (0-100%) of achieving Grade A
- **Binary Prediction**: "A" or "Not A"
- **Status Assessment**: EXCELLENT, GOOD, NEEDS IMPROVEMENT, or CRITICAL
- **Personalized Recommendations**: Top 5 actionable improvements with impact analysis

## 📥 Request Format

### Headers
```
Content-Type: application/json
```

### Body (JSON)
```json
{
  "Stream": "Science",
  "Subject": "Physics",
  "Gender": "Male",
  "Medium": "English",
  "Social Media Platform": "Instagram",
  "Daily Usage": "3-4 hours",
  "Notification Status": "Always kept on",
  "Distraction Level": 5,
  "Sleep Hours": "5-6 hours",
  "Timing Behavior": "Often exceeded the time limit",
  "Study Hours": "2-4 hours",
  "Consistency": 2,
  "Recent Past Paper": "Below 40%",
  "Past Papers Count": "0-10 papers",
  "Avg Five Papers": "Below 40%"
}
```

## 📤 Response Format

### Success Response (200 OK)
```json
{
  "success": true,
  "prediction": {
    "predicted_grade": "Not A",
    "grade_a_probability": 0.28,
    "confidence": 0.72,
    "status": "CRITICAL",
    "recommendations": [
      {
        "feature": "Past Papers Count",
        "current": "0-10 papers",
        "suggested": "More than 40 papers",
        "reason": "Practice more past papers to boost confidence",
        "improvement": "+40.2%",
        "new_probability": "68.2%"
      },
      {
        "feature": "Study Hours",
        "current": "2-4 hours",
        "suggested": "More than 8 hours",
        "reason": "Increase study hours for better preparation",
        "improvement": "+24.5%",
        "new_probability": "52.5%"
      },
      {
        "feature": "Daily Usage",
        "current": "3-4 hours",
        "suggested": "1-2 hours",
        "reason": "Reduce social media to free up study time",
        "improvement": "+13.8%",
        "new_probability": "41.8%"
      },
      {
        "feature": "Sleep Hours",
        "current": "5-6 hours",
        "suggested": "7-8 hours",
        "reason": "Better sleep improves focus and memory",
        "improvement": "+8.5%",
        "new_probability": "36.5%"
      },
      {
        "feature": "Consistency",
        "current": "2",
        "suggested": "5",
        "reason": "Maintain consistent study habits",
        "improvement": "+6.2%",
        "new_probability": "34.2%"
      }
    ],
    "model_type": "deep_learning",
    "architecture": "5-layer neural network (128-64-32-16-1)"
  }
}
```

### Error Response (400/500)
```json
{
  "success": false,
  "error": "Missing required fields: Study Hours, Consistency"
}
```

## 🔧 Required Fields

All 15 fields are required:

| Field | Type | Valid Values |
|-------|------|--------------|
| Stream | String | Commerce, Science, Arts, Technology, Biology, Mathematics |
| Subject | String | Physics, Chemistry, Biology, ICT, Accounting, Economics, etc. |
| Gender | String | Male, Female |
| Medium | String | English, Sinhala, Tamil |
| Social Media Platform | String | Facebook, Instagram, TikTok, YouTube, WhatsApp, Twitter, LinkedIn, etc. |
| Daily Usage | String | Less than 1 hour, 1-2 hours, 2-3 hours, 3-4 hours, More than 4 hours |
| Notification Status | String | Always turned off, Sometimes turned off, Usually kept on, Always kept on |
| Distraction Level | Number | 1-10 |
| Sleep Hours | String | Less than 5 hours, 5-6 hours, 6-7 hours, 7-8 hours, More than 8 hours |
| Timing Behavior | String | Always completed within the allocated time limit, Usually completed within the time limit, Sometimes exceeded the time limit, Often exceeded the time limit, Always took longer than the allocated time |
| Study Hours | String | Less than 2 hours, 2-4 hours, 4-6 hours, 6-8 hours, More than 8 hours |
| Consistency | Number | 1-5 |
| Recent Past Paper | String | Below 40%, 40-55%, 55-70%, 70-85%, Above 85% |
| Past Papers Count | String | 0-10 papers, 11-20 papers, 21-30 papers, 31-40 papers, More than 40 papers |
| Avg Five Papers | String | Below 40%, 40-55%, 55-70%, 70-85%, Above 85% |

## 📊 Status Levels

| Status | Probability Range | Meaning |
|--------|------------------|---------|
| EXCELLENT | 80-100% | On track for Grade A |
| GOOD | 60-79% | Strong chance for Grade A |
| NEEDS IMPROVEMENT | 40-59% | Significant effort needed |
| CRITICAL | 0-39% | Major changes required |

## 🧪 Testing in Postman

### Example 1: Low Performing Student
```bash
POST http://localhost:5000/api/deeplearning
Content-Type: application/json

{
  "Stream": "Science",
  "Subject": "Physics",
  "Gender": "Male",
  "Medium": "English",
  "Social Media Platform": "Instagram",
  "Daily Usage": "3-4 hours",
  "Notification Status": "Always kept on",
  "Distraction Level": 5,
  "Sleep Hours": "5-6 hours",
  "Timing Behavior": "Often exceeded the time limit",
  "Study Hours": "2-4 hours",
  "Consistency": 2,
  "Recent Past Paper": "Below 40%",
  "Past Papers Count": "0-10 papers",
  "Avg Five Papers": "Below 40%"
}
```

### Example 2: High Performing Student
```bash
POST http://localhost:5000/api/deeplearning
Content-Type: application/json

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
  "Recent Past Paper": "Above 85%",
  "Past Papers Count": "More than 40 papers",
  "Avg Five Papers": "Above 85%"
}
```

## 🚀 How to Use Recommendations

The API returns personalized recommendations sorted by impact. Each recommendation shows:

1. **Feature**: What to change
2. **Current**: Your current value
3. **Suggested**: Recommended value
4. **Reason**: Why this change helps
5. **Improvement**: Percentage increase in Grade A probability
6. **New Probability**: Expected probability after this change

### Implementation Strategy

1. **Focus on high-impact recommendations first** (largest improvement %)
2. **Make changes gradually** - don't overwhelm yourself
3. **Track progress weekly**
4. **Combine multiple recommendations** for maximum effect

## 🔬 Model Architecture

- **Type**: Deep Neural Network (DNN)
- **Layers**: 5 layers (128 → 64 → 32 → 16 → 1 neurons)
- **Features**: Batch Normalization, Dropout (0.3, 0.3, 0.2, 0.2)
- **Activation**: ReLU (hidden layers), Sigmoid (output)
- **Training**: SMOTE for class balance, Early Stopping, Learning Rate Reduction
- **Accuracy**: ~95%+ on test set
- **AUC Score**: ~0.98

## 💡 Key Differences from Traditional ML Models

| Feature | Traditional ML | Deep Learning |
|---------|---------------|---------------|
| Architecture | Single layer | 5 hidden layers |
| Parameters | Hundreds | 11,000+ |
| Feature Learning | Manual | Automatic |
| Recommendations | No | Yes (personalized) |
| Confidence | Basic | Advanced probability |

## ⚠️ Important Notes

1. **Server must be running**: `npm start` before testing
2. **Model files required**: `grade_a_predictor.h5` and `preprocessing_objects.pkl` must be in `models/` folder
3. **TensorFlow installed**: Python environment needs TensorFlow
4. **All fields required**: Missing any field will result in error
5. **Case-sensitive values**: Use exact strings as shown in valid values

## 🐛 Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "Model file not found" | Missing .h5 file | Copy `grade_a_predictor.h5` to `models/` |
| "Preprocessing file not found" | Missing .pkl file | Copy `preprocessing_objects.pkl` to `models/` |
| "No module named 'tensorflow'" | TensorFlow not installed | Run `pip install tensorflow` |
| "Missing required fields" | Incomplete request body | Include all 15 required fields |
| 500 error | Server/model error | Check server logs for details |

## 📞 Support

For issues or questions about the deep learning endpoint, check:
- Server logs for detailed error messages
- Model files are in correct location
- All dependencies are installed
- Request body matches required format
