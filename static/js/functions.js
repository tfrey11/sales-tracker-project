const eventbtn = document.querySelector('#login-form-submit');

eventbtn.addEventListener('click', () => {
    alert('Welcome, you are now logged in!')
});


const createbtn = document.querySelector('#new-user-submit');

createbtn.addEventListener('click', () => {
    alert('Account created, please log in.')
});

const logoutbtn = document.querySelector('#logout-btn');

logoutbtn.addEventListener('click', () => {
    alert('You have been logged out. Goodbye.')
});