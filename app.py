import os
import random
from pathlib import Path
import sqlite3
import json

from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from flask_uploads import configure_uploads, patch_request_class
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from webpack_boilerplate.config import setup_jinja2_ext

from autonsk.FDataBase import FDataBase
from autonsk.UserLogin import UserLogin
from autonsk.forms import LoginForm, addGoodForm
from autonsk.config import photos, DATABASE, SECRET_KEY, MAX_CONTENT_LENGTH




BASE_DIR = Path(__file__).parent
app = Flask(__name__, static_folder="frontend/build", static_url_path="/static/")
app.config.update({
    'WEBPACK_LOADER': {
        'MANIFEST_FILE': BASE_DIR / "frontend/build/manifest.json",
    }
})

app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'autonsk.db'),
                       SECRET_KEY = SECRET_KEY
))

app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(app.root_path, 'frontend/vendors/images')
configure_uploads(app, photos)
# максимальный размер файла, по умолчанию 16MB
patch_request_class(app) 

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

setup_jinja2_ext(app)


@app.cli.command("webpack_init")
def webpack_init():
    from cookiecutter.main import cookiecutter
    import webpack_boilerplate
    pkg_path = os.path.dirname(webpack_boilerplate.__file__)
    cookiecutter(pkg_path, directory="frontend_template")


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()



@app.route('/')
def main():
  goods = dbase.get_goods()
  return render_template('index.html', goods = goods)

@app.route('/goods/<int:id>', methods = ['POST', 'GET'])
def show_good(id):
  def sqlRowToJson(table):
      res = [tuple(table[row]) for row in range(len(table))]
      return json.dumps(res)
  
  good_dict = {}
  min_price = request.args.get('minPrice')
  max_price = request.args.get('maxPrice')
  if min_price and max_price:
      response = dbase.getGoodPriceFilter(id, min_price, max_price)
      response_json = sqlRowToJson(response)
      return {
          'data': response_json
      }
  good, attributes, offers, table_products = dbase.show_goods(id)
  print(good, attributes, offers, table_products)
  good_dict['good'] = good
  good_dict['good_attrs'] = attributes
  good_dict['good_offers'] = offers
  good_dict['table_products'] = table_products

  table_products_json = sqlRowToJson(table_products)

  return render_template('good.html', context=[good_dict, table_products_json])

@app.route('/register', methods = ['POST', 'GET'])
def register():
  if request.method == 'POST':
    hash = generate_password_hash(request.form['psw'])
    if request.form.get('companyOpf'):
      company_data = {'companyOpf': request.form['companyOpf'],
                      'companyName': request.form['companyName'],
                      'companyInn': request.form['companyInn'],
                      'companyKpp': request.form['companyKpp'],
                      'companyPhone': request.form['companyPhone'],
                      'companyAddress': request.form['companyAddress'],
                      'companyType': request.form['companyType']
                      }
      res = dbase.addUser(request.form['name'], request.form['email'], hash, company_data)
    else:
      res = dbase.addUser(request.form['name'], request.form['email'], hash, False)
    if res:
        return redirect(url_for('login'))
    else:
        flash("Ошибка при добавлении в БД", "error")
  return render_template('register.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw_hash'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(url_for("main"))

    return render_template("login.html", form=form)

@app.route('/add/good', methods = ['POST', 'GET'])
@login_required
def add_good():
    user_id = current_user.get_id()
    is_supplier = dbase.isSupplier(user_id)
    if not is_supplier['organization_id']:
        abort(401)

    goods = dbase.get_goods_option()
    form = addGoodForm()
    if form.validate_on_submit():
        try:
            good_id = int(form.select_input.data)
            dbase.setGoodAvailability(good_id,
                                      is_supplier['organization_id'],
                                      form.price.data,
                                      form.amount.data,
                                      form.period.data,
            )
            #for i in form._fields:
                #print(i,form._fields[i].data)
        except:
            manufacturer_id = None
            is_manufacturer = dbase.isManufacturerByTitle(form.manufacturer.data)
            if not is_manufacturer:
                manufacturer_id = dbase.setManufacturer(form.manufacturer.data)
                print(manufacturer_id)
            photo = photos.save(form.photo.data)
            photo_url = photos.url(photo)
            photo_id = dbase.setGoodImage(photo_url)
            print(photo_id)
            good_id = dbase.setGood(form.select_input.data,
                                 manufacturer_id,
                                 photo_id,
            )
            for attr in form.attributes.data:
                dbase.setGoodAttribute(good_id,
                                       attr['attribute'],
                                       attr['value'],
                )
            dbase.setGoodAvailability(good_id,
                                      is_supplier['organization_id'],
                                      form.price.data,
                                      form.amount.data,
                                      form.period.data,
            )
    return render_template("addGood.html", goods = goods, form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
  app.run(host='localhost', port=8000)