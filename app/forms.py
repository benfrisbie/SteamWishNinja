from flask.ext.wtf import Form
from wtforms.validators import Required
from wtforms import TextField

class SearchForm(Form):
    search = TextField('search', validators = [Required()])