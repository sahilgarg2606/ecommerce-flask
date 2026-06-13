import os
from flask import Flask, render_template, redirect, url_for, session, flash

app = Flask(__name__)
# In production, this should be an environment variable
app.secret_key = os.environ.get("SECRET_KEY", "devops_super_secret_key_12345")

# Mock Product Database (Stateless / Immutable)
PRODUCTS = {
    1: {"id": 1, "name": "Cloud Native Hoodie", "price": 49.99, "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500", "desc": "Perfect for late-night on-call shifts."},
    2: {"id": 2, "name": "Kubernetes Mug", "price": 19.99, "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=500", "desc": "Holds 12 rules of microservices and 16oz of coffee."},
    3: {"id": 3, "name": "CI/CD Pipeline Sticker Pack", "price": 4.99, "image": "https://images.unsplash.com/photo-1572375995301-45a6b30f054a?w=500", "desc": "Guaranteed to make your laptop build faster."},
    4: {"id": 4, "name": "Production Deploy Button", "price": 99.99, "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500", "desc": "Smash in case of emergency. Or on Fridays."},
}

@app.route('/')
def index():
    # Adding an environment variable check to easily test configuration injection in DevOps pipelines
    env_name = os.environ.get("APP_ENV", "Development")
    return render_template('index.html', products=PRODUCTS.values(), env_name=env_name)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if product_id not in PRODUCTS:
        flash("Product not found!", "error")
        return redirect(url_for('index'))
    
    if 'cart' not in session:
        session['cart'] = {}
        
    cart = session['cart']
    pid_str = str(product_id)
    
    if pid_str in cart:
        cart[pid_str] += 1
    else:
        cart[pid_str] = 1
        
    session['cart'] = cart
    flash(f"Added {PRODUCTS[product_id]['name']} to cart!", "success")
    return redirect(url_for('index'))

@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0.0
    
    for pid_str, quantity in cart.items():
        pid = int(pid_str)
        if pid in PRODUCTS:
            item = PRODUCTS[pid].copy()
            item['quantity'] = quantity
            item['subtotal'] = item['price'] * quantity
            total += item['subtotal']
            cart_items.append(item)
            
    return render_template('cart.html', cart_items=cart_items, total=round(total, 2))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash("Cart cleared.", "info")
    return redirect(url_for('view_cart'))

@app.route('/checkout', methods=['POST'])
def checkout():
    session.pop('cart', None)
    flash("Order placed successfully! (DevOps Mock Checkout)", "success")
    return redirect(url_for('index'))

@app.route('/health')
def health():
    # Essential endpoint for Kubernetes probes or AWS Target Group health checks
    return {"status": "healthy", "version": "1.0.0"}, 200

if __name__ == '__main__':
    # Bind to 0.0.0.0 to make it accessible outside a Docker container
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)