from app import app,session,render_template,Items,flash,redirect,Checkout,Orders,dt,db
@app.route('/cart',methods=['post','get'])
def cart():
    cart_items = session.get('cart',[])
    total_price = 0
    for i in cart_items: 
        total_price += i['price']
    return render_template('cart.html',cart_items=cart_items,total_price=round(total_price,2))     
            
@app.route('/add_to_cart/<int:item_id>', methods=['GET','POST'])
def add_to_cart(item_id):
    cart_items = session.get('cart',[])
    item = Items.query.get(item_id)
    cart_items.append({
        'id':item.id,
        'name':item.id,
        'description': f'Weigh of the item: {item.chargeable_weight}',
        'weight': item.chargeable_weight,
        'price':item.chargeable_weight,
    })
    flash('Item added to Cart','success')
    return redirect('/cart')

@app.route('/remove_from_cart/<int:item_id>', methods=['GET','POST'])
def remove_from_cart(item_id):
    cart_items = session.get('cart', [])
    updated_cart_items = [item for item in cart_items if item['id'] != item_id]
    session['cart'] = updated_cart_items
    flash('Item removed from Cart', 'success')
    return redirect('/cart')

@app.route('/checkout')
def checkout():
    cart_items = session.get('cart',[])
    total_price = 0
    total_weight = 0
    items_count = 0
    for i in cart_items: 
        total_price += i['price']
        items_count += 1
    checkout_form = Checkout()

    if checkout_form.validate_on_submit(): 
        new_order = Orders(
            date_create = str(dt.now()),
            first_name = checkout_form.first_name.data, 
            last_name = checkout_form.last_name.data, 
            phone = checkout_form.phone.data, 
            shipping_address = checkout_form.address.data,
            order_total = total_price, 
            order_weight = None, 
            payment_method = checkout_form.first_name.data, 
            city = checkout_form.city.data, 
            username=checkout_form.username.data, 
            items = None, 
        )
        db.session.add(new_order)
        db.session.commit()
    return render_template('checkout.html',cart_items=cart_items, total_price=round(total_price,2),items_count=items_count,form = checkout_form)
