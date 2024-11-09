document.getElementById('fee-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting in the traditional way

    const feeCategory = document.getElementById('fee-category').value; // Fee category (though it won't be used in this case)
    const receipt = document.getElementById('receipt-upload').files[0]; // Uploaded receipt file

    const feeStatus = document.getElementById('fee-status');
    const feeMessage = document.getElementById('fee-message');

    // Simulate fee payment status (e.g., pending fees)
    let pendingFees = {
        mess: 5000,
        hostel: 10000
    };

    // Check if the receipt is uploaded
    if (receipt) {
        console.log('File size: ', receipt.size);  // Output in bytes
        if (receipt.size > 64 * 1024 * 1024) {    // 64MB in bytes
            alert('The file is too large. Please upload a smaller file.');
        }
    }

    // Fetch the user_id from localStorage
    const userId = localStorage.getItem('user_id');
    
    if (!userId) {
        alert("User is not logged in.");
        return;
    }

    // Create a FormData object to send to the backend
    const formData = new FormData();
    formData.append('user_id', userId);

    // First, send a request to check the fee status before proceeding with the receipt upload
    fetch('http://127.0.0.1:5000/get_fee_status', {
        method: 'POST',
        body: JSON.stringify({ user_id: userId }), // Send user_id as JSON
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const pendingAmount = data.pending_amount;
            if (pendingAmount > 0) {
                feeMessage.textContent = `You have a pending fee of ₹${pendingAmount}. Please make the payment.`;
            } else {
                feeMessage.textContent = "All fees have been paid.";
            }

            // Show the status message
            feeStatus.classList.remove('hidden');

            // After checking fee status, proceed with uploading the receipt if necessary
            if (receipt) {
                // Create FormData for uploading the receipt
                const formData = new FormData();
                formData.append('user_id', userId);
                formData.append('fee_category', feeCategory); // Optional if needed
                formData.append('image', receipt);

                // Send the receipt to the backend
                fetch('http://127.0.0.1:5000/upload_fee_payment', {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert("Fee payment receipt uploaded successfully.");
                    } else {
                        alert("Error uploading the payment receipt.");
                    }
                })
                .catch(error => {
                    console.error("Error uploading the payment receipt:", error);
                    alert("An error occurred while uploading the payment receipt.");
                });
            }
        } else {
            alert("Error fetching fee status.");
        }
    })
    .catch(error => {
        console.error("Error fetching fee status:", error);
        alert("An error occurred while checking the fee status.");
    });
});
