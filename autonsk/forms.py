from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, BooleanField, PasswordField, FormField, FieldList, IntegerField
from wtforms.validators import DataRequired, Email, Length, InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from autonsk.config import photos

class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")], render_kw={'placeholder':'email'})
    psw = PasswordField("Пароль: ", validators=[DataRequired(),
                                                Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")], render_kw={'placeholder':'пароль'})
    remember = BooleanField("Запомнить", default = False)
    submit = SubmitField("Войти")

class AttributesForm(Form):
    attribute = StringField(validators=[DataRequired()], render_kw={'placeholder':'Атрибут'})
    value = StringField(validators=[DataRequired()], render_kw={'placeholder':'Значение'})

class addGoodForm(FlaskForm):
    select_input = StringField(validators=[DataRequired()])
    brand_title = StringField(validators=[InputRequired()], render_kw={'placeholder':'Название бренда'})
    product_title = StringField(validators=[InputRequired()], render_kw={'placeholder':'Название продукта'})
    photo = FileField("Загрузите фото:", validators=[FileAllowed(photos, 'Только изображения!')])
    article = StringField(validators=[InputRequired()])
    manufacturer = StringField(validators=[InputRequired()])
    price = IntegerField(validators=[DataRequired()], render_kw={'placeholder':'Цена'})
    amount = IntegerField(validators=[DataRequired()], render_kw={'placeholder':'Количество'})
    period = IntegerField(validators=[DataRequired()], render_kw={'placeholder':'Время доставки'})
    attributes = FieldList(FormField(AttributesForm), min_entries=0)
    submit = SubmitField('Опубликовать')


    

