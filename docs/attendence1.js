document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('fetch-students-btn').addEventListener('click', function () {
        const roomNumber = document.getElementById('room-number').value;
        const hostelName = document.getElementById('hostel-name').value;

        console.log("Room Number:", roomNumber);
        console.log("Hostel Name:", hostelName);

        if (!roomNumber || !hostelName) {
            alert("Please enter room number and select hostel.");
            return;
        }

        // Fetch students from the backend based on room number and hostel
        fetch('http://127.0.0.1:5000/api/getStudents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ roomNumber, hostelName }),
        })
        .then(response => {
            console.log("Response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Data received from backend:", data);
            displayAttendanceList(data.students);
        })
        .catch(error => console.error('Error fetching students:', error));
    });

    // Function to display students in the attendance list
    function displayAttendanceList(students) {
        const attendanceList = document.getElementById('attendance-list');
        attendanceList.innerHTML = ''; // Clear existing list

        console.log("Displaying attendance list for students:", students);

        students.forEach(student => {
            const studentItem = document.createElement('div');
            studentItem.className = 'attendance-list-item';

            studentItem.innerHTML = `
                <label>${student.name} (ID: ${student.id})</label>
                <button class="mark-present-btn" data-id="${student.id}" data-name="${student.name}" data-status="Present">Present</button>
                <button class="mark-absent-btn" data-id="${student.id}" data-name="${student.name}" data-status="Absent">Absent</button>
            `;

            attendanceList.appendChild(studentItem);
        });

       // Event listeners for the attendance buttons
       document.querySelectorAll('.mark-present-btn, .mark-absent-btn').forEach(button => {
        button.addEventListener('click', function () {
            const studentId = this.getAttribute('data-id');
            const studentName = this.getAttribute('data-name');
            const status = this.getAttribute('data-status');
            const date = document.getElementById('date').value;

            console.log("Marking attendance:", {
                studentId,
                studentName,
                status,
                date
            });

            if (!date) {
                alert("Please select a date.");
                return;
            }

            // Send attendance status to the backend
            fetch('http://127.0.0.1:5000/api/markAttendance', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ student_id: studentId, date: date, status: status }),
            })
            .then(response => {
                console.log("Attendance response status:", response.status);
                return response.json();
            })
            .then(data => {
                console.log("Response after marking attendance:", data);
                if (data.success) {
                    alert(`${studentName} marked as ${status}`);
                } else {
                    alert(`Error marking attendance for ${studentName}`);
                }
            })
            .catch(error => console.error('Error submitting attendance:', error));
        });
    });
}
});