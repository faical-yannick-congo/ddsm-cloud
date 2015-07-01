from ddsmdb.common.models import UserModel
from flask.ext.stormpath import user
from flask.ext.stormpath import login_required
import flask as fk
from cloud import app
import datetime

@app.route('/cloud')
def user_view():
    print fk.request.headers.get('User-Agent')
    print fk.request.remote_addr
    (user_model, created) = UserModel.objects.get_or_create(email=user.email)
    print "Token %s"%user_model.api_token
    # token = user.custom_data.get('token', "")
    # if token == "":
    #     user.custom_data['token'] = "abcdefghijklmnopqrst0123456789"
    #     user.save()
    user_model.renew("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
    print "Session: %s"%user_model.session
    # return fk.redirect(fk.url_for('dashboard_view', id=user_model.id))
    # return fk.redirect(fk.url_for('dashboard_cloud', hash_session=user_model.session))
    return fk.redirect('http://localhost:8080/ddsm-frontend/?session=%s'%user_model.session)

@app.route('/cloud/<hash_session>')
@login_required
def dashboard_cloud(hash_session):
	user_model = UserModel.objects(session=hash_session).first()
	print fk.request.path
	if user_model is None:
		return fk.redirect('http://localhost:8080/ddsm-frontend/')
		# return fk.redirect(fk.url_for('stormpath.logout', next=fk.request.path))
	else:
		allowance = user_model.allowed("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
		print "Allowance: "+allowance
		if allowance == hash_session:
		    user_model = UserModel.objects(session=hash_session).first()
		    # return fk.render_template('dashboard.html', user_model=user_model)
		    return fk.redirect('http://localhost:8080/ddsm-frontend/dashboard.html?session=%s'%hash_session)
		else:
			return fk.redirect('http://localhost:8080/ddsm-frontend/')

# @app.route('/dashboard/<objectid:id>')
# def dashboard_view(id):
#     user_model = UserModel.objects.with_id(id)
#     print user_model.api_token
#     return fk.render_template('dashboard.html', user_model=user_model)

# @app.route('/cloud')
# def cloud_view():
#     (user_model, created) = UserModel.objects.get_or_create(email=user.email)
#     user_model.renew()
#     print user_model.session
#     print user_model.api_token
#     return fk.redirect('http://127.0.0.1:8080/binder/javascript/?token=%s'%user_model.api_token)