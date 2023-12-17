var form = document.getElementById("form");
var csrftoken = form.getElementsByTagName("input")[0].value;

// Event Listeners

// Catch the shipping details form submission and handle it
form.addEventListener("submit", function(e){
    // Prevent the default
    e.preventDefault();
    // Hide the shipping form submit button
    document.getElementById("form-button").classList.add("hidden");
    // Show payment options section ready to pay
    document.getElementById("payment-info").classList.remove("hidden");
});

document.getElementById("make-payment").addEventListener("click", function(e){
    submitFormData();
});

// Logic to submit form
function submitFormData() {
    // User form
    var userFormData = {
        "email":null,
        "name":null,
        "total":total
    };

    // Shipping address form
    var shippingInfo = {
        "address": form.address.value,
        "city": form.city.value,
        "country": form.country.value,
        "county": form.county.value,
        "postcode": form.postcode.value
    };

    var url = "/process_order/";
    userFormData.name = form.name.value;
    userFormData.email = form.email.value;

    // fetch api to send data for order completion
    fetch(url, {
        body:JSON.stringify({"form":userFormData, "shipping":shippingInfo}),
        headers:{
            "Content-Type":"application/json",
            "X-CSRFToken":csrftoken
        },
        method:"POST"
    })

    .then((response) => response.json())

    .then((data) => {
        alert("Transaction completed");
        window.location.href = "/";
    });
}