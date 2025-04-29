from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def urun_ekle():
    return render_template('logout.html')

@app.route('/urunler')
def stok_duzenle():
    return render_template('urunler.html')

@app.route('/urun/ekle')
def stok_listesi():
    return render_template('urun_ekle.html')


@app.route('/satis/rapor')
def satis_raporlari():
    return render_template('satis_raporlari.html')

if __name__ == '__main__':
    app.run(debug=True)
