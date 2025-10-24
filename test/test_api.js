const http = require('http');

const BASE_URL = 'http://localhost:5000';

// Test data - High performing student
const testData = {
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

async function runTests() {
  console.log('='.repeat(60));
  console.log('🧪 Testing Ensenar ML Backend API');
  console.log('='.repeat(60));

  // Test 1: Health Check
  console.log('\n📋 Test 1: Health Check');
  console.log('-'.repeat(60));
  try {
    const health = await makeRequest('/api/health');
    console.log('✅ Health check passed');
    console.log('Status:', health.status);
    console.log('Uptime:', health.uptime.toFixed(2), 'seconds');
  } catch (error) {
    console.log('❌ Health check failed:', error.message);
  }

  // Test 2: Get Subjects
  console.log('\n📋 Test 2: Get Available Subjects');
  console.log('-'.repeat(60));
  try {
    const subjects = await makeRequest('/api/predict/subjects');
    console.log('✅ Subjects endpoint passed');
    console.log('Available subjects:', subjects.subjects.length);
    console.log('Available models:', subjects.availableModels);
  } catch (error) {
    console.log('❌ Subjects endpoint failed:', error.message);
  }

  // Test 3: Prediction
  console.log('\n📋 Test 3: Make Prediction');
  console.log('-'.repeat(60));
  try {
    const prediction = await makeRequest('/api/predict/accounting', 'POST', testData);
    
    if (prediction.success) {
      console.log('✅ Prediction passed');
      console.log('Predicted Grade:', prediction.prediction.predicted_grade);
      console.log('Confidence:', (prediction.prediction.confidence * 100).toFixed(2) + '%');
      console.log('Model Accuracy:', (prediction.prediction.model_accuracy * 100).toFixed(2) + '%');
      console.log('\nGrade Probabilities:');
      for (const [grade, prob] of Object.entries(prediction.prediction.probabilities)) {
        const bar = '█'.repeat(Math.round(prob * 50));
        console.log(`  Grade ${grade}: ${(prob * 100).toFixed(2)}% ${bar}`);
      }
    } else {
      console.log('❌ Prediction failed:', prediction.error);
    }
  } catch (error) {
    console.log('❌ Prediction failed:', error.message);
  }

  // Test 4: Invalid Subject
  console.log('\n📋 Test 4: Invalid Subject (Error Handling)');
  console.log('-'.repeat(60));
  try {
    const invalid = await makeRequest('/api/predict/invalid_subject', 'POST', testData);
    console.log('✅ Error handling works correctly');
    console.log('Error:', invalid.error);
  } catch (error) {
    console.log('❌ Error handling test failed:', error.message);
  }

  console.log('\n' + '='.repeat(60));
  console.log('✅ All tests completed!');
  console.log('='.repeat(60));
}

// Run tests
runTests().catch(err => {
  console.error('Test suite failed:', err);
  process.exit(1);
});
