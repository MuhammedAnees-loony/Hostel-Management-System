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

function displayDetails(users) {
    const userDetails = document.getElementById('user-details');
    userDetails.innerHTML = ''; // Clear existing details

    users.forEach(user => {
        const info = document.createElement('div');
        info.classList.add('user-info');

        info.innerHTML = `
            <label>Name:</label> <span>${user.name}</span><br>
            <label>Room:</label> <span>${user.room}</span><br>
            <label>Fee Receipt:</label>
            <a href="${user.receipt}" target="_blank">View Receipt</a><br>
            <input type="checkbox" name="verify-${user.id}" value="verified"> Verify
        `;

        userDetails.appendChild(info);
    });
}
