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
// Debugging - Log all retrieved data
console.log("Retrieved from localStorage:");
console.log("Username (loginId):", loginId);
console.log("User Type (role_id):", userType);
console.log("Room Number:", roomNumber);
console.log("Hostel Name:", hostelName);
console.log("Full Name:", fullName);
console.log("Date of Birth:", dob);
console.log("Gender:", gender);
console.log("Contact:", contact);
console.log("Email:", email);
console.log("Address:", address);
console.log("Year of Study:", yearOfStudy)
// Additional user details (add these elements in HTML if needed)
document.getElementById('dob').textContent = dob || 'Not Available';
document.getElementById('gender').textContent = gender || 'Not Available';
document.getElementById('contact').textContent = contact || 'Not Available';
document.getElementById('email').textContent = email || 'Not Available';
document.getElementById('address').textContent = address || 'Not Available';
document.getElementById('yearOfStudy').textContent = yearOfStudy || 'Not Available';
