

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
    if rows != [] :                                     #User with such Extension founded in DB
        if str(rows[0][0]) != form.loc_id.data:         #User with such Extension is not edited User (ID edited != ID inputed)
            raise ValidationError('Location already exist')



def pbx_exist_check(form, field):
    Database = voip_db.VoIP_DB()
    rows = Database.Get_PBX_By_Fqdn(field.data)
    if rows != [] :                                     #User with such Extension founded in DB
        if str(rows[0][0]) != form.pbx_id.data:         #User with such Extension is not edited User (ID edited != ID inputed)
            raise ValidationError('PBX already exist')




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


class PbxEditForm(Form):
    pbx_id = TextField('ID', [validators.Required()])
    server = TextField('Server*', [validators.Required()])
    fqdn = TextField('PBX Fqdn*', [validators.Required(), pbx_exist_check])
    mac = TextField('MAC')
    ip = TextField('IP*', [validators.Required()])
    mask = TextField('Mask*', [validators.Required()])
    gateway = TextField('Gateway*', [validators.Required()])
    dns1 = TextField('DNS 1*', [validators.Required()])
    dns2 = TextField('DNS 2*', [validators.Required()])
    ext_ip = TextField('External IP*', [validators.Required()])
    root_pass = TextField('root Password*', [validators.Required()])
    maint_pass = TextField('maint Password*', [validators.Required()])

class PbxAddForm(Form):
    server = TextField('Server*', [validators.Required()])
    fqdn = TextField('PBX Fqdn*', [validators.Required(), pbx_exist_check])
    mac = TextField('MAC')
    ip = TextField('IP*', [validators.Required()])
    mask = TextField('Mask*', [validators.Required()])
    gateway = TextField('Gateway*', [validators.Required()])
    dns1 = TextField('DNS 1*', [validators.Required()])
    dns2 = TextField('DNS 2*', [validators.Required()])
    ext_ip = TextField('External IP*', [validators.Required()])
    root_pass = TextField('root Password*', [validators.Required()])
    maint_pass = TextField('maint Password*', [validators.Required()])