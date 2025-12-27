from flask import Blueprint, render_template, request, session, jsonify

main_bp = Blueprint('main', __name__)

# Вибірка товарів
PRODUCTS = [
    {'id': 1, 'name': 'Пиця Маргарита', 'category': 'Піца', 'price': 250, 'image': 'pizza1.jpg'},
    {'id': 2, 'name': 'Пиця Пепероні', 'category': 'Піца', 'price': 280, 'image': 'pizza2.jpg'},
    {'id': 3, 'name': 'Бургер Класичний', 'category': 'Бургери', 'price': 180, 'image': 'burger1.jpg'},
    {'id': 4, 'name': 'Бургер Де Люкс', 'category': 'Бургери', 'price': 220, 'image': 'burger2.jpg'},
    {'id': 5, 'name': 'Паста Карбонара', 'category': 'Паста', 'price': 200, 'image': 'pasta1.jpg'},
    {'id': 6, 'name': 'Паста Болоньєзе', 'category': 'Паста', 'price': 210, 'image': 'pasta2.jpg'},
    {'id': 7, 'name': 'Салат Цезар', 'category': 'Салати', 'price': 150, 'image': 'salad1.jpg'},
    {'id': 8, 'name': 'Салат Грецький', 'category': 'Салати', 'price': 160, 'image': 'salad2.jpg'},
    {'id': 9, 'name': 'Кола 500ml', 'category': 'Напої', 'price': 50, 'image': 'cola.jpg'},
    {'id': 10, 'name': 'Сік Апельсиновий', 'category': 'Напої', 'price': 60, 'image': 'juice.jpg'},
]

CATEGORIES = ['Піца', 'Бургери', 'Паста', 'Салати', 'Напої']

@main_bp.route('/')
def index():
    cart = session.get('cart', [])
    return render_template('index.html', products=PRODUCTS, categories=CATEGORIES, cart_count=len(cart))

@main_bp.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = calculate_total(cart)
    return render_template('cart.html', cart=cart, total=total)

@main_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    cart = session.get('cart', [])
    
    # Знайти товар
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        # Перевірити чи товар уже в кошику
        cart_item = next((item for item in cart if item['id'] == product_id), None)
        if cart_item:
            cart_item['quantity'] += quantity
        else:
            cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
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
    return render_template('checkout.html', cart=cart, total=total)

@main_bp.route('/place-order', methods=['POST'])
def place_order():
    data = request.json
    cart = session.get('cart', [])
    total = calculate_total(cart)
    
    # Тут можна додати логіку для зберігання замовлення
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
    
    # Очистити кошик
    session['cart'] = []
    session.modified = True
    
    return jsonify({'success': True, 'order': order})

def calculate_total(cart):
    return sum(item['price'] * item['quantity'] for item in cart)
