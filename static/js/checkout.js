var form = document.getElementById('form')

// Catch the shipping details form submission and handle it
form.addEventListener('submit', function(e){
    // Prevent the default
    e.preventDefault()
    // Testing
    console.log('Form submitted')
    // Hide the shipping form submit button
    document.getElementById('form-button').classList.add('hidden')
    // Show payment options section ready to pay
    document.getElementById('payment-info').classList.remove('hidden')
})