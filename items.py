from app import app,render_template,Items,ItemsForm,redirect,db,dt,math,current_user,url_for,session,Orders

from flask_login import current_user

@app.route('/items', methods=['get', 'post'])
def view_items():
    if current_user.is_authenticated:  # Check if user is logged in

        items = Items.query.filter_by(username=current_user.username).all()
        return render_template('items_viewer.html', id=items)
    else:
        # Handle case where user is not logged in (e.g., redirect to login page)
        return redirect(url_for('login'))


# def s_function(fetched_item): 
#     product = stripe.Product.create(
#         name = f"Item Number: {fetched_item.id}",
#         description= f"Item:{fetched_item.id},\n Weight: {fetched_item.chargeable_weight},\n Tracking: {fetched_item.tracking_number}",
#     )
#     stripe.Price.create(
#         currency='usd',
#         unit_amount = int((fetched_item.chargeable_weight*27)*100),
#         product_data={'name':product['name']},
#     )
#     return product.id
# This Function is to add a new item to the database. 
@app.route('/scan_item',methods=['get','post'])
def scan_item():
    item_form = ItemsForm()
    if item_form.validate_on_submit():
        new_item = Items(
            tracking_number = item_form.tracking_number.data,
            source_country = item_form.scanning_country.data,
            receiving_date = str(dt.now()),
            measured_weight= item_form.item_weight.data,
            chargeable_weight = math.ceil(item_form.item_weight.data*10)/10,
            username = item_form.username.data,
            quantity = 1,
            status = item_form.status.data
        )

        db.session.add(new_item)
        db.session.commit()
        db.session.commit()

        return redirect('/items')
    return render_template('scan_item.html',form=item_form)

# This Funcion is to edit and existing item in database
@app.route('/dashboard/<int:id>/edit',methods=['GET',"POST"])
def edit_item(id):
    form = ItemsForm()
    item = db.get_or_404(Items,id)
    
    if form.validate_on_submit():
        item.tracking_number = form.tracking_number.data
        item.source_country =   form.scanning_country.data
        item.username = form.username.data
        db.session.commit()
        return redirect('/dashboard')
    else:
        return render_template('scan_item.html',form=form)

# This Function is to delete added items in database
@app.route('/items/<int:id>/delete')
def delete_item(id): 
    item = db.get_or_404(Items,id)
    db.session.delete(item)
    db.session.commit()
    return redirect('/items')


@app.route('/orders/')
def view_orders(): 
    if current_user.is_authenticated:
        orders = Orders.query.filter_by(username=current_user.username)
        return render_template('orders.html',orders = orders)
    else: 
        redirect('/login')
