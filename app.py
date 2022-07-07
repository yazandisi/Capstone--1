from s import key, c_id, a_id
from flask import Flask, render_template, redirect, flash, session, request, jsonify
# request
from flask_debugtoolbar import DebugToolbarExtension
# from requests import session
import requests
req_session = requests.session
from models import db, connect_db, Category_Game, Category, Game, User, Comment
from forms import UserForm, AddGameForm, AddCategoryForm
from search_logic import search_logic, search_by_id_logic, search_for_vid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///video_game_app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'Yazan'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


# key ='acszo6wtibxnv5kkyjfvx4dy8vrjcj'
# c_id='o5ny07nd7uy2wol6w70f8bo17qhv1a'
# a_id = 'Bearer nwylltbgpyzj0hb8xohtrl6y5x7he1'

connect_db(app)
data=[]


@app.route('/')
def index():
    """Populates the login/sign-up page"""
    return render_template("index.html")

@app.route('/game_result', methods=["GET", "POST"])
def game_result():
    games = Game.query.filter_by(favorite=True, user_id=session['user_id']).all()
    game = {"lookup_id": [g.api_id for g in games],
    "user_id": [g.user_id for g in games]
    }
    size = len(data)
    form = AddGameForm()
    if form.validate_on_submit():
        data.append(search_logic(form,data,c_id,a_id ))
        return redirect('/game_result')
    return render_template('game_result.html', info=data, size=size, form=form, game=game)


@app.route('/game-home',methods=["GET","POST"])
def game_home():
    games = Game.query.all()
    cat_form = AddCategoryForm()
    category = Category.query.filter_by(user_id=session['user_id']).all()
    if "user_id" not in session:
        flash("Please login!")
        return redirect('/')
    form = AddGameForm()
    if form.validate_on_submit():
        data.append(search_logic(form,data,c_id,a_id))
        return redirect('/game_result')
    
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
            return redirect('/game-home')
    else:
        return render_template('game-home.html',form=form, games=games, category=category, cat_form=cat_form)

@app.route('/register', methods=['GET', 'POST'])
def register_user():
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
    game = Game.query.get_or_404(id)
    comment = Comment.query.filter_by(user_id=session['user_id'],game_id=id).all()
    if session['user_id'] != game.user_id:
        flash("Nothing here!")
        return redirect('/game-home')
    api_id = game.api_id
    info = search_by_id_logic(api_id,data,c_id,a_id)
    img = info[0]["screenshots"]
    video = info[0]["videos"][0]
    vid_data = search_for_vid(video,data, c_id, a_id)


    return render_template('game_info.html', game=game, info=info, img=img, video=video, vid_data=vid_data, comment=comment)

@app.route('/game_info/comment/<int:id>', methods=['POST'])
def submit_comment(id):
    comment = request.form['comments']
    new_comment = Comment(comment=comment, user_id=session['user_id'], game_id=id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(f'/game_info/{id}')

@app.route('/login', methods=['GET','POST'])
def login_user():
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
    session.pop('user_id')
    flash("Logout successful!")
    return redirect ('/')


@app.route('/get_fav', methods=["POST"])
def get_fav():
    data = {
        "fav_input":"",
        "fav_name":"",
        "api_Id":"",
    }
    print(request.json['fav_input'])
    print(request.json['fav_name'])
    
    if request.json['fav_input'] == 'on':
        title = request.json['fav_name']
        api_id = request.json['api_Id']
        new_game = Game( title=title, genre="genre", company="company", summary='summary', url="url", favorite=True, user_id=session['user_id'], api_id=api_id )
        session['fav_game'] = new_game.title
        db.session.add(new_game)
        db.session.commit()
        print('good to go')
        
    return jsonify(data) 

@app.route('/delete_fav', methods=["POST"])
def delete_fav():
    data = {
        "fav_input":"",
        "fav_name":""
    }
    title = request.json['fav_name']
    
    game = Game.query.filter_by(title=title, user_id=session['user_id']).first()
    print(game.id)
    all_comments = Comment.query.filter(Comment.game_id==game.id).all()
    print(all_comments)
    print("******************COMMENTS****************")
   

    for a in all_comments:
        db.session.delete(a)
        db.session.commit()
    db.session.delete(game)
    db.session.commit()
    print('*******************DELETED***********************')
    return jsonify(data)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_from_home(id):
    game = Game.query.get(id)
    all_game = Category_Game.query.all()
    for a in all_game:
        if a.category_id:
            db.session.delete(a)
            db.session.commit()
    db.session.delete(game)
    db.session.commit()
    return redirect('/game-home')

@app.route('/delete/category/<int:id>', methods=['POST'])
def delete_cat_from_home(id):
    category = Category.query.get(id)
    all_cat = Category_Game.query.all()
    for a in all_cat:
        if a.category_id:
            db.session.delete(a)
            db.session.commit()
    db.session.delete(category)
    db.session.commit()
    return redirect('/game-home')

@app.route('/category/game/<int:id>', methods=["POST"])
def custome_cat(id):
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
            return redirect ("/game-home")
    except:
        flash("Please select an option")
        return redirect('/game-home')

@app.route('/category/<int:id>')
def cat_list(id):
    
    cat_game = Category_Game.query.filter_by(category_id=id).all()
    games = [c.game_id for c in cat_game]
    info = []
    for c in games:
        game_data = Game.query.get_or_404(c)
        info.append(game_data)
    return render_template('cat_games.html', games=games, info=info)



