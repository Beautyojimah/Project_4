function getForecast() {
    let storeId = document.getElementById('storeSelection').value;
    let days = document.getElementById('daysPrediction').value;

    // Fetch data from Flask backend
    fetch('/forecast', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `store_id=${storeId}&number_of_days=${days}`
    })
    .then(response => response.json())
    .then(data => {
        if (!data || !data.prediction) {
            console.error('Invalid data received from server:', data);
            return;
        }
        
        let daysArray = Array.from({length: data.prediction.length}, (_, i) => `Day ${i + 1}`);
        
        // Main forecast trace
        let forecastData = [{
            x: daysArray,
            y: data.prediction,
            type: 'line',
            name: 'Forecast'
        }];

        // Trend trace
        forecastData.push({
            x: daysArray,
            y: data.trend,
            type: 'line',
            name: 'Trend',
            line: {dash: 'dot'}
        });

        // Yearly seasonality trace
        forecastData.push({
            x: daysArray,
            y: data.yearly,
            type: 'line',
            name: 'Yearly Seasonality',
            line: {dash: 'dot'}
        });

        // Weekly seasonality trace
        forecastData.push({
            x: daysArray,
            y: data.weekly,
            type: 'line',
            name: 'Weekly Seasonality',
            line: {dash: 'dot'}
        });

        // If daily seasonality is available, add its trace
        if (data.daily && data.daily.length) {
            forecastData.push({
                x: daysArray,
                y: data.daily,
                type: 'line',
                name: 'Daily Seasonality',
                line: {dash: 'dot'}
            });
        }

        let layout = {
            title: 'Sales Forecast',
            xaxis: {
                title: 'Days'
            },
            yaxis: {
                title: 'Sales'
            }
        };

        Plotly.newPlot('forecastPlot', forecastData, layout);
    })
    .catch(error => {
        console.error('Error fetching forecast:', error);
    });
}
