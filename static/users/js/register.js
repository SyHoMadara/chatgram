function register(event) {
    var password = document.getElementById('password').value;
    var confirmPassword = document.getElementById('confirmPassword').value;
    if (password !== confirmPassword) {
        event.preventDefault();
        document.getElementById('passwordError').style.display = 'block';
        return false;
    } else {
        document.getElementById('passwordError').style.display = 'none';
        return true;
    }
}

document.getElementById('registerForm').addEventListener('submit', register);

document.getElementById('registerForm').addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        if (register(event)) {
            document.getElementById('registerForm').submit();
        }
    }
});
