from flask import render_template, session, redirect, url_for, request, abort, flash
from flask_login import current_user, login_required

from shopping import app
from shopping.models import Product


@app.route('/')
def index():
    products = Product.query.filter_by(available=True).all()
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)


@app.route('/carrinho')
def cart():
    cart = session.get('cart', {})
    products = Product.query.filter(Product.id.in_(cart.keys())).all()

    total = 0
    for product in products:
        product_id = str(product.id)
        if product_id in cart:
            item = cart[product_id]
            total += product.price * item['quantity']

    return render_template('cart.html', products=products, cart=cart, total=total)


@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))  # Garante que a quantidade seja um número inteiro

    # Recupera ou inicializa o carrinho na sessão
    cart = session.get('cart', {})

    # Verifica se o produto já está no carrinho
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += quantity
    else:
        # Se não estiver, cria a entrada para o produto
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),  # Converte o preço para float
            'quantity': quantity
        }

    session['cart'] = cart  # Atualiza o carrinho na sessão

    return redirect(url_for('index'))


@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})

    # Calcula o total do carrinho
    total_price = 0
    for item in cart.values():
        total_price += item['price'] * item['quantity']

    # Passa o carrinho e o total para o template
    return render_template('checkout.html', cart=cart, total_price=total_price)


@app.route('/place_order', methods=['POST'])
def place_order():
    cart = session.get('cart', {})
    if not cart:
        flash("O carrinho está vazio.", "warning")
        return redirect(url_for('cart'))

    # Simula o início do processo de pagamento
    total_price = 0
    for item in cart.values():
        total_price += item['price'] * item['quantity']

    # Redireciona para a página de pagamento com o valor total do pedido
    return redirect(url_for('payment', total_price=total_price))


@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    # Aqui você pode adicionar a lógica de verificação de pagamento via PIX

    # Após a confirmação do pagamento, finalize o pedido
    session['cart'] = {}  # Limpa o carrinho
    flash("Pagamento confirmado e pedido realizado com sucesso!", "success")
    return redirect(url_for('index'))


@app.route('/payment')
def payment():
    total_price = request.args.get('total_price', type=float)

    # Renderiza a página onde o usuário escolhe a forma de pagamento
    return render_template('payment.html', total_price=total_price)


@app.route('/admin/products', methods=['GET', 'POST'])
@login_required
def manage_products():
    if not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        # Lógica para adicionar ou atualizar produtos
        pass

    products = Product.query.all()
    return render_template('admin_products.html', products=products)


@app.context_processor
def cart_info():
    cart = session.get('cart', {})
    total_items = sum(item['quantity'] for item in cart.values())
    return dict(total_items=total_items)
