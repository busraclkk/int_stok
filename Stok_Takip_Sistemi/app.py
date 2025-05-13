from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stok.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)



class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        kullanici = request.form['username']
        sifre = request.form['password']

        user = User.query.filter_by(username=kullanici).first()
        
        if user and check_password_hash(user.password, sifre):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Geçersiz kullanıcı adı veya şifre', 'danger')
            return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        kullanici = request.form['username']
        sifre = request.form['password']
        
        hashed_password = generate_password_hash(sifre, method='pbkdf2:sha256')

        user_exists = User.query.filter_by(username=kullanici).first()
        if user_exists:
            flash('Bu kullanıcı adı zaten alınmış.', 'warning')
        else:
            new_user = User(username=kullanici, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Kayıt başarılı, giriş yapabilirsiniz.', 'success')
            return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    toplam_urun = Product.query.count()
    dusuk_stok = Product.query.filter(Product.quantity < 10).count()
    yeni_eklenen = Product.query.order_by(Product.id.desc()).limit(3).count()  

    return render_template('dashboard.html',
                           toplam_urun=toplam_urun,
                           dusuk_stok=dusuk_stok,
                           yeni_eklenen=yeni_eklenen)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'info')
    return redirect(url_for('index'))


@app.route('/urunler')
@login_required
def urunler():
   
    products = Product.query.all()
    return render_template('urunler.html', products=products)


@app.route('/urun/ekle', methods=['GET', 'POST'])
@login_required
def urun_ekle():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        quantity = request.form['quantity']
        price = request.form['price']

       
        new_product = Product(name=name, category=category, quantity=quantity, price=float(price))
        db.session.add(new_product)
        db.session.commit()
        flash('Yeni ürün başarıyla eklendi!', 'success')
        return redirect(url_for('urunler'))

    return render_template('urun_ekle.html')


with app.app_context():
    db.create_all()  


if __name__ == '__main__':
    app.run(debug=True)
