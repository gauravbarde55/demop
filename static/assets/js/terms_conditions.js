// Get elements
const popup = document.getElementById('popup');
const openPopup = document.getElementById('openPopup');
const closePopup = document.getElementById('closePopup');
const acceptBtn = document.getElementById('acceptBtn');
const checkbox = document.getElementById('tandc');

// Open the popup when the button is clicked
openPopup.onclick = function() {
    popup.style.display = 'block';
}

// Close the popup when the close button is clicked
closePopup.onclick = function() {
    popup.style.display = 'none';
}

// Close the popup when clicking outside of the popup content
window.onclick = function(event) {
    if (event.target === popup) {
        popup.style.display = 'none';
    }
}

// Enable the Accept button when the checkbox is checked
checkbox.onchange = function() {
    acceptBtn.disabled = !this.checked;
}

// Handle the Accept button click
acceptBtn.onclick = function() {
    alert('You have accepted the terms and conditions!');
    popup.style.display = 'none'; // Close the popup after acceptance
}
