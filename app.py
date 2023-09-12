from flask import Flask, render_template, url_for, request, redirect, session
from flask_login import LoginManager, logout_user,current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
import mysql.connector
import ast


konekcija = mysql.connector.connect(
        passwd="", # lozinka za bazu
        user="root", # korisnicko ime
        database="film", # ime baze
        port = 3306, # port na kojem je mysql server
        auth_plugin="mysql_native_password" # ako se koristi mysql 8.x
)

kursor = konekcija.cursor(dictionary=True)

app = Flask(__name__)
app.secret_key = "tajni_kljuc_aplikacije"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    upit = "SELECT * FROM korisnici WHERE id = %s"
    kursor.execute(upit, (user_id,))
    return kursor.fetchone()

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('logout'))

def ulogovan():
    if"ulogovani_korisnik" in session:
        return True
    else:
        return False

@app.route('/home')
def render_home():
    if not ulogovan():
        return redirect(url_for('login'))
    return render_template('home.html',user_logged_in=current_user.is_authenticated,logged_in=ulogovan())


@app.route('/movie/<id>')
def render_movie(id):
    overview = request.args.get('overview')
    title = request.args.get('title')
    upit = """
        SELECT komentari.id, komentari.sadrzaj, korisnici.korisnickoime
        FROM komentari
        JOIN korisnici ON komentari.korisnik_id = korisnici.id
        WHERE komentari.film_id = %s AND komentari.odobren = 1
    """
    vrednosti = (id,)
    kursor.execute(upit, vrednosti)
    komentari = kursor.fetchall()
    return render_template('movie.html', id=id, title=title, overview=overview, komentari=komentari)

@app.route('/serije/<id>')
def render_series(id):
    overview = request.args.get('overview')
    title = request.args.get('title')
    upit = """
        SELECT komentari.id, komentari.sadrzaj, korisnici.korisnickoime
        FROM komentari
        JOIN korisnici ON komentari.korisnik_id = korisnici.id
        WHERE komentari.film_id = %s AND komentari.odobren = 1
    """
    vrednosti = (id,)
    kursor.execute(upit, vrednosti)
    komentari = kursor.fetchall()
    return render_template('serija.html', id=id, title=title, overview=overview, komentari=komentari)




#server side

@app.route('/', methods=["GET", "POST"])
def render_korisnik_novi():
        if request.method == "GET":
            upit2 = "select * from korisnici"
            kursor.execute(upit2)
            korisnici = kursor.fetchall()
            return render_template('korisnik_novi.html',korisnici= korisnici)

        if request.method == "POST":
            forma = request.form
            hesovana_lozinka = generate_password_hash(forma["lozinka"])
            vrednosti = (
                forma["korisnickoime"],
                forma["email"],
                hesovana_lozinka
            )

        upit = """insert into
                    korisnici(korisnickoime, email, lozinka)
                    values (%s, %s, %s)
        """
        kursor.execute(upit, vrednosti)
        konekcija.commit()
        return redirect(url_for("login"))


#deo za login

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        forma = request.form
        upit = "SELECT * FROM korisnici WHERE email=%s"
        vrednost = (forma["email"], )
        kursor.execute(upit, vrednost)
        korisnik = kursor.fetchone()
        if (korisnik["lozinka"], forma["lozinka"]):
            session["ulogovani_korisnik"] = korisnik
            return redirect(url_for("render_home"))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route('/serije')
def render_serije():
    if not ulogovan():
        return redirect(url_for('login'))
    
    API_KEY = 'c5632362513441998856f721496efc81'
    BASE_URL = 'https://api.themoviedb.org/3'
    LANGUAGE = 'hr'  # Promenite jezik na željeni
    API_URL = f'{BASE_URL}/discover/tv?language={LANGUAGE}&api_key={API_KEY}&with_genres=serija_zanr_id'  # Zamenjivanje serija_zanr_id sa ID-jem željenog žanra serija

    return render_template('serije.html', API_URL=API_URL, user_logged_in=current_user.is_authenticated, logged_in=ulogovan())

@app.route('/uputstvo-za-prevod')
def render_prevodi():
    if not ulogovan():
        return redirect(url_for('login'))
    return render_template('prevodi.html')

@app.route('/watchlist')
def render_wishlist():
    if not ulogovan():
        return redirect(url_for('login'))

    user_id = session["ulogovani_korisnik"]["id"]
    upit = "SELECT watchlist.movie_id, watchlist.poster_path, watchlist.title, watchlist.opis FROM watchlist WHERE watchlist.user_id = %s"
    kursor.execute(upit, (user_id,))
    wishlist_films = kursor.fetchall()

    return render_template('wishlist.html', wishlist_films=wishlist_films, logged_in=ulogovan())

# DODAVANJE U WATCHLIST
@app.route('/addToWatchlist', methods=['POST'])
def add_to_watchlist():
    if not ulogovan():
        return jsonify({'success': False, 'message': 'Niste prijavljeni.'})

    data = request.json
    filmId = data.get('filmId')
    naslovFilma = data.get('naslovFilma')
    userId = session["ulogovani_korisnik"]["id"]
    opis = data.get('opis')
    posterpath = data.get('posterpath')

    upit = "INSERT INTO watchlist (user_id, movie_id, title, opis, poster_path) VALUES (%s, %s, %s, %s, %s)"
    vrednosti = (userId, filmId, naslovFilma, opis, posterpath)

    try:
        kursor.execute(upit, vrednosti)
        konekcija.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    
#BRISANJE FILMA IZ WATCHLIST-E
@app.route('/removeFromWatchlist', methods=['POST'])
def remove_from_watchlist():
    if not ulogovan():
        return jsonify({'success': False, 'message': 'Niste prijavljeni.'})

    data = request.json
    filmId = data.get('filmId')
    userId = session["ulogovani_korisnik"]["id"]

    upit = "DELETE FROM watchlist WHERE user_id = %s AND movie_id = %s"
    vrednosti = (userId, filmId)

    try:
        kursor.execute(upit, vrednosti)
        konekcija.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    if request.method == "POST":
        forma = request.form
        upit = "SELECT * FROM administratori WHERE korisnickoime = %s"
        vrednost = (forma["korisnickoime"], )
        kursor.execute(upit, vrednost)
        admin = kursor.fetchone()
        if (admin["lozinka"], forma["lozinka"]):
            session["admin_ulogovan"] = admin
            return redirect(url_for("admin_panel"))
        else:
            return render_template("admin_login.html")
    else:
        return render_template("admin_login.html")


@app.route('/add_comment', methods=['POST'])
def add_comment():
    if not ulogovan():
        return jsonify({'success': False, 'message': 'Niste prijavljeni.'})

    user_id = session["ulogovani_korisnik"]["id"]
    korisnicko_ime = session["ulogovani_korisnik"]["korisnickoime"]
    film_id = request.json.get('movieId')
    komentar = request.json.get('komentar')

    upit = "INSERT INTO komentari (film_id, korisnik_id, korisnickoime, sadrzaj, odobren) VALUES (%s, %s, %s, %s, 0)"
    vrednosti = (film_id, user_id, korisnicko_ime, komentar)

    try:
        kursor.execute(upit, vrednosti)
        konekcija.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})



@app.route('/admin/panel')
def admin_panel():
    if not session.get('admin_ulogovan'):
        return redirect(url_for('admin_login'))

    # Dohvatanje komentara koji čekaju odobrenje iz baze podataka
    upit = "SELECT * FROM komentari WHERE odobren = 0"
    kursor.execute(upit)
    komentari = kursor.fetchall()

    return render_template('admin_panel.html', komentari=komentari)


@app.route('/admin/odobri/<int:komentar_id>', methods=['POST'])
def odobri_komentar(komentar_id):
    if not session.get('admin_ulogovan'):
        return jsonify({'success': False, 'message': 'Niste prijavljeni kao administrator.'})

    try:
        # Promena kolone 'odobren' u tabeli 'komentari' sa vrednosti 0 na 1
        upit = "UPDATE komentari SET odobren = 1 WHERE id = %s"
        vrednosti = (komentar_id,)
        kursor.execute(upit, vrednosti)
        konekcija.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/admin/obrisi/<int:komentar_id>', methods=['POST'])
def obrisi_komentar(komentar_id):
    if not session.get('admin_ulogovan'):
        return jsonify({'success': False, 'message': 'Niste prijavljeni kao administrator.'})

    try:
        # Brisanje komentara iz tabele 'komentari' na osnovu ID-ja
        upit = "DELETE FROM komentari WHERE id = %s"
        vrednosti = (komentar_id,)
        kursor.execute(upit, vrednosti)
        konekcija.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})





@app.route('/logout')
def logout():
    logout_user()
    session.pop('ulogovani_korisnik', None)
    return redirect(url_for("render_korisnik_novi"))


app.run(debug = False, host='0.0.0.0')
