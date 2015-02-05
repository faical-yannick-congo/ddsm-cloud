import flask as fk
from flask.ext import login
from smt_view import app
from smt_view import openid, login_manager
from ..forms import LoginForm
from common.models import UserModel

@app.route('/login', methods=['GET', 'POST'])
@openid.loginhandler
def login_view():
    if fk.g.user is not None and fk.g.user.is_authenticated():
        return fk.redirect(fk.url_for('dashboard_view', id=fk.g.user.id))
    form = LoginForm()
    if form.validate_on_submit():
        fk.session['remember_me'] = form.remember_me.data
        return openid.try_login(form.openid.data, ask_for=['email'])
    return fk.render_template('login.html',
                              form=form,
                              providers=app.config['OPENID_PROVIDERS'])

@login_manager.user_loader
def load_user(id):
    return UserModel.objects.with_id(id)

@openid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        fk.flash('Invalid login. Please try again.')
        return fk.redirect(fk.url_for('login_view'))

    user, created = UserModel.objects.get_or_create(email=resp.email)

    remember_me = False
    if 'remember_me' in fk.session:
        remember_me = fk.session['remember_me']
        fk.session.pop('remember_me', None)
    login.login_user(user, remember=remember_me)
    return fk.redirect(fk.request.args.get('next') or fk.url_for('index'))

@app.before_request
def before_request():
    fk.g.user = login.current_user

@app.route('/logout')
def logout_view():
    login.logout_user()
    url = fk.request.args.get('next', fk.url_for('index_view'))
    return fk.redirect(url)
