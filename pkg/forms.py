from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, DecimalField
from wtforms.validators import DataRequired, Email


class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class Farmerlogform(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message="Email is required"), Email(message="Enter a valid email")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    submit = SubmitField('Login')

    class meta:
        csrf = True
        csrf_time_limit = 7200


class Restaurantlogform(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message="Email is required"), Email(message="Enter a valid email")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    submit = SubmitField('Login')

    class meta:
        csrf = True
        csrf_time_limit = 7200


# Sign Up

class Farmersignform(FlaskForm):
    farm_name = StringField('Farm Name', validators=[DataRequired(message="Farm name is required")])
    firstname = StringField('First Name', validators=[DataRequired(message="First name is required")])
    lastname = StringField('Last Name', validators=[DataRequired(message="Last name is required")])
    phone_number = StringField('Phone Number', validators=[DataRequired(message="Phone number is required")])
    state = SelectField('State', choices=[(1, 'Abia State'), (2, 'Adamawa State'),
                                          (3, 'Akwa Ibom State'),
                                          (4, 'Anambra State'),
                                          (5, 'Bauchi State'),
                                          (6, 'Bayelsa State'),
                                          (7, 'Benue State'),
                                          (8, 'Borno State'),
                                          (9, 'Cross River State'),
                                          (10, 'Delta State'),
                                          (11, 'Ebonyi State'),
                                          (12, 'Edo State'),
                                          (13, 'Ekiti State'),
                                          (14, 'Enugu State'),
                                          (15, 'FCT'),
                                          (16, 'Gombe State'),
                                          (17, 'Imo State'),
                                          (18, 'Jigawa State'),
                                          (19, 'Kaduna State'),
                                          (20, 'Kano State'),
                                          (21, 'Katsina State'),
                                          (22, 'Kebbi State'),
                                          (23, 'Kogi State'),
                                          (24, 'Kwara State'),
                                          (25, 'Lagos State'),
                                          (26, 'Nasarawa State'),
                                          (27, 'Niger State'),
                                          (28, 'Ogun State'),
                                          (29, 'Ondo State'),
                                          (30, 'Osun State'),
                                          (31, 'Oyo State'),
                                          (32, 'Plateau State'),
                                          (33, 'Rivers State'),
                                          (34, 'Sokoto State'),
                                          (35, 'Taraba State'),
                                          (36, 'Yobe State'),
                                          (37, 'Zamfara State')],
                        coerce=int,  # ensures the value submitted is an integer (ID)
                        validators=[DataRequired(message="State is required")])

    address = StringField('Address', validators=[DataRequired(message="Address is required")])
    email = StringField('Email',
                        validators=[DataRequired(message="Email is required"), Email(message="Enter a valid email")])
    username = StringField('Username', validators=[DataRequired(message="Username is required")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(message="Confirm password field is required")])
    submit = SubmitField('Sign Up')

    class Meta:
        csrf = True
        csrf_time_limit = 7200


class Restaurantsignform(FlaskForm):
    name = StringField('Name', validators=[DataRequired(message="Name is required")])
    address = StringField('Address', validators=[
        DataRequired(message="We would love you to enjoy a smooth delivery, please provide your address")])
    contact_email = StringField('Email', validators=[DataRequired(message="Email is required"),
                                                     Email(message="Enter a valid email")])
    contact_num = StringField('Phone number', validators=[DataRequired(message="We would love to hear from you")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    cpassword = PasswordField('Password', validators=[DataRequired(message="You need to supply this field")])
    submit = SubmitField('Signup')

    class meta:
        csrf = True
        csrf_time_limit = 7200


class FarmerAddProductForm(FlaskForm):
    pro_name = StringField('Product Name', validators=[DataRequired()])
    pro_category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    qua_avail = FloatField('Quantity Available', validators=[DataRequired()])
    price_per_unit = DecimalField('Price per Unit', validators=[DataRequired()])
    pro_picture = FileField('Product Picture',
                            validators=[FileAllowed(['jpg', 'png', 'jpeg'],
                                                    'Images only!')])
    pro_status = StringField('Product Status', validators=[DataRequired()])

    # Populate the categories dropdown dynamically from your Category model
    def populate_categories(self):
        from pkg.models import Category
        self.pro_category_id.choices = [
            (cat.category_id, cat.category_name)
            for cat in Category.query.all()]
