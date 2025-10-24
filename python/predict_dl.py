import sys
import json
import pickle
import numpy as np
import argparse
from pathlib import Path

def load_deep_learning_model():
    """Load the deep learning model and preprocessing objects"""
    try:
        import tensorflow as tf
        
        model_path = Path(__file__).parent.parent / 'models' / 'grade_a_predictor.h5'
        preprocessing_path = Path(__file__).parent.parent / 'models' / 'preprocessing_objects.pkl'
        
        if not model_path.exists():
            return None, None, f"Model file not found: {model_path}"
        
        if not preprocessing_path.exists():
            return None, None, f"Preprocessing file not found: {preprocessing_path}"
        
        # Load model
        model = tf.keras.models.load_model(str(model_path))
        
        # Load preprocessing objects
        with open(preprocessing_path, 'rb') as f:
            preprocessing = pickle.load(f)
        
        return model, preprocessing, None
    except Exception as e:
        return None, None, f"Error loading model: {str(e)}"

def predict_grade_a(input_data):
    """Make Grade A prediction using deep learning model"""
    try:
        # Load model
        model, preprocessing, error = load_deep_learning_model()
        if error:
            return {'error': error}
        
        # Extract preprocessing objects
        label_encoders = preprocessing['label_encoders']
        scaler = preprocessing['scaler']
        feature_columns = preprocessing['feature_columns']
        categorical_cols = preprocessing['categorical_cols']
        numeric_cols = preprocessing['numeric_cols']
        
        # Encode input
        encoded_input = []
        for col in feature_columns:
            if col in categorical_cols:
                val = input_data.get(col, '')
                le = label_encoders.get(col)
                if le:
                    try:
                        code = le.transform([str(val)])[0]
                    except:
                        code = 0  # default
                else:
                    code = 0
                encoded_input.append(code)
            else:  # numeric
                encoded_input.append(float(input_data.get(col, 0)))
        
        # Scale input
        input_array = np.array([encoded_input])
        input_scaled = scaler.transform(input_array)
        
        # Make prediction
        probability = model.predict(input_scaled, verbose=0)[0][0]
        predicted_grade = 'A' if probability >= 0.5 else 'Not A'
        
        # Generate comprehensive recommendations
        analysis, recommendations, combined_effect = generate_comprehensive_recommendations(
            input_data, model, scaler, label_encoders, 
            feature_columns, categorical_cols, probability
        )
        
        return {
            'predicted_grade': predicted_grade,
            'grade_a_probability': float(probability),
            'probability_percentage': f"{float(probability) * 100:.2f}%",
            'confidence': float(probability if probability >= 0.5 else 1 - probability),
            'status': get_status(probability),
            'current_status_analysis': analysis,
            'prioritized_recommendations': recommendations,
            'combined_effect': combined_effect,
            'model_type': 'deep_learning',
            'architecture': '5-layer neural network (128-64-32-16-1)'
        }
        
    except Exception as e:
        return {'error': f"Prediction error: {str(e)}"}

def get_status(probability):
    """Get status assessment based on probability"""
    if probability >= 0.8:
        return "EXCELLENT"
    elif probability >= 0.6:
        return "GOOD"
    elif probability >= 0.4:
        return "NEEDS IMPROVEMENT"
    else:
        return "CRITICAL"

def generate_comprehensive_recommendations(input_data, model, scaler, label_encoders, 
                                          feature_columns, categorical_cols, baseline_prob):
    """Generate comprehensive recommendations like the notebook"""
    
    # Analyze current status
    analysis = analyze_current_status(input_data, baseline_prob)
    
    # Define improvement hierarchy with priorities
    improvements = {
        "Daily Usage": {
            "options": ["1-2 hours", "Less than 1 hour"],
            "priority": get_priority(input_data.get("Daily Usage", ""), 
                                    ["More than 4 hours", "3-4 hours", "2-3 hours"], 
                                    "CRITICAL", "HIGH", "MEDIUM"),
            "reason": "Reduce social media to free up valuable study time"
        },
        "Study Hours": {
            "options": ["6-8 hours", "More than 8 hours"],
            "priority": get_priority(input_data.get("Study Hours", ""), 
                                    ["Less than 2 hours", "2-4 hours"], 
                                    "CRITICAL", "HIGH", "MEDIUM"),
            "reason": "Increase study hours for better preparation and understanding"
        },
        "Past Papers Count": {
            "options": ["31-40 papers", "More than 40 papers"],
            "priority": get_priority(input_data.get("Past Papers Count", ""), 
                                    ["0-10 papers", "11-20 papers"], 
                                    "CRITICAL", "HIGH", "MEDIUM"),
            "reason": "Practice more past papers to build exam confidence and familiarity"
        },
        "Sleep Hours": {
            "options": ["7-8 hours"],
            "priority": get_priority(input_data.get("Sleep Hours", ""), 
                                    ["Less than 5 hours", "5-6 hours"], 
                                    "CRITICAL", "HIGH", "MEDIUM"),
            "reason": "Adequate sleep improves focus, memory retention, and cognitive performance"
        },
        "Consistency": {
            "options": [4, 5],
            "priority": get_priority(input_data.get("Consistency", 0), 
                                    [1, 2], 
                                    "CRITICAL", "HIGH", "MEDIUM"),
            "reason": "Consistent study habits lead to better long-term retention and results"
        },
        "Notification Status": {
            "options": ["Always turned off", "Sometimes turned off"],
            "priority": get_priority(input_data.get("Notification Status", ""), 
                                    ["Always kept on", "Usually kept on"], 
                                    "HIGH", "MEDIUM", "LOW"),
            "reason": "Minimize distractions to maintain focus during study sessions"
        },
        "Recent Past Paper": {
            "options": ["70-85%", "Above 85%"],
            "priority": get_priority(input_data.get("Recent Past Paper", ""), 
                                    ["Below 40%", "40-55%"], 
                                    "HIGH", "MEDIUM", "LOW"),
            "reason": "Improve recent performance through targeted practice and review"
        },
        "Avg Five Papers": {
            "options": ["70-85%", "Above 85%"],
            "priority": get_priority(input_data.get("Avg Five Papers", ""), 
                                    ["Below 40%", "40-55%"], 
                                    "HIGH", "MEDIUM", "LOW"),
            "reason": "Consistent high scores indicate strong understanding and readiness"
        },
        "Timing Behavior": {
            "options": ["Always completed within the allocated time limit"],
            "priority": "MEDIUM" if "exceeded" in str(input_data.get("Timing Behavior", "")).lower() else "LOW",
            "reason": "Better time management improves exam performance and reduces stress"
        }
    }
    
    # Test each improvement and measure impact
    best_changes = {}
    for feature, config in improvements.items():
        if config["priority"] == "LOW":
            continue
            
        best_val = None
        best_prob = baseline_prob
        
        for val in config["options"]:
            test_input = input_data.copy()
            test_input[feature] = val
            
            test_prob = predict_probability(test_input, model, scaler, label_encoders, 
                                          feature_columns, categorical_cols)
            
            if test_prob > best_prob:
                best_prob = test_prob
                best_val = val
        
        if best_val is not None and (best_prob - baseline_prob) > 0.005:
            best_changes[feature] = {
                "current": str(input_data.get(feature, "")),
                "suggested": str(best_val),
                "priority": config["priority"],
                "reason": config["reason"],
                "improvement": (best_prob - baseline_prob) * 100,
                "new_probability": best_prob * 100
            }
    
    # Sort by priority then improvement
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}
    sorted_recommendations = sorted(
        best_changes.items(),
        key=lambda x: (priority_order.get(x[1]["priority"], 3), -x[1]["improvement"])
    )
    
    # Format recommendations
    recommendations = []
    for feature, details in sorted_recommendations[:5]:
        recommendations.append({
            "feature": feature,
            "priority": details["priority"],
            "current": details["current"],
            "suggested": details["suggested"],
            "reason": details["reason"],
            "improvement": f"+{details['improvement']:.2f}%",
            "new_probability": f"{details['new_probability']:.2f}%"
        })
    
    # Calculate combined effect
    combined_effect = calculate_combined_effect(
        input_data, best_changes, model, scaler, label_encoders, 
        feature_columns, categorical_cols, baseline_prob
    )
    
    return analysis, recommendations, combined_effect

def get_priority(current, bad_values, critical, high, medium):
    """Determine priority based on current value"""
    if current in bad_values[:1] if len(bad_values) > 0 else []:
        return critical
    elif current in bad_values:
        return high
    return medium

def predict_probability(input_data, model, scaler, label_encoders, 
                       feature_columns, categorical_cols):
    """Helper to predict probability for given input"""
    encoded = []
    for col in feature_columns:
        if col in categorical_cols:
            val = input_data.get(col, '')
            le = label_encoders.get(col)
            if le:
                try:
                    code = le.transform([str(val)])[0]
                except:
                    code = 0
            else:
                code = 0
            encoded.append(code)
        else:
            encoded.append(float(input_data.get(col, 0)))
    
    arr = np.array([encoded])
    scaled = scaler.transform(arr)
    return model.predict(scaled, verbose=0)[0][0]

def analyze_current_status(input_data, baseline_prob):
    """Analyze current student status"""
    analysis = {
        "grade_a_probability": f"{baseline_prob * 100:.2f}%",
        "status_assessment": get_status(baseline_prob)
    }
    
    # Analyze key factors
    factors = {}
    
    # Social Media
    sm_usage = input_data.get("Daily Usage", "")
    if "More than 4" in sm_usage or "3-4" in sm_usage:
        factors["social_media"] = {"status": "HIGH USAGE", "impact": "Significantly impacting study time"}
    elif "2-3" in sm_usage:
        factors["social_media"] = {"status": "MODERATE", "impact": "Should be reduced"}
    else:
        factors["social_media"] = {"status": "GOOD", "impact": "Well controlled"}
    
    # Study Hours
    study = input_data.get("Study Hours", "")
    if "Less than 2" in study or "2-4" in study:
        factors["study_hours"] = {"status": "INSUFFICIENT", "impact": "Need significant increase"}
    elif "4-6" in study:
        factors["study_hours"] = {"status": "BELOW OPTIMAL", "impact": "Should increase"}
    else:
        factors["study_hours"] = {"status": "GOOD", "impact": "Adequate time investment"}
    
    # Past Papers
    papers = input_data.get("Past Papers Count", "")
    if "0-10" in papers or "11-20" in papers:
        factors["past_papers"] = {"status": "LOW", "impact": "Critical for improvement"}
    elif "21-30" in papers:
        factors["past_papers"] = {"status": "MODERATE", "impact": "Should practice more"}
    else:
        factors["past_papers"] = {"status": "GOOD", "impact": "Adequate practice"}
    
    # Sleep
    sleep = input_data.get("Sleep Hours", "")
    if "Less than 5" in sleep or "5-6" in sleep:
        factors["sleep"] = {"status": "INSUFFICIENT", "impact": "Affecting performance"}
    elif "6-7" in sleep:
        factors["sleep"] = {"status": "BELOW OPTIMAL", "impact": "Should improve"}
    else:
        factors["sleep"] = {"status": "GOOD", "impact": "Adequate rest"}
    
    # Consistency
    consistency = input_data.get("Consistency", 0)
    if consistency <= 2:
        factors["consistency"] = {"status": "LOW", "impact": "Major area for improvement"}
    elif consistency <= 3:
        factors["consistency"] = {"status": "MODERATE", "impact": "Should be more consistent"}
    else:
        factors["consistency"] = {"status": "GOOD", "impact": "Well maintained"}
    
    analysis["key_factors"] = factors
    return analysis

def calculate_combined_effect(input_data, best_changes, model, scaler, 
                              label_encoders, feature_columns, categorical_cols, baseline_prob):
    """Calculate combined effect of all recommendations"""
    combined_input = input_data.copy()
    for feature, details in best_changes.items():
        combined_input[feature] = details["suggested"]
    
    combined_prob = predict_probability(combined_input, model, scaler, 
                                       label_encoders, feature_columns, categorical_cols)
    
    total_improvement = (combined_prob - baseline_prob) * 100
    
    # Determine action plan
    if combined_prob >= 0.8:
        action_plan = "EXCELLENT! With these changes, you're highly likely to achieve Grade A!"
        timeline = "Week 1-2: CRITICAL priorities, Week 3-4: HIGH priorities, Week 5+: Maintain improvements"
    elif combined_prob >= 0.65:
        action_plan = "PROMISING! You're on the right track to Grade A with consistent effort."
        timeline = "Week 1-3: CRITICAL priorities, Week 4-6: HIGH priorities, Week 7+: Maintain and fine-tune"
    else:
        action_plan = "ATTENTION NEEDED: Significant effort required for Grade A."
        timeline = "Immediate: Start CRITICAL priorities TODAY, Week 1-4: Gradually add others, Ongoing: Seek additional support"
    
    return {
        "current_probability": f"{baseline_prob * 100:.2f}%",
        "projected_probability": f"{combined_prob * 100:.2f}%",
        "total_improvement": f"+{total_improvement:.2f}%",
        "action_plan": action_plan,
        "timeline": timeline,
        "success_tips": [
            "Make changes gradually - don't overwhelm yourself",
            "Track your daily progress",
            "Set specific, measurable goals for each week",
            "Reward yourself for maintaining improvements",
            "Seek help when stuck - don't struggle alone"
        ]
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deep Learning Grade A Prediction')
    parser.add_argument('--input', type=str, required=True, help='Input data as JSON string')
    
    args = parser.parse_args()
    
    try:
        input_data = json.loads(args.input)
        result = predict_grade_a(input_data)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.exit(1)
