document.getElementById('fee-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Fee receipts verified successfully.');
});

function displayDetails() {
    const userType = document.getElementById('user-type').value;
    const userDetails = document.getElementById('user-details');
    userDetails.innerHTML = '';

    if (userType === 'student') {
        displayStudentDetails();
    } else {
        displayFacultyDetails();
    }
}

function displayStudentDetails() {
    const students = [
        { id: 1, name: 'John Doe', room: 'A101', receipt: 'receipt1.jpg' },
        { id: 2, name: 'Jane Smith', room: 'B201', receipt: 'receipt2.jpg' }
    ];

    const userDetails = document.getElementById('user-details');
    students.forEach(student => {
        const info = document.createElement('div');
        info.classList.add('user-info');

        info.innerHTML = `
            <label>Name:</label> <span>${student.name}</span><br>
            <label>Room:</label> <span>${student.room}</span><br>
            <label>Fee Receipt:</label>
            <a href="${student.receipt}" target="_blank">View Receipt</a>
            <input type="checkbox" name="verify-${student.id}" value="verified"> Verify
        `;

        userDetails.appendChild(info);
    });
}

function displayFacultyDetails() {
    const faculties = [
        { id: 1, name: 'Dr. Michael Johnson', dept: 'Computer Science', receipt: 'receipt3.jpg' },
        { id: 2, name: 'Prof. Sarah Lee', dept: 'Mechanical Engineering', receipt: 'receipt4.jpg' }
    ];

    const userDetails = document.getElementById('user-details');
    faculties.forEach(faculty => {
        const info = document.createElement('div');
        info.classList.add('user-info');

        info.innerHTML = `
            <label>Name:</label> <span>${faculty.name}</span><br>
            <label>Department:</label> <span>${faculty.dept}</span><br>
            <label>Fee Receipt:</label>
            <a href="${faculty.receipt}" target="_blank">View Receipt</a>
            <input type="checkbox" name="verify-${faculty.id}" value="verified"> Verify
        `;

        userDetails.appendChild(info);
    });
}

