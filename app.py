from s import c_id, a_id
from flask import Flask, render_template, redirect, flash, session, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import requests
import datetime
req_session = requests.session
from models import db, connect_db, Category_Game, Category, Game, User, Comment
from forms import UserForm, AddGameForm, AddCategoryForm
from search_logic import search_logic, search_by_id_logic, search_for_vid, get_live_video
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///video_game_app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECERT_KEY', 'hellosecret1')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
data=[]

@app.route('/')
def index():
    """Populates the login/sign-up page"""
    return render_template("index.html")

@app.route('/game-home',methods=["GET","POST"])
def game_home():
    """Renders the post login screen. Checks for saved games and created catergories. Also handels form subs"""
    games = Game.query.all()
    cat_form = AddCategoryForm()
    if "user_id" not in session:
        flash("Please login!")
        return redirect('/')
    form = AddGameForm()
    category = Category.query.filter_by(user_id=session['user_id']).all()
    if form.validate_on_submit():
        ts = datetime.datetime.now().timestamp()
        games = Game.query.filter_by(favorite=True, user_id=session['user_id']).all()
        game = {"lookup_id": [g.api_id for g in games],
        "user_id": [g.user_id for g in games]
                }
        size = len(data)
        print('************DATA BEFORE APPEND******************')
        print(data)
        print('************DATA BEFORE APPEND******************')
        data.append(search_logic(form,data,c_id,a_id))
        print('************DATA AFTER APPEND******************')
        print(data)
        print('************DATA AFTER APPEND******************')
        return render_template('first_result.html', info=data, size=size, form=form, game=game, ts=ts)
    elif cat_form.validate_on_submit():
        name = cat_form.name.data
        description = cat_form.description.data
        q = Category.query.filter(Category.name==name, Category.description==description, Category.user_id==session['user_id'])
        if q.count() >= 1:
            flash("Category Already Exists!")
            return redirect("/game-home")
        else:
            new_playlist = Category(name=name, description=description, user_id=session['user_id'])
            db.session.add(new_playlist)
            db.session.commit()
            flash('Catagory Created')
            return redirect('/game-home')
    else:
        return render_template('game-home.html',form=form, games=games, category=category, cat_form=cat_form)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Creates new user and handels validation"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        try:
            new_user = User.register(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            flash("Created account successfully")
            return redirect('/game-home')
        except:
            flash("Username / Password already taken")
            return redirect('/register')
    return render_template('register.html', form=form)

@app.route('/game_info/<int:id>', methods=['GET', 'POST'])
def game_info(id):
    """Renders the selected game page providing Twitch live TV, youtube trailer/gameplay and live tweets from twitch.
     uses the Twitch, IGDB, and giphy APIs"""
    if "user_id" not in session:
        flash("Please login!")
        return redirect('/')
    game = Game.query.get_or_404(id)
    comment = Comment.query.filter_by(user_id=session['user_id'],game_id=id).all()
    if session['user_id'] != game.user_id:
        flash("Nothing here!")
        return redirect('/game-home')
    api_id = game.api_id
    info = search_by_id_logic(api_id,data,c_id,a_id)
    try:
        img = info[0]["screenshots"]
        video = info[0]["videos"][0]
        vid_data = search_for_vid(video,data, c_id, a_id)
        live_video = get_live_video(game.title, c_id, a_id)
    except:
        img = []
        video = info[0]["videos"][0]
        vid_data = search_for_vid(video,data, c_id, a_id)
        live_video = get_live_video(game.title, c_id, a_id)
    return render_template('game_info.html', game=game, info=info, img=img, vid_data=vid_data, comment=comment, live_video=live_video)

@app.route('/game_info/comment/<int:id>', methods=['POST'])
def submit_comment(id):
    """Lets user add notes for a specific game page that is saved in the DB"""
    comment = request.form['comments']
    new_comment = Comment(comment=comment, user_id=session['user_id'], game_id=id)
    db.session.add(new_comment)
    db.session.commit()
    flash("Note Added")
    return redirect(f'/game_info/{id}')

@app.route('/login', methods=['GET','POST'])
def login_user():
    """Lets exisiting users login and checks for valid user/name. Validation done with Bcrypt"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['user_id'] = user.id
            return redirect('/game-home')
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)

@app.route('/logout', methods=["POST"])
def logout_user():
    """Removes user id from seesion to log out"""
    session.pop('user_id')
    flash("Logout successful!")
    return redirect ('/')

@app.route('/get_fav', methods=["POST"])
def get_fav():
    """Listens for request incoming from JS axios and apends data to user home-page"""
    data = {
        "fav_input":"",
        "fav_name":"",
        "api_Id":"",
    }
    if request.json['fav_input'] == 'on':
        title = request.json['fav_name']
        api_id = request.json['api_Id']
        new_game = Game( title=title, favorite=True, user_id=session['user_id'], api_id=api_id )
        session['fav_game'] = new_game.title
        db.session.add(new_game)
        db.session.commit()
    return jsonify(data) 

@app.route('/delete_fav', methods=["POST"])
def delete_fav():
    """Listens for a delete request and removes games. Incoming request from JS Axios"""
    data = {
        "fav_input":"",
        "fav_name":""
    }
    title = request.json['fav_name']
    game = Game.query.filter_by(title=title, user_id=session['user_id']).first()
    category_game = Category_Game.query.filter(Category_Game.game_id==game.id).first()
    if category_game:
        db.session.delete(category_game)
        db.session.commit()
    all_comments = Comment.query.filter(Comment.game_id==game.id).all()
    for a in all_comments:
        db.session.delete(a)
        db.session.commit()
    db.session.delete(game)
    db.session.commit()
    return jsonify(data)
@app.route('/delete/<int:id>', methods=['POST'])
def delete_from_home(id):
    """Remove a game from all locations"""
    game = Game.query.get(id)
    all_comments = Comment.query.filter(Comment.game_id==game.id).all()
    for a in all_comments:
        db.session.delete(a)
        db.session.commit()
    category_game = Category_Game.query.filter(Category_Game.game_id==game.id).all()
    for a in category_game:
        if a.game_id == id:
            db.session.delete(a)
            db.session.commit()
    db.session.delete(game)
    db.session.commit()
    flash('Game Removed Everywhere')
    return redirect('/game-home')

@app.route('/delete/category/<int:id>', methods=['POST'])
def delete_cat_from_home(id):
    """Remove a custom category"""
    category = Category.query.get(id)
    all_cat = Category_Game.query.filter(Category_Game.category_id==id).all()
    for a in all_cat:
        if a.category_id:
            db.session.delete(a)
            db.session.commit()
    db.session.delete(category)
    db.session.commit()
    flash("Category Removed")
    return redirect('/game-home')

@app.route('/delete/category/<int:id>/<int:game_id>')
def delete_game_from_cat(id, game_id):
    """Remove only a single game from one category"""
    category_game = Category_Game.query.filter(Category_Game.category_id==id,Category_Game.game_id==game_id).first()
    db.session.delete(category_game)
    db.session.commit()
    return redirect(f'/category/{id}')
@app.route('/delete/comment/<int:id>/game/<int:game_id>', methods=['POST'])
def delete_comment(id,game_id):
    """Removes a note from a game page"""
    comment = Comment.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    flash('Note Deleted')
    return redirect(f'/game_info/{game_id}')

@app.route('/category/game/<int:id>', methods=["POST"])
def custom_cat(id):
    """Allows user to make custom categories"""
    category_id = request.form['addCat']
    try:
        q = Category_Game.query.filter(Category_Game.category_id==category_id, Category_Game.game_id==id)
        if q.count() >= 1:
            flash("Game Already in playlist!")
            return redirect("/game-home")
        else:
            new_cat_game = Category_Game(category_id=category_id, game_id=id)
            db.session.add(new_cat_game)
            db.session.commit()
            flash('Game Added')
            return redirect ("/game-home")
    except:
        flash("Please select an option")
        return redirect('/game-home')

@app.route('/category/<int:id>')
def cat_list(id):
    """Renders a custom category"""
    cat = Category.query.get(id)
    cat_game = Category_Game.query.filter_by(category_id=id).all()
    games = [c.game_id for c in cat_game]
    info = []
    for c in games:
        game_data = Game.query.get_or_404(c)
        info.append(game_data)
    return render_template('cat_games.html', games=games, info=info,cat=cat)