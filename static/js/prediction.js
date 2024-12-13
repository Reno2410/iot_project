// Handle form submission and prediction
const form = document.getElementById('predictForm');
const loader = document.getElementById('loader');
const results = document.getElementById('results');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Clear previous results and show loader
    results.style.display = 'none';
    loader.style.display = 'block';

    // Get form data
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;

    // Make POST request to server
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `latitude=${latitude}&longitude=${longitude}`
    });

    // Hide loader and display results
    loader.style.display = 'none';

    if (response.ok) {
        const data = await response.json();

        // Update results
        document.getElementById('resultLatitude').textContent = data.latitude;
        document.getElementById('resultLongitude').textContent = data.longitude;
        document.getElementById('resultWeather').textContent = data.weather_data.weather_description;
        document.getElementById('resultTemperature').textContent = data.weather_data.temp;
        document.getElementById('resultHumidity').textContent = data.weather_data.humidity;
        document.getElementById('resultCrimeType').textContent = data.predicted_crime;
        document.getElementById('resultProbability').textContent = (data.probability * 100).toFixed(2);
        document.getElementById('resultRecommendation').textContent = data.recommendation;

        results.style.display = 'block';
    } else {
        alert('Failed to get prediction. Please try again.');
    }
});

// Handle return to home button click
const homeButton = document.getElementById('homeButton');
homeButton.addEventListener('click', () => {
    window.location.href = '/'; // Redirect to the home page
});
