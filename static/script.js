// script.js

// Function to fetch data from credentials.json and fill in the form placeholders
function fillFormPlaceholders() {
    fetch('credentials.json')
    .then(response => response.json())
    .then(data => {
        // Fill in form fields with data from JSON
        document.getElementById('fullName').setAttribute('placeholder', data.fullName);
        document.getElementById('eMail').setAttribute('placeholder', data.email);
        document.getElementById('phone').setAttribute('placeholder', data.phone);
        document.getElementById('website').setAttribute('placeholder', data.website);
        document.getElementById('Street').setAttribute('placeholder', data.street);
        document.getElementById('ciTy').setAttribute('placeholder', data.city);
        document.getElementById('sTate').setAttribute('placeholder', data.state);
        document.getElementById('zIp').setAttribute('placeholder', data.zip);
    })
    .catch(error => console.error('Error fetching credentials:', error));
}

// Call the function to fill form placeholders when the page loads
window.onload = fillFormPlaceholders;
