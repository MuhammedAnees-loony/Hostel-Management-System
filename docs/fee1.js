document.getElementById('fee-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const date = document.getElementById('date').value;
    if (!date) {
        alert("Please select a date.");
        return;
    }
    
    // Send the date to the backend to fetch the fee details
    fetch('http://127.0.0.1:5000/api/getFeeDetails', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ date: date })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayDetails(data.users); // Display the users with their fee details
        } else {
            alert('Error fetching fee details.');
        }
    })
    .catch(error => console.error('Error fetching fee details:', error));
});
function openIframePopup(receiptData) {
    const iframe = document.getElementById('receipt-iframe');
    
    // Set the iframe's src to a data URI containing the image data
    iframe.src = 'data:image/jpeg;base64,' + receiptData;  // Assuming the image is base64 encoded as a JPEG

    document.getElementById('iframe-popup').style.display = 'flex';  // Show the popup
}

// Function to close the iframe popup
function closeIframePopup() {
    const iframe = document.getElementById('receipt-iframe');
    iframe.src = '';  // Reset the iframe source to stop the image from displaying
    document.getElementById('iframe-popup').style.display = 'none';  // Hide the popup
}

// Function to close the iframe popup
function closeIframePopup() {
    const iframe = document.getElementById('receipt-iframe');
    iframe.src = '';  // Reset the iframe source to stop the video or image from playing
    document.getElementById('iframe-popup').style.display = 'none';  // Hide the popup
}
function displayDetails(users) {
    const userDetails = document.getElementById('user-details');
    userDetails.innerHTML = ''; // Clear existing details

    users.forEach(user => {
        const info = document.createElement('div');
        info.classList.add('user-info');

        // For fee receipt, open the image in an iframe popup
        const receiptLink = `<a href="javascript:void(0);" onclick="openIframePopup('${user.receipt}')">View Receipt</a>`;

        info.innerHTML = `
            <label>Name:</label> <span>${user.name}</span><br>
            <label>Room:</label> <span>${user.room}</span><br>
            <label>Fee Receipt:</label> ${receiptLink}<br>
            <input type="checkbox" name="verify-${user.id}" value="verified"> Verify
        `;

        userDetails.appendChild(info);
    });
}