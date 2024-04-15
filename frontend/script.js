document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData();
    const fileInput = document.querySelector('[name=transactionFile]');
    const responseDiv = document.getElementById('response');
    
    // Ensure a file was selected
    if (fileInput.files.length > 0) {
        formData.append('transactionFile', fileInput.files[0]);
        responseDiv.style.display = 'none';  // Hide response div in case it was previously shown
        
        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            responseDiv.textContent = data.message;  // Update response text
            responseDiv.style.display = 'block';  // Show response div
            responseDiv.classList.add('alert-success');  // Add success class if it's not there
        })
        .catch(error => {
            console.error('Error:', error);
            responseDiv.textContent = 'An error occurred while processing your file.';
            responseDiv.style.display = 'block';
            responseDiv.classList.remove('alert-success');
            responseDiv.classList.add('alert-danger');  // Show error in red
        });
    } else {
        responseDiv.textContent = 'Please select a file to upload.';
        responseDiv.style.display = 'block';
        responseDiv.classList.remove('alert-success');
        responseDiv.classList.add('alert-danger');
    }
});

// Update the label of the custom file input to show the file name
document.querySelector('.custom-file-input').addEventListener('change', function(e) {
    var fileName = document.getElementById("transactionFile").files[0].name;
    var nextSibling = e.target.nextElementSibling;
    nextSibling.innerText = fileName;
});
