function showEmailInput() {
    const emailInput = document.getElementById('email-input');
    if (document.getElementById('gift-receiving-mail').checked) {
        emailInput.style.display = 'block';
    } else {
        emailInput.style.display = 'none';
    }
}

document.getElementById('gift-receiving-mail').onchange = showEmailInput;
document.getElementById('gift-receiving-contact').onchange = showEmailInput;
showEmailInput();
