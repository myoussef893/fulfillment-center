from app import app,render_template,Items,ItemsForm,redirect,db,dt,math
from cart import stripe

stripe.api_key= 'sk_test_51NGN0CAa8vXaWUE9tisrczMe1enBRKQADGy7rDhyxisvisaujTI9l00nQQgVnHzOltMT1UE7nMLOgesK9xBfoHLg00eeQMcWdp'

@app.route('/items',methods=['get','post'])
def view_items(): 
    items = Items.query.all()
   
    return render_template('items.html',id=items)

def s_function(fetched_item): 
    product = stripe.Product.create(
        name = f"Item Number: {fetched_item.id}",
        description= f"Item:{fetched_item.id},\n Weight: {fetched_item.chargeable_weight},\n Tracking: {fetched_item.tracking_number}",
    )
    stripe.Price.create(
        currency='usd',
        unit_amount = int((fetched_item.chargeable_weight*27)*100),
        product_data={'name':product['name']},
    )
    return product.id


# This Function is to add a new item to the database. 
@app.route('/items/scan_item',methods=['get','post'])
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
            quantity = 1
        )

        db.session.add(new_item)
        db.session.commit()
        striper =s_function(new_item)
        updated_item = db.get_or_404(Items,new_item.id)
        updated_item.stripe_id = striper
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