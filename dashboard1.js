// Ensure the DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Retrieve data from localStorage
    var loginId = localStorage.getItem('loginId') || 'Guest'; // Default to 'Guest' if missing
    var userType = localStorage.getItem('userType') || 'Unknown';
    var roomNumber = localStorage.getItem('roomNumber') || 'N/A';
    var hostelName = localStorage.getItem('hostelName') || 'N/A';

    // Display the data in the corresponding HTML elements
    document.getElementById('loginId').textContent = loginId;
    document.getElementById('userType').textContent = userType;
    document.getElementById('roomNumber').textContent = roomNumber;
    document.getElementById('hostelName').textContent = hostelName;

// Toggle navigation for mobile view
const navToggle = document.querySelector('#menu-btn');
const navLinks = document.querySelector('.navbar');

navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('show');
});
});
