from flask import Blueprint, render_template, request, session, jsonify

main_bp = Blueprint('main', __name__)

PRODUCTS = [
    {'id': 1, 'name': 'Margherita Pizza', 'category': 'Pizza', 'price': 250, 'image': 'https://source.unsplash.com/800x600/?margherita,pizza'},
    {'id': 2, 'name': 'Pepperoni Pizza', 'category': 'Pizza', 'price': 280, 'image': 'https://source.unsplash.com/800x600/?pepperoni,pizza'},
    {'id': 3, 'name': 'Classic Burger', 'category': 'Burgers', 'price': 180, 'image': 'https://source.unsplash.com/800x600/?classic,burger'},
    {'id': 4, 'name': 'Deluxe Burger', 'category': 'Burgers', 'price': 220, 'image': 'https://source.unsplash.com/800x600/?deluxe,burger'},
    {'id': 5, 'name': 'Carbonara Pasta', 'category': 'Pasta', 'price': 200, 'image': 'https://source.unsplash.com/800x600/?carbonara,pasta'},
    {'id': 6, 'name': 'Bolognese Pasta', 'category': 'Pasta', 'price': 210, 'image': 'https://source.unsplash.com/800x600/?bolognese,pasta'},
    {'id': 7, 'name': 'Caesar Salad', 'category': 'Salads', 'price': 150, 'image': 'https://source.unsplash.com/800x600/?caesar,salad'},
    {'id': 8, 'name': 'Greek Salad', 'category': 'Salads', 'price': 160, 'image': 'https://source.unsplash.com/800x600/?greek,salad'},
    {'id': 9, 'name': 'Cola 500ml', 'category': 'Drinks', 'price': 50, 'image': 'https://source.unsplash.com/800x600/?cola,soda'},
    {'id': 10, 'name': 'Orange Juice', 'category': 'Drinks', 'price': 60, 'image': 'https://source.unsplash.com/800x600/?orange,juice'},
]

CATEGORIES = ['Pizza', 'Burgers', 'Pasta', 'Salads', 'Drinks']

# Remote images for payment methods (can be Google-hosted or other URLs)
PAYMENT_IMAGES = {
    'apple': 'https://upload.wikimedia.org/wikipedia/commons/b/b9/Apple_logo.svg',
    'google': 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg',
    'card': 'https://cdn.pixabay.com/photo/2016/03/31/19/56/credit-card-1294149_640.png',
    'cash': 'https://cdn.pixabay.com/photo/2016/03/31/19/56/money-1294148_640.png'
}

@main_bp.route('/')
def index():
    cart = session.get('cart', [])
    return render_template('index.html', products=PRODUCTS, categories=CATEGORIES, cart_count=len(cart), payment_images=PAYMENT_IMAGES)

@main_bp.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = calculate_total(cart)
    return render_template('cart.html', cart=cart, total=total, payment_images=PAYMENT_IMAGES)

@main_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    cart = session.get('cart', [])
    
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        cart_item = next((item for item in cart if item['id'] == product_id), None)
        if cart_item:
            cart_item['quantity'] += quantity
        else:
            cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'image': product.get('image'),
                'quantity': quantity
            })
        session['cart'] = cart
        session.modified = True
        
    return jsonify({'success': True, 'cart_count': len(cart)})

@main_bp.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    data = request.json
    product_id = data.get('product_id')
    
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    session.modified = True
    
    return jsonify({'success': True, 'cart_count': len(cart)})

@main_bp.route('/update-quantity', methods=['POST'])
def update_quantity():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    cart = session.get('cart', [])
    for item in cart:
        if item['id'] == product_id:
            item['quantity'] = max(1, quantity)
    
    session['cart'] = cart
    session.modified = True
    total = calculate_total(cart)
    
    return jsonify({'success': True, 'total': total})

@main_bp.route('/checkout')
def checkout():
    cart = session.get('cart', [])
    total = calculate_total(cart)
    return render_template('checkout.html', cart=cart, total=total, payment_images=PAYMENT_IMAGES)

@main_bp.route('/place-order', methods=['POST'])
def place_order():
    data = request.json
    cart = session.get('cart', [])
    total = calculate_total(cart)
    
    # Here you can add logic to persist the order
    order = {
        'items': cart,
        'total': total,
        'delivery': data.get('delivery'),
        'payment': data.get('payment'),
        'name': data.get('name'),
        'phone': data.get('phone'),
        'address': data.get('address'),
        'notes': data.get('notes', '')
    }
    
    # Clear the cart
    session['cart'] = []
    session.modified = True
    
    return jsonify({'success': True, 'order': order})

def calculate_total(cart):
    return sum(item['price'] * item['quantity'] for item in cart)
