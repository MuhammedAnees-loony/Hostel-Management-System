document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // Prevent the form from submitting normally

    // Get user input values
    const loginId = document.getElementById('login-id').value;
    const userType = document.getElementById('user-type').value;
    const password = document.getElementById('password').value;

    try {
        // Send POST request to the backend with loginId, userType, and password
        const response = await fetch("http://127.0.0.1:5000", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ loginId, userType, password })
        });

        // Handle the backend response
        if (response.ok) {
            const data = await response.json();
            if (data.status === 'success') {
                // Store the user details returned by the backend
                localStorage.setItem('username', data.data.username);
                localStorage.setItem('role_id', data.data.role_id);
                
                // Store all user details individually
                for (const [key, value] of Object.entries(data.data.user_details)) {
                    localStorage.setItem(key, value);
                }

                // Redirect based on user type
                if (userType === "manager") {
                    window.location.href = "dashboard.html"; // Redirect to manager dashboard
                } else if (userType === "student" || userType === "faculty") {
                    window.location.href = "dashboard1.html"; // Redirect to student/faculty dashboard
                }
            } else {
                alert("Invalid credentials. Please try again.");
            }
        } else {
            console.error("Server error:", response.status);
            alert("Server error. Please try again later.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    }
});
