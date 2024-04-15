from app import app,session,render_template,Items,flash,redirect

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