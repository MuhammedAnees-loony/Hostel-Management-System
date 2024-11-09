document.addEventListener("DOMContentLoaded", function () {
    // Retrieve individual warden properties from localStorage
    const wardenName = localStorage.getItem('Name');
    const wardenContact = localStorage.getItem('Contact');
    const wardenEmail = localStorage.getItem('Email');
    const hostelName = localStorage.getItem('Hostel_ID');  // You may need to adjust this if you have a separate name for the hostel.

    // Check if all required data is available in localStorage
    if (wardenName && wardenContact && wardenEmail && hostelName) {
        // Update the DOM with the warden's information
        document.getElementById("wardenName").textContent = wardenName;
        document.getElementById("wardenContact").textContent = wardenContact;
        document.getElementById("wardenEmail").textContent = wardenEmail;
        document.getElementById("hostelName").textContent = hostelName;  // Adjust as necessary
    } else {
        console.error('Required warden information is missing in localStorage');
    }
});
