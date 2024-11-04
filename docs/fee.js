document.getElementById('fee-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting in the traditional way

    const feeCategory = document.getElementById('fee-category').value;
    const receipt = document.getElementById('receipt-upload').files[0];

    const feeStatus = document.getElementById('fee-status');
    const feeMessage = document.getElementById('fee-message');

    // Simulate fee payment status (e.g., pending fees)
    let pendingFees = {
        mess: 5000,
        hostel: 10000
    };

    // Check if the receipt is uploaded
    if (receipt) {
        if (pendingFees[feeCategory] > 0) {
            feeMessage.textContent = `Your ${feeCategory === 'mess' ? 'Mess' : 'Hostel'} Fee of ₹${pendingFees[feeCategory]} is still pending.`;
        } else {
            feeMessage.textContent = "All fees have been paid.";
        }

        // Show the status message
        feeStatus.classList.remove('hidden');
    } else {
        alert("Please upload a fee receipt.");
    }
});
