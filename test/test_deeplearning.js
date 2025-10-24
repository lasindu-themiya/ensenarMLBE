const http = require('http');

const BASE_URL = 'http://localhost:5000';

// Test data
const testData = {
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
};

function makeRequest(path, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          resolve(body);
        }
      });
    });

    req.on('error', reject);

    if (data) {
      req.write(JSON.stringify(data));
    }
    req.end();
  });
}

async function testDeepLearning() {
  console.log('='.repeat(70));
  console.log('🧠 Testing Deep Learning Grade A Prediction API');
  console.log('='.repeat(70));

  console.log('\n📋 Test: Deep Learning Prediction with Recommendations');
  console.log('-'.repeat(70));
  try {
    const prediction = await makeRequest('/api/deeplearning', 'POST', testData);
    
    if (prediction.success) {
      console.log('✅ Deep Learning Prediction passed\n');
      console.log(`Predicted Grade: ${prediction.prediction.predicted_grade}`);
      console.log(`Grade A Probability: ${(prediction.prediction.grade_a_probability * 100).toFixed(2)}%`);
      console.log(`Confidence: ${(prediction.prediction.confidence * 100).toFixed(2)}%`);
      console.log(`Status: ${prediction.prediction.status}`);
      console.log(`Model Type: ${prediction.prediction.model_type}`);
      console.log(`Architecture: ${prediction.prediction.architecture}`);
      
      if (prediction.prediction.recommendations && prediction.prediction.recommendations.length > 0) {
        console.log('\n📚 Top Recommendations for Improvement:');
        prediction.prediction.recommendations.forEach((rec, idx) => {
          console.log(`\n${idx + 1}. ${rec.feature}`);
          console.log(`   Current: ${rec.current}`);
          console.log(`   Suggested: ${rec.suggested}`);
          console.log(`   Reason: ${rec.reason}`);
          console.log(`   Improvement: ${rec.improvement}`);
          console.log(`   New Probability: ${rec.new_probability}`);
        });
      }
    } else {
      console.log('❌ Deep Learning Prediction failed:', prediction.error);
    }
  } catch (error) {
    console.log('❌ Deep Learning Prediction failed:', error.message);
  }

  console.log('\n' + '='.repeat(70));
  console.log('✅ Test completed!');
  console.log('='.repeat(70));
}

// Run test
testDeepLearning().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
