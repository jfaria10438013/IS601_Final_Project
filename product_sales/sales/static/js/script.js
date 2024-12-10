// Function to get the CSRF token (needed for POST requests in Django)
function getCSRFToken() {
    let csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return csrfToken;
}

document.addEventListener('DOMContentLoaded', function() {
    // Function to clear filters
    function clearAllFilters(e) {
        e.preventDefault(); // prevents default behavior and allows to actually reload

        const url = new URL(window.location.href);
        url.searchParams.delete('search'); // Remove search
        url.searchParams.delete('price');  // Remove price filter
        url.searchParams.delete('category'); // Remove category filter

        window.location.href = url.toString(); // Redirect to the new URL without filters
    }

    // Add event listener to the "Clear Filters" button
    const clearButton = document.querySelector('.clear-filters-btn');
    if (clearButton) {
        clearButton.addEventListener('click', clearAllFilters);
    }
});

function updateCartDisplay() {

    // Update total cart count on navbar 
    fetch(`http://127.0.0.1:8000/get_cart_count/`)
        .then(response => response.json())
        .then(data => {
            let cartItemCount = data.cart_item_count;

            let cartCountElement = document.getElementById('cart-count');
            if (cartCountElement){
                cartCountElement.textContent = `Items in cart: ${cartItemCount}`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

    
    

    fetch(`http://127.0.0.1:8000/get_cart_total/`)
        .then(response => response.json())
        .then(data => {
            let totalElement = document.getElementById('total-price');
            if (totalElement){
                totalElement.textContent = `Total: $${data.total}`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

document.addEventListener('DOMContentLoaded', updateCartDisplay);

function decCount(itemId) {
    // Get the current count displayed on the page
    let currentCount = parseInt(document.getElementById(`${itemId}`).textContent);

    // Increment the count
    if(currentCount>0){
    let newCount = currentCount - 1;

    // Send the new count to the server using an AJAX request
    fetch(`http://127.0.0.1:8000/update_count/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // CSRF token for Django security
        },
        body: JSON.stringify({ 'count': newCount }) // Sending the new count
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the count on the frontend
            document.getElementById(`${itemId}`).textContent = newCount;

            // Also decrease the total cart count
            updateCartDisplay();
        } else {
            alert('Failed to update count.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
    /*
    if (newCount <= 0){
        removeFromCart(itemId);
    }*/
}
}

// Function to update the count
function incCount(itemId) {
    // Get the current count displayed on the page
    let currentCount = parseInt(document.getElementById(`${itemId}`).textContent);

    // Increment the count
    let newCount = currentCount + 1;

    // Send the new count to the server using an AJAX request
    fetch(`http://127.0.0.1:8000/update_count/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // CSRF token for Django security
        },
        body: JSON.stringify({ 'count': newCount }) // Sending the new count
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the count on the frontend
            document.getElementById(`${itemId}`).textContent = newCount;

            // Also increase the total cart count
            updateCartDisplay();
        } else {
            alert('Failed to update count.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function removeFromCart(itemId) {
    // Find the item's container element by ID
    let itemElement = document.getElementById(`item-${itemId}`);
    
    if (itemElement) {
        resetCount(itemId);
        // Remove the element from the DOM
        itemElement.remove();
        //updateCartDisplay();
    } else {
        console.error(`Item with ID ${itemId} not found in the cart.`);
    }
}

function resetCount(itemId) {
    // Send a request to the server to reset the count to zero for the item
    fetch(`http://127.0.0.1:8000/reset_count/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // CSRF token for Django security
        },
        body: JSON.stringify({ 'count': 0 }) // Sending the new count
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the count on the frontend
            //document.getElementById(`${itemId}`).textContent = 0;

            // Also decrease the total cart count
            updateCartDisplay();
        } else {
            alert('Failed to update count.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


function resetAll(itemId) {
    // Send a request to the server to reset the count to zero for the item
    fetch(`http://127.0.0.1:8000/reset_count/${itemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),  // Ensure you have CSRF token for Django
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // If successful, reset the count in the frontend as well
            document.getElementById(`${itemId}`).textContent = "0";
        } else {
            alert('Failed to reset count.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function resetAllCounts() {

    // Send a request to the server to reset the counts for all items
    fetch('http://127.0.0.1:8000/reset_all_counts/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),  // CSRF token for Django security
        }
    })
    .then(response => response.json())
    .catch(error => {
        console.error('Error:', error);
    });
}