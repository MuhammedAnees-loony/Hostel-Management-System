// student.js

document.getElementById("studentForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Gather form data
    const studentData = {
        studentId: document.getElementById("studentId").value,
        studentName: document.getElementById("studentName").value,
        hostelName: document.getElementById("hostelName").value,
        roomAllotment: document.getElementById("roomAllotment").value
    };

    // Send data to the backend
    fetch("/save_student", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(studentData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("responseMessage").innerText = "Student details saved successfully!";
        } else {
            document.getElementById("responseMessage").innerText = "Error saving student details.";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("responseMessage").innerText = "Error connecting to the server.";
    });
});
