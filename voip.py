from flask import Flask, url_for, render_template, request


import voip_db, forms

#conn.close()

app = Flask(__name__,static_folder='bootstrap')

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

        return render_template('sub_db.html',name='Name',rows=Database.Get_Sub_By_Name(user_name))


@app.route('/subscribers/edit/<sid>', methods=['POST', 'GET'])
def edit_sub(sid):
    form = forms.SubEditForm(request.form)
    Database = voip_db.VoIP_DB()
    rows = Database.Get_Sub_By_ID(sid)                                                                  #Get sunscriber info by ID
    Locations = Database.Get_Locations()
    print form.username.data
    if request.method == 'GET':                                                                #Get list of Locations
        form.location.choices = ((l[0],l[1]) for l in Locations)          #Fill list of locations to SelectField 
        form.location.default = rows[0][3]                                                                  #Chose user Location from list of locations in SelectField
        #form.process()        
        form.sub_id.data = sid                                                                              #Get User ID (static field)
        form.username.data = rows[0][1]                                                                     #Get UserName
        form.extension.data = rows[0][2]
        form.password.data = rows[0][4]
        form.vmpassword.data = rows[0][5]
        form.privateline.data = rows[0][6]
        form.pmc_id.data = rows[0][7]

    if request.method == 'POST':
        #form.location.choices = ((l[0],l[1]) for l in Locations)          #Fill list of locations to SelectField 
        print Locations
        #form.location.default = rows[0][3]                                                                  #Chose user Location from list of locations in SelectField
        #form.process()
        print form.username.data
        print form.username
        if form.validate(): 
            return redirect(url_for('login'))

    return render_template('edit_sub.html',name='Name',form=form)








if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
raw_input()