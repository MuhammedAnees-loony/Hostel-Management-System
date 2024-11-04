document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the form from submitting normally

    // Get user input values
    var loginId = document.getElementById('login-id').value;
    var userType = document.getElementById('user-type').value;

    // Static values for room and hostel (in a real system, you'd retrieve these from a server)
    var roomNumber = "101"; // Example room number
    var hostelName = "Saintgits Hostel";

    // Store the data in localStorage
    localStorage.setItem('loginId', loginId);
    localStorage.setItem('userType', userType);
    localStorage.setItem('roomNumber', roomNumber);
    localStorage.setItem('hostelName', hostelName);

    // Redirect based on user type
    if (userType === "manager") {
        window.location.href = "dashboard.html"; // Redirect to manager dashboard
    } else if (userType === "student" || userType === "faculty") {
        window.location.href = "dashboard1.html"; // Redirect to student/faculty dashboard
    }
});
