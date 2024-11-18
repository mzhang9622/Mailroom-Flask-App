/* FOR CONFIRMING DELETION of ADMIN */
const deleteAdmin = document.querySelectorAll('.remove-form');
deleteAdmin.forEach(form => {
    form.addEventListener('submit', confirmDelete);
});

function confirmDelete(event) {
    event.preventDefault();

    const isConfirmed = confirm("Do you want to delete this admin?");

    if (isConfirmed) {
        event.target.submit(); 
    }
}

/* FOR SCROLLING */
window.onbeforeunload = function() {
    sessionStorage.setItem('scroll_pos', window.scrollY);
};

window.onload = function() {
    const scroll_pos = sessionStorage.getItem('scroll_pos');
    
    if (scroll_pos)
    {
        window.scrollTo(0, scroll_pos);
    }
};


/* TO ALLOW USERS TO SEE PASSWORDS TYPED */
function togglePassword() {
    const show_button = document.querySelector('#show-password');
    const show_password_icon = show_button.querySelector('img');
    const password_input = document.querySelector('.password-input-text');


        show_button.addEventListener('click', function() {
        if (password_input.type === 'password') {
            password_input.type = 'text';
            show_password_icon.src = './static/images/eye-regular.svg';
        } else {
            password_input.type = 'password';
            show_password_icon.src = './static/images/eye-slash-regular.svg';
        }
    });

}
togglePassword();
