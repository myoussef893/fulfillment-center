from app import app,session,render_template,Items,flash,redirect,Checkout,Orders,dt,db,url_for,current_user
from random import randint

exchange_rate = 50

@app.route('/cart',methods=['post','get'])
def cart():
    cart_items = session.get('cart',[])
    total_price = 0
    cart_count = 0
    for i in cart_items: 
        total_price += i['price']
        cart_count += 1
    return render_template('cart.html',cart_items=cart_items,total_price=round(total_price,2),items_count =cart_count)     
            
@app.route('/add_to_cart/<int:item_id>', methods=['GET','POST'])
def add_to_cart(item_id):
    cart_items = session.get('cart',[])
    item = Items.query.get(item_id)
    cart_items.append({
        'id':item.id,
        'name':item.id,
        'description': f'Weigh of the item: {item.chargeable_weight}',
        'weight': item.chargeable_weight,
        'price':float(item.chargeable_weight)*27,
    })
    item.quantity -= 1
    db.session.commit()
    flash('Item added to Cart','success')
    return redirect('/dashboard')

@app.route('/remove_from_cart/<int:item_id>', methods=['GET','POST'])
def remove_from_cart(item_id):
    cart_items = session.get('cart', [])
    updated_cart_items = [item for item in cart_items if item['id'] != item_id]
    rtrn_quantity = Items.query.get(item_id)
    rtrn_quantity.quantity +=1
    db.session.commit()
    session['cart'] = updated_cart_items

    flash('Item removed from Cart', 'success')
    return redirect('/cart')

@app.route('/clear_cart')
def clear_cart(): 
    session['cart'] = []
    flash('The cart has been cleared, successfully','sucess')
    return redirect('/cart')


def payment_method_switcher(method): 
    if method == 'Bank Deposit' or 'Cash on Delivery': 
        pass
    else: 
        render_template('index.html')

@app.route('/checkout',methods=['GET','POST'])
def checkout():
    cart_items = session.get('cart',[])
    total_price = 0
    total_weight = 0
    items_count = 0
    for i in cart_items: 
        total_price += i['price']
        items_count += 1
        total_weight +=i['weight']
    checkout_form = Checkout()
    
    if checkout_form.validate_on_submit():
        pay_method = checkout_form.payment_method.data
        if pay_method == 'Cash On Delivery' or 'Bank Deposit':
            new_order = Orders(
                date_created = str(dt.now()),
                first_name = checkout_form.first_name.data, 
                last_name = checkout_form.last_name.data, 
                phone = checkout_form.phone.data, 
                shipping_address = checkout_form.address.data,
                order_total = total_price, 
                order_weight = total_weight, 
                payment_method = pay_method, 
                # inventory = current_user.inventory,
                city = checkout_form.city.data, 
                username=current_user.username,
                order_number = randint(1000,9999999999)
            )

            n = new_order.order_number
            print(n)
            db.session.add(new_order)
            db.session.commit()
            session['cart'] = []
            return render_template('success-order-confirmation.html',order = n)
        else: 
            return redirect('/')

    return render_template('checkout.html',cart_items=cart_items, total_price=round(total_price,2),items_count=items_count,form = checkout_form)

@app.route('/success')
def sucess_result(): 
    return render_template('success.html')



