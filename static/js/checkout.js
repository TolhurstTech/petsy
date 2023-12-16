var form = document.getElementById('form')
csrftoken = form.getElementsByTagName("input")[0].value

// Event Listeners

// Catch the shipping details form submission and handle it
form.addEventListener('submit', function(e){
    // Prevent the default
    e.preventDefault()
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

    if (user == 'AnonymousUser'){
        userFormData.name = form.name.value
        userFormData.email = form.email.value
    }

    var url = '/process_order/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'form':userFormData, 'shipping':shippingInfo}),
    })

    .then((response) => response.json())

    .then((data) => {
        alert('Transaction completed');
        window.location.href = "/"
    })
}