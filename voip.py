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




#Controller for Subscribers page

@app.route('/subscribers', methods=['GET'])
def sub_db_get():
    return render_template('sub_db.html',)
        

@app.route('/subscribers', methods=['POST'])
def sub_db_post():
    Database = voip_db.VoIP_DB()
    user_name = request.form['SearchName']                                                          #get text from SearchName form
    app.logger.info( 'Search Name Request: ' + user_name )                          
    try:
        tbl = Database.Get_Sub_By_Name(user_name)                                                   #get list of founded subscribers 
        return render_template('sub_db.html',name='Name',rows=tbl)                                  #send list of founded subscribers to View
    except Exception:
        flash('[voip_db.py]: Communication with Database failed')                                   
        return redirect('/subscribers', code=303)                                                   #redirect to Subscribers page in case of exception



#Controller for Subscriber Edit page

@app.route('/subscribers/edit/<sid>', methods=['GET'])
def edit_sub_get(sid):
    app.logger.info( 'Edit Subscriber Page Request' )
    form = forms.SubEditForm(request.form)                                                          #create Form for edit subscriber
    Database = voip_db.VoIP_DB()
    try:    
        rows = Database.Get_Sub_By_ID(sid)                                                          #get sunscriber info by ID
        Locations = Database.Get_Locations()                                                        #get list of Locations
    except Exception:
        flash('[voip_db.py]: Communication with Database failed')                                   
        return redirect('/subscribers', code=303)                                                   #redirect to Subscribers page('GET' method) in case of exception  
    form.location.choices = [(l[0],l[1]) for l in Locations]                                        #fill list of locations to SelectField 
    form.location.default = rows[0][3]                                                              #chose user Location from list of locations in SelectField
    form.process()        
    form.sub_id.data = sid                                                                          #get User ID (static field)
    form.username.data = rows[0][1]                                                                 #get UserName
    form.extension.data = rows[0][2]                                                                #get User extension
    form.password.data = rows[0][4]                                                                 #get User password
    form.vmpassword.data = rows[0][5]                                                               #get User Vmpassword
    form.privateline.data = rows[0][6]                                                              #get User private line
    form.pmc_id.data = rows[0][7]                                                                   #get User pmc id
    return render_template('edit_sub.html',name='Name',form=form)

@app.route('/subscribers/edit/<sid>', methods=['POST'])
def edit_sub_post(sid):
    app.logger.info( 'Edit Subscriber Request: ID = ' + sid )
    form = forms.SubEditForm(request.form)                                                          #create Form for edit subscriber
    Database = voip_db.VoIP_DB()
    try:
        rows = Database.Get_Sub_By_ID(sid)                                                          #get sunscriber info by ID                                                         
        Locations = Database.Get_Locations()                                                        #get list of all locations
    except Exception:
        flash('[voip_db.py]: Communication with Database failed')                                   
        return redirect('/subscribers', code=303)                                                   #redirect to Subscribers page('GET' method) in case of exception           
    form.location.choices = [(l[0],l[1]) for l in Locations]                                        #fill list of locations to SelectField 
    if form.validate():                                                                             #form validation
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



@app.route('/locations/edit/<lid>', methods=['GET'])
def edit_loc_get(lid):
    app.logger.info( 'Edit Location Request: ID = ' + lid )
    form = forms.LocEditForm(request.form)                                                          #create Form for edit subscriber
    Database = voip_db.VoIP_DB()
    try:    
        rows = Database.Get_Location_By_ID(lid) 
        PBXs = Database.Get_PBX()                                                                                                
    except Exception:
        flash('[voip_db.py]: Communication with Database failed')                                   
        return redirect('/locations', code=303)                                                   #redirect to Subscribers page('GET' method) in case of exception  
    form.pbx.choices = [(l[0],l[1]) for l in PBXs]
    form.pbx.default = rows[0][2]
    form.process()
    form.loc_id.data = lid
    form.location.data = rows[0][1]
    form.info.data = rows[0][3]
    return render_template('edit_loc.html',form = form)



@app.route('/locations/edit/<lid>', methods=['POST'])
def edit_loc_post(lid):
    app.logger.info( 'Save Changes Edit Location Request: ID = ' + lid )
    form = forms.LocEditForm(request.form)                                                          #create Form for edit subscriber
    Database = voip_db.VoIP_DB()
    try:    
        rows = Database.Get_Location_By_ID(lid) 
        PBXs = Database.Get_PBX()                                                                                                
    except Exception:
        flash('[voip_db.py]: Communication with Database failed')                                   
        return redirect('/locations', code=303)                                                   #redirect to Subscribers page('GET' method) in case of exception  
    form.pbx.choices = [(l[0],l[1]) for l in PBXs]
    if form.validate():                                                                             #form validation
        app.logger.info( 'Save Changes Edit Location Request: ID = ' + lid +'OK')
        Database.Update_Loc(form)
        flash('Updated Successfully')
        return redirect('/locations')
    else:
        app.logger.info( 'Save Changes Edit Location Request: ID = ' + lid +' Form is not valid')

    return render_template('edit_loc.html',form = form)




@app.route('/locations/add', methods=['GET'])
def add_loc_get():
    app.logger.info( 'Add Location Request: ID' )
    form = forms.LocAddForm(request.form)                                                          #create Form for edit subscriber
    Database = voip_db.VoIP_DB()
    try:    
        PBXs = Database.Get_PBX()                                                                                                
    except Exception:
        flash('[voip_db.py]: Communication with Database failed')                                   
        return redirect('/locations', code=303)                                                   #redirect to Subscribers page('GET' method) in case of exception  
    form.pbx.choices = [(l[0],l[1]) for l in PBXs]
    form.process()
    return render_template('add_loc.html',form = form)


@app.route('/locations/add', methods=['POST'])
def add_loc_post():
    app.logger.info( 'Save Changes Add Location Request: ID' )
    form = forms.LocAddForm(request.form)                                                          #create Form for edit subscriber
    Database = voip_db.VoIP_DB()
    try:    
        PBXs = Database.Get_PBX()                                                                                                
    except Exception:
        flash('[voip_db.py]: Communication with Database failed')                                   
        return redirect('/locations', code=303)                                                   #redirect to Subscribers page('GET' method) in case of exception  
    form.pbx.choices = [(l[0],l[1]) for l in PBXs]
    if form.validate():                                                                             #form validation
        app.logger.info( 'Save Changes Add Location Request: OK')
        Database.Add_Loc(form)
        flash('Updated Successfully')
        return redirect('/locations')    
    return render_template('add_loc.html',form = form)


@app.route('/pbx', methods=['POST', 'GET'])
def pbx():
    Database = voip_db.VoIP_DB()
    return render_template('pbxs.html',rows=Database.Get_PBX_List())




if __name__ == '__main__':
    formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('foo.log', maxBytes=10000000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0',debug=True)
raw_input()