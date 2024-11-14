document.getElementById('registrationForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Get input values
    let name = document.getElementById('name').value;
    let email = document.getElementById('email').value;
    let phone = document.getElementById('phone').value;
    let address = document.getElementById('address').value;
    let password = document.getElementById('password').value;
    let confirmPassword = document.getElementById('confirmPassword').value;

    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    // Send data to Python backend (Assuming you're using Flask or another framework)
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, email, phone, address, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === "Registration successful!") {
            // Display registered data to the user
            let output = `
                <h3>Registered Data:</h3>
                <p><strong>Name:</strong> ${data.data.name}</p>
                <p><strong>Email:</strong> ${data.data.email}</p>
                <p><strong>Phone:</strong> ${data.data.phone}</p>
                <p><strong>Address:</strong> ${data.data.address}</p>
            `;
            document.getElementById('registrationOutput').innerHTML = output;
        } else {
            alert(data.message);
        }
    });
});
