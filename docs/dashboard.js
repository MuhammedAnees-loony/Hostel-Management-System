document.addEventListener("DOMContentLoaded", function () {
    // Fetch warden information from an API or backend
    fetch('/api/getWardenInfo')  // Replace with your actual API endpoint
        .then(response => response.json())
        .then(data => {
            document.getElementById("wardenName").textContent = data.name;
            document.getElementById("wardenContact").textContent = data.contact;
            document.getElementById("wardenEmail").textContent = data.email;
            document.getElementById("hostelName").textContent = data.hostelName;
        })
        .catch(error => console.error('Error fetching warden information:', error));
});
