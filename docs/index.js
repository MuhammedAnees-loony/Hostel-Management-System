document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const loginId = document.getElementById('login-id').value;
    const userType = document.getElementById('user-type').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ loginId, userType, password })
        });

        console.log('Response:', response); // Log the response
        if (response.ok) {
            const data = await response.json();
            console.log('Data:', data); // Log the returned data
            // Handle success...
        } else {
            console.error("Server responded with:", response.status, response.statusText);
            alert("Server error. Please try again later.");
        }
    } catch (error) {
        console.error("Fetch error:", error); // More details on the error
        alert("An error occurred. Please try again.");
    }
});
