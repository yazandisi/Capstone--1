from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class AddGameForm(FlaskForm):

    title = StringField("Game Name", validators=[
                       InputRequired(message="Game name can't be blank")])
class AddCategoryForm(FlaskForm):

    name = StringField("Category Name", validators=[
                       InputRequired(message="Name can't be blank")])
    

    description = StringField("Description", validators=[
                InputRequired(message="Description can't be blank")])

