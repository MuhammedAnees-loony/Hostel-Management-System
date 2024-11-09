const attendanceData = [];

// Sample leave data
const leaveData = [];

// Function to display attendance data in the table
function displayAttendance(data) {
    const tableBody = document.querySelector('#attendance-table tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    data.forEach(record => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${record.date}</td><td>${record.status}</td>`;
        tableBody.appendChild(row);
    });
}

// Function to display leave data in the leave table
function displayLeave(data) {
    const tableBody = document.querySelector('#leave-table tbody');
    tableBody.innerHTML = ''; // Clear existing rows

    data.forEach(record => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${record.date}</td><td>${record.reason}</td><td>${record.duration} days</td>`;
        tableBody.appendChild(row);
    });
}

// Function to filter attendance by date and fetch data from backend
async function filterAttendance() {
    const selectedDate = document.getElementById('date-filter').value;
    const studentId = localStorage.getItem('user_id'); // Get student_id from local storage

    if (!selectedDate) {
        alert('Please select a date.');
        return;
    }
    
    if (!studentId) {
        alert('Student ID not found in local storage.');
        return;
    }

    try {
        // Send POST request to the backend
        console.log("Sending request to backend...")
        const response = await fetch('http://127.0.0.1:5000/attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                student_id: studentId,
                date: selectedDate
            })
        });

        const result = await response.json();

        if (response.ok && result.status === 'success') {
            console.log("Response Data:",result.data);
            const formattedData = result.data.map(record => {
                // Convert the date string to a Date object and format it
                const dateObj = new Date(record.Date);
                const formattedDate = dateObj.toISOString().split('T')[0]; // Get only the date part
                return {
                    date: formattedDate,
                    status: record.Status
                };
            });
            displayAttendance(formattedData);
        } else {
            alert(result.message || 'Failed to fetch attendance records.');
            displayAttendance([]); // Clear table if no data
        }
    } catch (error) {
        console.error('Error fetching attendance data:', error);
        alert('An error occurred while fetching attendance data.');
    }
}

// Function to mark a leave and add it to the leave table
function markLeave() {
    const leaveDate = document.getElementById('leave-date').value;
    const leaveReason = document.getElementById('leave-reason').value;
    const leaveDuration = document.getElementById('leave-duration').value;

    if (leaveDate && leaveReason && leaveDuration) {
        // Add leave record
        leaveData.push({
            date: leaveDate,
            reason: leaveReason,
            duration: leaveDuration
        });
        
        // Display updated leave data
        displayLeave(leaveData);
        
        // Clear form fields
        document.getElementById('leave-date').value = '';
        document.getElementById('leave-reason').value = '';
        document.getElementById('leave-duration').value = '';
    } else {
        alert('Please fill in all leave details.');
    }
}

// Initial display of all attendance data
displayAttendance(attendanceData);

// Event listener for the filter button
document.getElementById('filter-btn').addEventListener('click', function() {
    console.log("Filter button clicked.");
    filterAttendance();
    

});

// Event listener for the mark leave button
document.getElementById('mark-leave-btn').addEventListener('click', markLeave);
