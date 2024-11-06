// Retrieve data from localStorage
const loginId = localStorage.getItem('username'); // Using 'username' to match login ID (e.g., 'Mike Adams')
const userType = localStorage.getItem('role_id'); // Assuming 'role_id' indicates user type (e.g., 1 for student)
const roomNumber = localStorage.getItem('room_number'); // Room number, if stored separately in localStorage
const hostelName = localStorage.getItem('hostel_name'); // Hostel name, if stored separately in localStorage

// Additional details from user data
const fullName = localStorage.getItem('Name'); // Full name
const dob = localStorage.getItem('DOB'); // Date of birth
const gender = localStorage.getItem('Gender'); // Gender
const contact = localStorage.getItem('Contact'); // Contact number
const email = localStorage.getItem('Email'); // Email
const address = localStorage.getItem('Address'); // Address
const yearOfStudy = localStorage.getItem('Year_of_Study'); // Year of study

// Display the data in the corresponding HTML elements
document.getElementById('loginId').textContent = fullName || 'Not Available';
document.getElementById('userType').textContent = userType || 'Not Available';
document.getElementById('roomNumber').textContent = roomNumber || 'Not Available';
document.getElementById('hostelName').textContent = hostelName || 'Not Available';

// Additional user details (add these elements in HTML if needed)
document.getElementById('dob').textContent = dob || 'Not Available';
document.getElementById('gender').textContent = gender || 'Not Available';
document.getElementById('contact').textContent = contact || 'Not Available';
document.getElementById('email').textContent = email || 'Not Available';
document.getElementById('address').textContent = address || 'Not Available';
document.getElementById('yearOfStudy').textContent = yearOfStudy || 'Not Available';
