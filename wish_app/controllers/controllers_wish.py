from wish_app import app
from flask import request, render_template, redirect, session, url_for
from wish_app.models.loregs import User
from wish_app.models.wish import Wish
from wish_app.models.granted import Grant
from wish_app.models.aime import Aime
from datetime import date, datetime


@app.route('/dashboard')
def home():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id' : session['user_id']
    }
    user = User.get_one(data)
    m = Wish.get_mine(data)
    mgwishes = Grant.get_mine(data)
    gwishes = Grant.gaw()
    ogwishes = Grant.get_other(data)
    w = []
    g = []
    uw = []
    ugwishes = []
    if len(m) > 0:
        for x in m:
            w.append(x['wish_id'])
    if len(mgwishes) > 0:
        for x in mgwishes:
            g.append(x['wish_id'])
    for x in w:
        if x not in g:
            uw.append(x)
        else: 
            pass
    for x in uw:
        ugwishes.append(Wish.get_one(x))
    return render_template('user_page.html', user = user, m = m, mgwishes = mgwishes, ugwishes = ugwishes, ogwishes = ogwishes, gwishes = gwishes)

@app.route('/stats/<int:user_id>')
def display(user_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': user_id
    }
    user = User.get_one(data)
    m = Wish.get_mine(data)
    mgwishes = Grant.get_mine(data)
    gwishes = Grant.gaw()
    ogwishes = Grant.get_other(data)
    w = []
    g = []
    uw = []
    ugwishes = []
    for x in m:
        w.append(x['wish_id'])
    if len(mgwishes) > 0:
        for x in mgwishes:
            g.append(x['wish_id'])
    for x in w:
        if x not in g:
            uw.append(x)
        else: 
            pass
    for x in uw:
        ugwishes.append(Wish.get_one(x))
    return render_template('showpage.html', mgwishes = mgwishes, user = user, gwishes = gwishes, ugwishes = ugwishes)


@app.route('/create_wish')
def addwish():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id': session['user_id']
    }
    user = User.get_one(data)
    today = date.today()
    return render_template('add_fav.html', user = user, today = today)

@app.route('/addwish', methods=['POST'])
def savewish():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'item' : request.form['item'],
        'dateadd' : date.today(),
        'dategrant' : '', 
        'description' : request.form['description'],
        'user_id' : session['user_id'],
        'created_at': 'Now',
        'updated_at': 'Now',
        'realda': '',
        'realdg': ''
    }
    valid = Wish.validation_wish(data)
    if valid:
        now = date.today()
        data['created_at'] = now
        data['updated_at'] = now
        #start = datetime.strptime(data['dateadd'], '%Y-%m-%d')
        data['dateadd'] = datetime.strftime(data['created_at'], "%b %d %Y")
        data['realda'] = datetime.now()
        Wish.save(data)
        return redirect('/dashboard')
    return redirect('/create_wish')

@app.route('/grant/<int:wish_id>')
def grant(wish_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id' : session['user_id'],
        'wish_id' : wish_id,
        'dategrant': date.today(),
        'realdg': ''
    }
    now = date.today()
    rdg = datetime.strftime(now, "%b %d %Y")
    data['realdg'] = rdg
    data['dategrant'] = datetime.strftime(now, "%b %d %Y")
    Wish.gdate(data)
    Grant.save(data)
    print(data['dategrant'])
    return redirect('/dashboard')

@app.route('/wishes/update/<int:wish_id>')
def update(wish_id):
    if 'user_id' not in session:
        return redirect('/') 
    session['wish_id'] = wish_id
    wish = Wish.get_one(wish_id)
    data = {
        'user_id':session['user_id'],
    }
    user = User.get_one(data)
    today = date.today()
    return render_template('edit_fav.html', wish = wish, user = user, today = today)

@app.route('/wishes/edit', methods=['POST'])
def edit():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'wish_id' : session['wish_id'],
        'item' : request.form['item'],
        'description' : request.form['description'],
        'user_id' : session['user_id'],
        'updated_at': 'Now',
    }
    valid = Wish.validation_wish(data)
    if valid:
        data['updated_at'] = datetime.now()
        Wish.update(data)
        return redirect('/dashboard')
    return redirect(url_for('update', wish_id = session['wish_id']))

@app.route('/like/<int:wish_id>')
def favorite(wish_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'user_id' : session['user_id'],
        'wish_id' : wish_id
    }
    count = Aime.user_like(data)
    if count < 1:
        Aime.save(data)
        nlc = Aime.get_likes(data)
        ndata = {
            'wish_id' : wish_id,
            'likes' : nlc
        }
        Wish.ulike(ndata)
    else:
        Aime.deletelike(data)
        ulc = Aime.get_likes(data)
        udata = {
            'wish_id' : wish_id,
            'likes' : ulc
        }
        Wish.ulike(udata)
    return redirect('/dashboard')

@app.route('/wishes/delete/<int:wish_id>')
def delete(wish_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'wish_id': wish_id,
        'user_id':session['user_id']
    }
    Grant.deletegrant(data)
    Grant.delete(wish_id)
    Wish.delete(data)
    return redirect('/dashboard')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')