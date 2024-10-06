// Event listener for the login form submission
document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent default form submission

    const username = document.getElementById('username').value; // Get username
    const password = document.getElementById('password').value; // Get password

    try {
        // Make a POST request to the login endpoint
        const response = await axios.post('http://localhost:5000/login', {
            username: username,
            password: password
        });

        // Display success message
        document.getElementById('login-message').textContent = response.data.message;
        document.getElementById('login-message').className = 'text-success'; // Optional: Add success class for styling
    } catch (error) {
        // Display error message if login fails
        document.getElementById('login-message').textContent = error.response?.data?.message || "An error occurred.";
        document.getElementById('login-message').className = 'text-danger'; // Optional: Add error class for styling
    }
});

// Event listener for user type selection
document.getElementById('user-type').addEventListener('change', function (e) {
    const userType = e.target.value; // Get selected user type

    // Hide all conditional fields initially
    document.querySelectorAll('.conditional-fields').forEach(field => {
        field.style.display = 'none';
    });

    // Show fields based on selected user type
    if (userType === 'student') {
        document.getElementById('student-fields').style.display = 'block';
    } else if (userType === 'faculty') {
        document.getElementById('faculty-fields').style.display = 'block';
    } else if (userType === 'warden') {
        document.getElementById('warden-fields').style.display = 'block';
    }
});

// Event listener for the registration form submission
document.getElementById('register-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent default form submission

    const userType = document.getElementById('user-type').value; // Get user type
    const name = document.getElementById('name').value; // Get name
    const contact = document.getElementById('contact').value; // Get contact
    const email = document.getElementById('email').value; // Get email

    // Initialize data object
    const data = { user_type: userType, name: name, contact: contact, email: email };

    // Add additional fields based on user type
    if (userType === 'student') {
        data.dob = document.getElementById('dob').value;
        data.gender = document.getElementById('gender').value;
        data.address = document.getElementById('address').value;
        data.year_of_study = document.getElementById('year_of_study').value;
    } else if (userType === 'faculty') {
        data.department = document.getElementById('department').value;
    } else if (userType === 'warden') {
        data.address = document.getElementById('warden-address').value;
        data.hostel_id = document.getElementById('hostel_id').value;
    }

    try {
        // Make a POST request to the register_user endpoint
        const response = await axios.post('http://localhost:5000/register_user', data);
        // Display success message
        document.getElementById('register-message').textContent = response.data.message;
        document.getElementById('register-message').className = 'text-success'; // Optional: Add success class for styling
    } catch (error) {
        // Display error message if registration fails
        document.getElementById('register-message').textContent = error.response?.data?.message || "An error occurred.";
        document.getElementById('register-message').className = 'text-danger'; // Optional: Add error class for styling
    }
});
