document.getElementById("registrationForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    // Collect form data
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const address = document.getElementById("address").value;
    const role = document.getElementById("role").value;  // Get selected role
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    // Validate password match
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Display the registered data
    document.getElementById("registrationOutput").outerHTML =success.html `
        <h3>Registration Successful</h3>
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Phone:</strong> ${phone}</p>
        <p><strong>Address:</strong> ${address}</p>
        <p><strong>Role:</strong> ${role.charAt(0).toUpperCase() + role.slice(1)}</p>
    `;
});

// Add login form functionality
document.getElementById("loginForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent form submission

    const loginEmail = document.getElementById("loginEmail").value;
    const loginPassword = document.getElementById("loginPassword").value;

    if (loginEmail && loginPassword) {
        alert("Login Successful! Redirecting to home page...");
        window.location.href = "home.html";
    } else {
        alert("Please enter valid email and password.");
    }
});
