function sendComplaint() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;

    // Construct the mailto link
    const mailtoLink = `mailto:dbmanagersaintgits.org?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent("Name: " + name + "\nEmail: " + email + "\n\n" + message)}`;

    // Open the mailto link to open the default email client
    window.location.href = mailtoLink;
}
