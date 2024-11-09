document.getElementById('fee-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting in the traditional way

    const feeCategory = document.getElementById('fee-category').value;
    const receipt = document.getElementById('receipt-upload').files[0];
    if (receipt) {
        console.log('File size: ', receipt.size);  // Output in bytes
        if (receipt.size > 64 * 1024 * 1024) {    // 64MB in bytes
            alert('The file is too large. Please upload a smaller file.');
        }
    }
    
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

        // Fetch the user_id from localStorage
        const userId = localStorage.getItem('user_id');
        
        if (!userId) {
            alert("User is not logged in.");
            return;
        }

        // Create a FormData object to send to the backend
        const formData = new FormData();
        formData.append('user_id', userId);
        formData.append('fee_category', feeCategory);
        formData.append('image', receipt);

        // Send the data to the backend
        fetch('http://127.0.0.1:5000/upload_fee_payment', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the backend
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
    } else {
        alert("Please upload a fee receipt.");
    }
});
