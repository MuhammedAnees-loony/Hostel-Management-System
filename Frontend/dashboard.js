// Retrieve data from localStorage
var loginId = localStorage.getItem('loginId');
var userType = localStorage.getItem('userType');
var roomNumber = localStorage.getItem('roomNumber');
var hostelName = localStorage.getItem('hostelName');

// Display the data in the corresponding HTML elements
document.getElementById('loginId').textContent = loginId;
document.getElementById('userType').textContent = userType;
document.getElementById('roomNumber').textContent = roomNumber;
document.getElementById('hostelName').textContent = hostelName;
