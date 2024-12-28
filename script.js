document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const features = [
        'cylinders', 'displacement', 'horsepower', 'weight',
        'acceleration', 'model_year', 'origin'
    ].map(id => parseFloat(document.getElementById(id).value));

    if (features.some(isNaN)) {
        document.getElementById('result').innerHTML = `
            <div class="alert alert-danger">
                Please enter valid numbers for all fields.
            </div>
        `;
        return;
    }

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ features: features })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.prediction_mpg && data.prediction_km_per_l) {
            document.getElementById('result').innerHTML = `
                <div class="alert alert-info">
                    Predicted Fuel Efficiency:<br>
                    ${data.prediction_mpg} MPG<br>
                    ${data.prediction_km_per_l} km/L
                </div>
            `;
        } else if (data.error) {
            document.getElementById('result').innerHTML = `
                <div class="alert alert-danger">
                    An error occurred: ${data.error}
                </div>
            `;
        }
    } catch (error) {
        document.getElementById('result').innerHTML = `
            <div class="alert alert-danger">
                An error occurred: ${error.message}
            </div>
        `;
    }
});
