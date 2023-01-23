from flask import Flask, render_template, url_for, request, redirect, session
from flask_login import LoginManager, logout_user,current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import ast
import mariadb


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
    return render_template('movie.html', id=id, title=title, overview=overview)

@app.route('/movies/<int:page>')
def render_movies(page):
    movies = get_movies_from_db(page)
    return render_template('movies.html', movies=movies, page=page)

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

@app.route('/logout')
def logout():
    logout_user()
    session.pop('ulogovani_korisnik', None)
    return redirect(url_for("render_korisnik_novi"))


app.run(debug = True)