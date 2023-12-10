// Get all buttons that update cart state identified using class update-cart
var btnsThatUpdate = document.getElementsByClassName('update-cart')


for (i = 0; i < btnsThatUpdate.length; i++) {
    // Add event listeners to btns and gather btn data
    btnsThatUpdate[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        console.log('USER', user)

        // Handle user cart update actions based on logged in status
        if(user === 'AnonymousUser'){
            console.log('Not logged In')
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    console.log('User is logged in, sending data')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) =>{
        console.log('data: ', data)
        location.reload()
    })
}