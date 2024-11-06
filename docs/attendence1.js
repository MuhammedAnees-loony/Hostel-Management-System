// Simple validation to ensure 'from date' is not after 'to date'
document.getElementById('date-form').addEventListener('submit', function (event) {
    const fromDate = new Date(document.getElementById('from-date').value);
    const toDate = new Date(document.getElementById('to-date').value);

    if (fromDate > toDate) {
        event.preventDefault();
        alert('The "From Date" cannot be later than the "To Date". Please correct it.');
    }
});
