
from wtforms import Form, BooleanField, TextField, SelectField, HiddenField, validators



class SubEditForm(Form):
    sub_id = TextField('ID', [validators.Required()])
    username = TextField('Username', [validators.Required()])
    extension = TextField('Extension', [validators.Required()])
    password = TextField('Password', [validators.Required()])
    vmpassword = TextField('Vm Password')
    location = SelectField(u'Location', coerce=int)
    privateline = TextField('Private Line', [validators.Required()])
    pmc_id = TextField('PMC ID', [validators.Required()])
    accept_changes = BooleanField('Accept changes',[validators.Required()])