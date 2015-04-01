from ddsmdb.common.models import UserModel
from flask.ext.stormpath import user
import flask as fk
from cloud import app

@app.route('/dashboard')
def user_view():
    (user_model, created) = UserModel.objects.get_or_create(email=user.email)
    return fk.redirect(fk.url_for('dashboard_view', id=user_model.id))

@app.route('/dashboard/<objectid:id>')
def dashboard_view(id):
    user_model = UserModel.objects.with_id(id)
    return fk.render_template('dashboard.html', user_model=user_model)
