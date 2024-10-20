// Sample attendance data (This could be dynamic in a real system)
const attendanceData = [
    { date: '2024-10-01', status: 'Present' },
    { date: '2024-10-02', status: 'Absent' },
    { date: '2024-10-03', status: 'Present' }
];

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

// Function to filter attendance by date
function filterAttendance() {
    const selectedDate = document.getElementById('date-filter').value;
    const filteredData = attendanceData.filter(record => record.date === selectedDate);
    
    if (filteredData.length > 0) {
        displayAttendance(filteredData);
    } else {
        alert('No attendance records found for this date.');
        displayAttendance(attendanceData); // Show all data if no match
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
document.getElementById('filter-btn').addEventListener('click', filterAttendance);

// Event listener for the mark leave button
document.getElementById('mark-leave-btn').addEventListener('click', markLeave);
