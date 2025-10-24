import sys
import json
import pickle
import pandas as pd
import numpy as np
import argparse
from pathlib import Path

def load_model(subject):
    """Load the trained model and all components"""
    try:
        model_path = Path(__file__).parent.parent / 'models' / f'{subject}_model.pkl'
        
        if not model_path.exists():
            return None, f"Model file not found: {model_path}"
        
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        return model_data, None
    except Exception as e:
        return None, f"Error loading model: {str(e)}"

def engineer_features(user_df, mappings):
    """Create all engineered features matching the training process"""
    
    # Define study_hours_map (not stored in model, so we define it here)
    study_hours_map = {
        'Less than 2 hours': 1,
        '2-4 hours': 3,
        '4-6 hours': 5,
        '6-8 hours': 7,
        'More than 8 hours': 9
    }
    
    # Apply numeric mappings
    user_df['Daily_Usage_Numeric'] = user_df['Daily Usage'].map(mappings['daily_usage_map'])
    user_df['Study_Hours_Numeric'] = user_df['Study Hours'].map(study_hours_map)
    user_df['Sleep_Hours_Numeric'] = user_df['Sleep Hours'].map(mappings['sleep_hours_map'])
    user_df['Recent_Paper_Numeric'] = user_df['Recent Past Paper'].map(mappings['past_paper_score_map'])
    user_df['Papers_Count_Numeric'] = user_df['Past Papers Count'].map(mappings['past_papers_count_map'])
    user_df['Timing_Numeric'] = user_df['Timing Behavior'].map(mappings['timing_behavior_map'])
    user_df['Notification_Numeric'] = user_df['Notification Status'].map(mappings['notification_map'])
    user_df['Avg_Papers_Numeric'] = user_df['Avg Five Papers'].map(mappings['past_paper_score_map'])
    
    # Create engineered features
    user_df['Social_Media_Impact'] = user_df['Daily_Usage_Numeric'] * user_df['Distraction Level']
    user_df['Study_Efficiency'] = user_df['Study_Hours_Numeric'] * user_df['Consistency']
    
    user_df['Sleep_Quality'] = user_df['Sleep_Hours_Numeric'].apply(
        lambda x: 5 if 7 <= x <= 8 else (4 if 6 <= x <= 9 else (3 if 5 <= x <= 10 else 2))
    )
    
    user_df['Past_Paper_Mastery'] = (user_df['Recent_Paper_Numeric'] * user_df['Papers_Count_Numeric']) / 10
    user_df['Time_Management'] = user_df['Timing_Numeric'] * user_df['Consistency']
    
    user_df['Overall_Distraction'] = (
        user_df['Distraction Level'] * 0.5 + 
        user_df['Notification_Numeric'] * 0.3 + 
        user_df['Daily_Usage_Numeric'] * 0.2
    )
    
    user_df['Study_Life_Balance'] = user_df['Study_Hours_Numeric'] / (user_df['Daily_Usage_Numeric'] + 0.1)
    
    user_df['Performance_Consistency'] = (
        (user_df['Consistency'] * user_df['Recent_Paper_Numeric'] * user_df['Avg_Papers_Numeric']) ** (1/3)
    )
    
    user_df['Preparation_Score'] = (
        user_df['Study_Hours_Numeric'] * 0.4 + 
        user_df['Papers_Count_Numeric'] * 0.3 +
        user_df['Consistency'] * 2 * 0.3
    )
    
    user_df['Focus_Score'] = 10 - user_df['Overall_Distraction']
    user_df['Wellness_Score'] = user_df['Sleep_Quality'] - (user_df['Overall_Distraction'] / 2)
    user_df['Practice_Intensity'] = user_df['Papers_Count_Numeric'] / (user_df['Study_Hours_Numeric'] + 1)
    user_df['Study_Quality'] = user_df['Study_Efficiency'] - user_df['Social_Media_Impact']
    
    user_df['Success_Probability'] = (
        user_df['Recent_Paper_Numeric'] * 0.3 +
        user_df['Avg_Papers_Numeric'] * 0.3 +
        user_df['Study_Efficiency'] * 0.2 +
        user_df['Time_Management'] * 0.2
    )
    
    user_df['Notification_Impact'] = user_df['Notification_Numeric'] * user_df['Distraction Level'] * user_df['Daily_Usage_Numeric']
    user_df['Performance_Gap'] = user_df['Recent_Paper_Numeric'] - user_df['Avg_Papers_Numeric']
    
    user_df['Exam_Readiness'] = (
        user_df['Time_Management'] * 0.3 +
        user_df['Past_Paper_Mastery'] * 0.4 +
        user_df['Study_Quality'] * 0.3
    )
    
    user_df['Productivity'] = user_df['Study_Hours_Numeric'] * user_df['Focus_Score'] / 10
    user_df['Study_Hours_Squared'] = user_df['Study_Hours_Numeric'] ** 2
    user_df['Consistency_Squared'] = user_df['Consistency'] ** 2
    user_df['Distraction_Squared'] = user_df['Distraction Level'] ** 2
    
    user_df['Study_Consistency_Papers'] = (
        user_df['Study_Hours_Numeric'] * user_df['Consistency'] * user_df['Recent_Paper_Numeric']
    )
    
    return user_df

def predict(subject, input_data):
    """Make prediction for given subject and input data"""
    try:
        # Load model
        model_data, error = load_model(subject)
        if error:
            return {'error': error}
        
        # Extract components
        model = model_data['model']
        scaler = model_data['scaler']
        label_encoders = model_data['label_encoders']
        grade_encoder = model_data['grade_encoder']
        feature_columns = model_data['feature_columns']
        mappings = model_data['mappings']
        categorical_cols = model_data['categorical_cols']
        
        # Create DataFrame
        user_df = pd.DataFrame([input_data])
        
        # Engineer features
        user_df = engineer_features(user_df, mappings)
        
        # Encode categorical columns
        for col in categorical_cols:
            if col in label_encoders:
                le = label_encoders[col]
                user_df[col] = le.transform(user_df[col])
        
        # Handle NaN values
        user_df = user_df.fillna(user_df.median(numeric_only=True))
        
        # Select features in correct order
        user_features = user_df[feature_columns]
        
        # Scale features
        user_scaled = scaler.transform(user_features)
        
        # Make prediction
        prediction_encoded = model.predict(user_scaled)[0]
        probabilities = model.predict_proba(user_scaled)[0]
        
        # Decode prediction
        prediction_label = grade_encoder.inverse_transform([prediction_encoded])[0]
        grade_labels = grade_encoder.inverse_transform(model.classes_)
        
        # Create probability dictionary
        probs_dict = {str(label): float(prob) for label, prob in zip(grade_labels, probabilities)}
        
        # Get confidence
        confidence = float(np.max(probabilities))
        
        return {
            'predicted_grade': prediction_label,
            'confidence': confidence,
            'probabilities': probs_dict,
            'model_accuracy': float(model_data.get('accuracy', 0)),
            'features_used': len(feature_columns)
        }
        
    except Exception as e:
        return {'error': f"Prediction error: {str(e)}"}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ML Grade Prediction')
    parser.add_argument('--subject', type=str, required=True, help='Subject name')
    parser.add_argument('--input', type=str, required=True, help='Input data as JSON string')
    
    args = parser.parse_args()
    
    try:
        input_data = json.loads(args.input)
        result = predict(args.subject, input_data)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)
