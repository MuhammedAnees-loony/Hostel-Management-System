document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault(); // Prevent the form from submitting normally

    // Get user input values
    const loginId = document.getElementById('login-id').value;
    const userType = document.getElementById('user-type').value;
    const password = document.getElementById('password').value;

    // Log user input values for debugging
    console.log("Login ID:", loginId);
    console.log("User Type:", userType);
    console.log("Password:", password);

    try {
        // Send POST request to the backend with loginId, userType, and password
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ loginId, userType, password })
        });

        // Log response status for debugging
        console.log("Response Status:", response.status);

        // Handle the backend response
        if (response.ok) {
            const data = await response.json();

            // Log the response data from the backend
            console.log("Response Data:", data);

            if (data.status === 'success') {
                // Store the user details returned by the backend
                console.log("Login successful, storing user details.");
                localStorage.setItem('username', data.data.username);
                localStorage.setItem('role_id', data.data.role_id);

                // Store all user details individually
                for (const [key, value] of Object.entries(data.data.user_details)) {
                    console.log(`Storing ${key}: ${value}`);
                    localStorage.setItem(key, value);
                }

                // Redirect based on user type
                if (userType === "manager") {
                    console.log("Redirecting to manager dashboard.");
                    window.location.href = "dashboard.html"; // Redirect to manager dashboard
                } else if (userType === "student" || userType === "faculty") {
                    console.log("Redirecting to student/faculty dashboard.");
                    window.location.href = "dashboard1.html"; // Redirect to student/faculty dashboard
                }
            } else {
                console.warn("Invalid credentials. Please try again.");
                alert("Invalid credentials. Please try again.");
            }
        } else {
            console.error("Server error:", response.status);
            alert("Server error. Please try again later.");
        }
    } catch (error) {
        console.error("Error occurred:", error);
        alert("An error occurred. Please try again.");
    }
});
