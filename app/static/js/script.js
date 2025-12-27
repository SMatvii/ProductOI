function addToCart(productId) {
    const quantity = parseInt(document.querySelector(`#qty-${productId}`).value) || 1;
    
    fetch('/add-to-cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Товар додано в кошик! ✓');
            updateCartCount(data.cart_count);
        }
    })
    .catch(error => console.error('Error:', error));
}

function removeFromCart(productId) {
    if (confirm('Видалити товар з кошика?')) {
        fetch('/remove-from-cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    }
}

function updateQuantity(productId) {
    const quantity = parseInt(document.querySelector(`#qty-${productId}`).value);
    
    if (quantity < 1) {
        document.querySelector(`#qty-${productId}`).value = 1;
        return;
    }
    
    fetch('/update-quantity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.querySelector('.summary-total').innerText = 
                `РАЗОМ: ${data.total} грн`;
            updateTotalPrice();
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateTotalPrice() {
    const total = Array.from(document.querySelectorAll('.item-price'))
        .reduce((sum, el) => {
            const quantity = parseInt(el.closest('.cart-item').querySelector('.item-quantity input').value);
            const price = parseInt(el.textContent);
            return sum + (price * quantity);
        }, 0);
    
    document.querySelector('.summary-total').innerHTML = 
        `<span>РАЗОМ:</span><span>${total} грн</span>`;
}

function updateCartCount(count) {
    const cartCount = document.querySelector('.cart-count');
    if (cartCount) {
        cartCount.textContent = count;
    }
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #10b981;
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

function filterByCategory(category) {
    const buttons = document.querySelectorAll('.category-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    if (category === 'all') {
        document.querySelectorAll('.product-card').forEach(card => {
            card.style.display = 'block';
        });
    } else {
        const button = Array.from(buttons).find(btn => btn.textContent === category);
        if (button) button.classList.add('active');
        
        document.querySelectorAll('.product-card').forEach(card => {
            const cardCategory = card.querySelector('.product-category').textContent;
            card.style.display = cardCategory === category ? 'block' : 'none';
        });
    }
}

function placeOrder(event) {
    event.preventDefault();
    
    const name = document.querySelector('input[name="name"]').value;
    const phone = document.querySelector('input[name="phone"]').value;
    const address = document.querySelector('input[name="address"]').value;
    const notes = document.querySelector('textarea[name="notes"]').value;
    const delivery = document.querySelector('input[name="delivery"]:checked').value;
    const payment = document.querySelector('input[name="payment"]:checked').value;
    
    if (!name || !phone || !address) {
        alert('Будь ласка, заповніть усі обов\'язкові поля!');
        return;
    }
    
    fetch('/place-order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            phone: phone,
            address: address,
            notes: notes,
            delivery: delivery,
            payment: payment
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showOrderConfirmation(data.order);
        }
    })
    .catch(error => console.error('Error:', error));
}

function showOrderConfirmation(order) {
    const html = `
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0,0,0,0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2000;
        ">
            <div style="
                background: white;
                padding: 2rem;
                border-radius: 15px;
                max-width: 500px;
                width: 90%;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            ">
                <h2 style="color: #7c3aed; margin-bottom: 1rem;">✓ Замовлення прийнято!</h2>
                <p style="margin-bottom: 1rem; color: #6b7280;">
                    Дякуємо за ваше замовлення, ${order.name}!
                </p>
                <p style="margin-bottom: 2rem; color: #6b7280;">
                    Ми скоро зв'яжемось з вами на номер ${order.phone}
                </p>
                <p style="font-size: 1.2rem; color: #7c3aed; font-weight: bold; margin-bottom: 2rem;">
                    Сума: ${order.total} грн
                </p>
                <button onclick="window.location.href='/'" style="
                    background-color: #7c3aed;
                    color: white;
                    padding: 0.8rem 2rem;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 600;
                    font-size: 1rem;
                ">Повернутись на головну</button>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', html);
}

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.quantity-control').forEach(control => {
        const decreaseBtn = control.querySelector('.qty-btn:first-child');
        const quantityInput = control.querySelector('.quantity');
        const increaseBtn = control.querySelector('.qty-btn:last-child');
        
        if (decreaseBtn && quantityInput && increaseBtn) {
            decreaseBtn.addEventListener('click', () => {
                const current = parseInt(quantityInput.value);
                if (current > 1) quantityInput.value = current - 1;
            });
            
            increaseBtn.addEventListener('click', () => {
                const current = parseInt(quantityInput.value);
                quantityInput.value = current + 1;
            });
        }
    });
});

