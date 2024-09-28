document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    // Clear previous errors
    document.getElementById('usernameError').innerText = '';
    document.getElementById('emailError').innerText = '';
    document.getElementById('passwordError').innerText = '';
    document.getElementById('phoneError').innerText = '';

    const formData = new FormData(this);

    fetch("{% url 'register' %}", {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errors => {
                if (errors.username) {
                    document.getElementById('usernameError').innerText = errors.username;
                }
                if (errors.email) {
                    document.getElementById('emailError').innerText = errors.email;
                }
                if (errors.password) {
                    document.getElementById('passwordError').innerText = errors.password;
                }
                if (errors.phone) {
                    document.getElementById('phoneError').innerText = errors.phone;
                }
            });
        } else {
            // If successful, redirect to login
            window.location.href = "{% url 'login' %}";
        }
    });
});
