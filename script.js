document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await axios.post('http://localhost:5000/login', {
            username: username,
            password: password
        });

        document.getElementById('login-message').textContent = response.data.message;
    } catch (error) {
        document.getElementById('login-message').textContent = error.response.data.message;
    }
});

document.getElementById('user-type').addEventListener('change', function (e) {
    const userType = e.target.value;
    document.querySelectorAll('.conditional-fields').forEach(field => {
        field.style.display = 'none';
    });

    if (userType === 'student') {
        document.getElementById('student-fields').style.display = 'block';
    } else if (userType === 'faculty') {
        document.getElementById('faculty-fields').style.display = 'block';
    } else if (userType === 'warden') {
        document.getElementById('warden-fields').style.display = 'block';
    }
});

document.getElementById('register-form').addEventListener('submit', async function (e) {
    e.preventDefault();

    const userType = document.getElementById('user-type').value;
    const name = document.getElementById('name').value;
    const contact = document.getElementById('contact').value;
    const email = document.getElementById('email').value;

    const data = { user_type: userType, name: name, contact: contact, email: email };

    if (userType === 'student') {
        data.dob = document.getElementById('dob').value;
        data.gender = document.getElementById('gender').value;
        data.address = document.getElementById('address').value;
        data.year_of_study = document.getElementById('year_of_study').value;
    } else if (userType === 'faculty') {
        data.department = document.getElementById('department').value;
    } else if (userType === 'warden') {
        data.warden_address = document.getElementById('warden-address').value;
        data.hostel_id = document.getElementById('hostel_id').value;
    }

    try {
        const response = await axios.post('http://localhost:5000/register_user', data);
        document.getElementById('register-message').textContent = response.data.message;
    } catch (error) {
        document.getElementById('register-message').textContent = error.response.data.message;
    }
});
