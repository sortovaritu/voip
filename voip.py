import logging


from logging.handlers import RotatingFileHandler



from flask import Flask, url_for, render_template, request, redirect, flash, logging


import voip_db, forms


app = Flask(__name__,static_folder='bootstrap')
app.secret_key = 'epam'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('sub_db.html',)
    else:
        return render_template('sub_db.html',name='Name')






@app.route('/subscribers', methods=['POST', 'GET'])
def sub_db():
    if request.method == 'GET':
        return render_template('sub_db.html',)
    else:
        Database = voip_db.VoIP_DB()
        user_name = request.form['SearchName']
        app.logger.info( 'Search Name Request: ' + user_name )
        try:
            tbl = Database.Get_Sub_By_Name(user_name)
            return render_template('sub_db.html',name='Name',rows=tbl)
        except Exception:
            flash('[voip_db.py]: Communication with Database failed')
            return redirect('/subscribers', code=303)






@app.route('/subscribers/edit/<sid>', methods=['POST', 'GET'])
def edit_sub(sid):
    form = forms.SubEditForm(request.form)
    Database = voip_db.VoIP_DB()
    rows = Database.Get_Sub_By_ID(sid)                                                                  #Get sunscriber info by ID
    Locations = Database.Get_Locations()
    if request.method == 'GET':                                                                #Get list of Locations
        form.location.choices = [(l[0],l[1]) for l in Locations]          #Fill list of locations to SelectField 
        form.location.default = rows[0][3]                                                                  #Chose user Location from list of locations in SelectField
        form.process()        
        form.sub_id.data = sid                                                                              #Get User ID (static field)
        form.username.data = rows[0][1]                                                                     #Get UserName
        form.extension.data = rows[0][2]
        form.password.data = rows[0][4]
        form.vmpassword.data = rows[0][5]
        form.privateline.data = rows[0][6]
        form.pmc_id.data = rows[0][7]

    if request.method == 'POST':
        form.location.choices = [(l[0],l[1]) for l in Locations]          #Fill list of locations to SelectField 
        if form.validate():
            Database.Update_Sub(form)
            flash('Updated Successfully')
            return redirect('/subscribers')
        else:
            form.accept_changes.data = False                                #Reset Accept changes checkbox
            print form.location.data

    return render_template('edit_sub.html',name='Name',form=form)



@app.route('/subscribers/add', methods=['POST', 'GET'])
def add_sub():
    form = forms.SubAddForm(request.form)
    Database = voip_db.VoIP_DB()                                                                #Get sunscriber info by ID
    Locations = Database.Get_Locations()
    if request.method == 'POST':
        form.location.choices = [(l[0],l[1]) for l in Locations]          #Fill list of locations to SelectField 
        if form.validate():
            flash('Added Successfully')
            return redirect('/subscribers')
        else:
            form.accept_changes.data = False                                #Reset Accept changes checkbox
            print form.location.data

    return render_template('edit_sub.html',name='Name',form=form)



@app.route('/locations', methods=['POST', 'GET'])
def locations():
    Database = voip_db.VoIP_DB()
    return render_template('locations.html',rows=Database.Get_Locations_List())




if __name__ == '__main__':
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('foo.log', maxBytes=10000000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0',debug=True)
raw_input()