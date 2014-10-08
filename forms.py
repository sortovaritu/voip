

from wtforms import *
import voip_db

def user_exist_check(form, field):
    Database = voip_db.VoIP_DB()
    rows = Database.Get_Sub_By_Name(field.data)
    if rows != [] :                                                                                 #User with such Name founded in DB
        if str(rows[0][0]) != form.sub_id.data:                                                     #User with such Name is not edited User (ID edited != ID inputed)
            raise ValidationError('UserName already exist')

#def user_exist_check(form, field):
#    Database = voip_db.VoIP_DB()
#    rows = Database.Get_Sub_By_Name(field.data)
#    if rows != [] :                                     #User with such Name founded in DB
#        if str(rows[0][0]) != form.sub_id.data:         #User with such Name is not edited User (ID edited != ID inputed)
#            raise ValidationError('UserName already exist')


def extension_exist_check(form, field):
    Database = voip_db.VoIP_DB()
    rows = Database.Get_Sub_By_Field('Extension',field.data)
    if rows != [] :                                     #User with such Extension founded in DB
        if str(rows[0][0]) != form.sub_id.data:         #User with such Extension is not edited User (ID edited != ID inputed)
            raise ValidationError('Extension already exist')





def location_exist_check(form, field):
    Database = voip_db.VoIP_DB()
    rows = Database.Get_Location_By_Name(field.data)
    print field.data
    print rows
    if rows != [] :                                     #User with such Extension founded in DB
        if str(rows[0][0]) != form.loc_id.data:         #User with such Extension is not edited User (ID edited != ID inputed)
            raise ValidationError('Location already exist')







class SubEditForm(Form):
    sub_id = TextField('ID', [validators.Required()])
    username = TextField('Username*', [validators.Required(),user_exist_check])
    extension = TextField('Extension*', [validators.Required(),extension_exist_check])
    location = SelectField(u'Location', coerce=int)
    password = TextField('Password*', [validators.Required(),validators.Length(max=10)])
    vmpassword = TextField('Vm Password',[validators.Length(max=9)])
    privateline = TextField('Private Line')
    pmc_id = TextField('PMC ID',[validators.Length(max=19)])
    accept_changes = BooleanField('Accept changes',[validators.Required()])


class SubAddForm(Form):
    username = TextField('Username*', [validators.Required(),user_exist_check])
    extension = TextField('Extension*', [validators.Required(),extension_exist_check])
    password = TextField('Password*', [validators.Required(),validators.Length(max=10)])
    vmpassword = TextField('Vm Password',[validators.Length(max=9)])
    location = SelectField(u'Location*', coerce=int)
    privateline = TextField('Private Line')
    pmc_id = TextField('PMC ID',[validators.Length(max=19)])
    accept_changes = BooleanField('Accept changes',[validators.Required()])


class LocEditForm(Form):
    loc_id = TextField('ID', [validators.Required()])
    location = TextField('Location*', [validators.Required(),location_exist_check])
    pbx = SelectField(u'PBX*', coerce=int)
    info = TextAreaField('Info')

class LocAddForm(Form):
    location = TextField('Location*', [validators.Required(),location_exist_check])
    pbx = SelectField(u'PBX*', coerce=int)
    info = TextAreaField('Info')