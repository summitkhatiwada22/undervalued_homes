document.getElementById('predictButton').addEventListener('click', function() {
    let location = document.getElementById('locationInput').value;
    fetch(`/predict?location=${location}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('results').innerText = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            document.getElementById('results').innerText = 'Error: ' + error;
        });
});
