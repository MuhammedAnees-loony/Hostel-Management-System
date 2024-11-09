document.getElementById('attendance-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const date = document.getElementById('date').value;
    const hostelName = document.getElementById('hostel-name').value;
    const userType = document.getElementById('user-type').value;

    alert(`Attendance submitted for ${userType} on ${date} in ${hostelName}.`);
});

function toggleUserType() {
    const userType = document.getElementById('user-type').value;
    const attendanceList = document.getElementById('attendance-list');
    attendanceList.innerHTML = '';

    if (userType === 'student') {
        displayStudentList();
    } else {
        displayFacultyList();
    }
}

function displayStudentList() {
    const students = [
        { id: 1, name: 'John Doe', room: 'A101' },
        { id: 2, name: 'Jane Smith', room: 'B201' },
        { id: 3, name: 'Robert Brown', room: 'C102' }
    ];

    const attendanceList = document.getElementById('attendance-list');
    students.forEach(student => {
        const listItem = document.createElement('div');
        listItem.classList.add('attendance-list-item');

        listItem.innerHTML = `
            <label for="student-${student.id}">${student.name} (Room: ${student.room})</label>
            <input type="radio" id="student-${student.id}" name="attendance-${student.id}" value="present"> Present
            <input type="radio" id="student-${student.id}-absent" name="attendance-${student.id}" value="absent"> Absent
        `;

        attendanceList.appendChild(listItem);
    });
}

function displayFacultyList() {
    const faculties = [
        { id: 1, name: 'Dr. Michael Johnson', department: 'Computer Science' },
        { id: 2, name: 'Prof. Sarah Lee', department: 'Mechanical Engineering' }
    ];

    const attendanceList = document.getElementById('attendance-list');
    faculties.forEach(faculty => {
        const listItem = document.createElement('div');
        listItem.classList.add('attendance-list-item');

        listItem.innerHTML = `
            <label for="faculty-${faculty.id}">${faculty.name} (Dept: ${faculty.department})</label>
            <input type="radio" id="faculty-${faculty.id}" name="attendance-${faculty.id}" value="present"> Present
            <input type="radio" id="faculty-${faculty.id}-absent" name="attendance-${faculty.id}" value="absent"> Absent
        `;

        attendanceList.appendChild(listItem);
    });
}
// Simple validation to ensure 'from date' is not after 'to date'
document.getElementById('date-form').addEventListener('submit', function (event) {
    const fromDate = new Date(document.getElementById('from-date').value);
    const toDate = new Date(document.getElementById('to-date').value);

    if (fromDate > toDate) {
        event.preventDefault();
        alert('The "From Date" cannot be later than the "To Date". Please correct it.');
    }
});
