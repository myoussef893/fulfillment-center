from app import app,render_template,Items,ItemsForm,redirect,db,dt,math 

@app.route('/items',methods=['get','post'])
def view_items(): 
    items = Items.query.all()
   
    return render_template('items.html',id=items)

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
            quantity = 1,
            
        )
        db.session.add(new_item)
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