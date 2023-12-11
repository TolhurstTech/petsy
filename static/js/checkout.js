var form = document.getElementById('form')
var total = '{{ order.get_cart_total|floatFormat:2 }}'

// Hide name and email fields if user is logged in
if (user != 'AnonynousUser'){
    
    document.getElementById('user-info').innerHTML = ''
}

// Event Listeners

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

document.getElementById('make-payment').addEventListener('click', function(e){
    submitFormData()
})

// Logic to submit form
function submitFormData() {
    console.log('Payment button clicked')

    var userFormData = {
        'name':null,
        'email':null,
        'total':total,
    }

    var shippingInfo = {
        'address': form.address.value,
        'city': form.city.value,
        'county': form.county.value,
        'postcode': form.postcode.value,
        'country': form.country.value,
    }
    console.log(shippingInfo.address)

    if (user == 'AnonymousUser'){
        userFormData.name = form.name.value
        userFormData.email = form.email.value
    }
}