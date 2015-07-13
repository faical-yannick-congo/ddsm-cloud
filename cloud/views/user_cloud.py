from ddsmdb.common.models import UserModel
from ddsmdb.common.models import ProjectModel
from ddsmdb.common.models import ContainerModel
from ddsmdb.common.models import RecordModel
from flask.ext.stormpath import user
from flask.ext.stormpath import login_required
from flask.ext.api import status
import flask as fk
from cloud import app, stormpath_manager, crossdomain
import datetime
import json
import traceback
import smtplib
from email.mime.text import MIMEText
from hurry.filesize import size
import hashlib

CLOUD_VERSION = 1
CLOUD_URL = '/cloud/v{0}'.format(CLOUD_VERSION)

@app.route(CLOUD_URL + '/user/register', methods=['POST'])
@crossdomain(origin='*')
def user_register():
	if fk.request.method == 'POST':
		if fk.request.data:
			data = json.loads(fk.request.data)
			application = stormpath_manager.application
			email = data.get('email', '')
			password = data.get('password', '')
			username = data.get('username', '')
			if email == '' or '@' not in email or username == '':
				return fk.make_response("The email field cannot be empty.", status.HTTP_400_BAD_REQUEST)
			else:
				try:
					_user = application.accounts.create({
						'email': email,
						'password': password,
						"username" : username,
						"given_name" : "Empty",
						"middle_name" : "Empty",
						"surname" : "Empty"
					})
					while True:
						try:
							# Many trials because of API key generation failures some times.
							(user_model, created) = UserModel.objects.get_or_create(email=email, api_token=hashlib.sha256(b'DDSM%s_%s'%(email, str(datetime.datetime.now()))).hexdigest())
							break
						except:
							print str(traceback.print_exc())


					print "Token %s"%user_model.api_token
					print fk.request.headers.get('User-Agent')
					print fk.request.remote_addr
					user_model.renew("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
					print "Session: %s"%user_model.session
					return fk.Response(json.dumps({'session':user_model.session}), mimetype='application/json')
					# return fk.redirect('http://52.26.127.180:5000/%s'%user_model.session)
				except:
					print str(traceback.print_exc())
					return fk.make_response('This user already exists.', status.HTTP_401_UNAUTHORIZED)
		else:
			return fk.make_response("Missing mandatory fields.", status.HTTP_400_BAD_REQUEST)
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

@app.route(CLOUD_URL + '/user/login', methods=['POST'])
@crossdomain(origin='*')
def user_login():
	if fk.request.method == 'POST':
		print "Request: %s"%str(fk.request.data)
		if fk.request.data:
			data = json.loads(fk.request.data)
			application = stormpath_manager.application
			email = data.get('email', '')
			password = data.get('password', '')
			if email == '' or '@' not in email:
				return fk.make_response("The email field cannot be empty.", status.HTTP_400_BAD_REQUEST)
			else:
				try:
					_user = application.authenticate_account(
						email,
						password,
					).account
					account = UserModel.objects(email=email).first()
					print "Token %s"%account.api_token
					print fk.request.headers.get('User-Agent')
					print fk.request.remote_addr
					account.renew("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
					print "Session: %s"%account.session
					return fk.Response(json.dumps({'session':account.session}), mimetype='application/json')
					# return fk.redirect('http://52.26.127.180:5000/?session=%s'%account.session)
				except:
					print str(traceback.print_exc())
					return fk.make_response('Login failed.', status.HTTP_401_UNAUTHORIZED)
					
		else:
			return fk.make_response("Missing mandatory fields.", status.HTTP_400_BAD_REQUEST)
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

@app.route(CLOUD_URL + '/user/logout/<hash_session>', methods=['GET'])
@crossdomain(origin='*')
def user_logout(hash_session):
	if fk.request.method == 'GET':
		user_model = UserModel.objects(session=hash_session).first()
		print fk.request.path
		if user_model is None:
			return fk.redirect('http://52.26.127.180:5000/?action=logout_denied')
		else:
			allowance = user_model.allowed("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
			print "Allowance: "+allowance
			if allowance == hash_session:
				user_model.renew("%sLogout"%(fk.request.headers.get('User-Agent')))
				# return fk.redirect('http://52.26.127.180:5000/?action=logout_success')
				return fk.Response('Logout succeed', status.HTTP_200_OK)
			else:
				return fk.redirect('http://52.26.127.180:5000/?action=logout_failed')
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)


@app.route(CLOUD_URL + '/user/dashboard/<hash_session>', methods=['GET'])
@crossdomain(origin='*')
def user_dashboard(hash_session):
	if fk.request.method == 'GET':
		user_model = UserModel.objects(session=hash_session).first()
		print fk.request.path
		if user_model is None:
			return fk.redirect('http://52.26.127.180:5000/?action=logout_denied')
		else:
			allowance = user_model.allowed("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
			print "Allowance: "+allowance
			if allowance == hash_session:
				dashboard = {}
				projects = ProjectModel.objects(owner=user_model)
				dashboard["projects_total"] = len(projects)
				dashboard["records_total"] = 0
				dashboard["containers_total"] = 0
				dashboard["projects"] = []
				for project in projects:
					project_dash = {"name":project.name, "records":{"January":{"number":0, "size":0}, "February":{"number":0, "size":0}, "March":{"number":0, "size":0}, "April":{"number":0, "size":0}, "May":{"number":0, "size":0}, "June":{"number":0, "size":0}, "July":{"number":0, "size":0}, "August":{"number":0, "size":0}, "September":{"number":0, "size":0}, "October":{"number":0, "size":0}, "November":{"number":0, "size":0}, "December":{"number":0, "size":0}}}
					records = RecordModel.objects(project=project)
					dashboard["records_total"] += len(records)
					for record in records:
						container = record.container
						size = 0
						try:
							size = container.image["size"]
						except:
							size = 0

						dashboard["containers_total"] += size

						month = str(record.created_at).split("-")[1]
						if month == "01":
							project_dash["records"]["January"]["number"] += 1
							project_dash["records"]["January"]["size"] += size
						if month == "02":
							project_dash["records"]["February"]["number"] += 1
							project_dash["records"]["February"]["size"] += size
						if month == "03":
							project_dash["records"]["March"]["number"] += 1
							project_dash["records"]["March"]["size"] += size
						if month == "04":
							project_dash["records"]["April"]["number"] += 1
							project_dash["records"]["April"]["size"] += size
						if month == "05":
							project_dash["records"]["May"]["number"] += 1
							project_dash["records"]["May"]["size"] += size
						if month == "06":
							project_dash["records"]["June"]["number"] += 1
							project_dash["records"]["June"]["size"] += size
						if month == "07":
							project_dash["records"]["July"]["number"] += 1
							project_dash["records"]["July"]["size"] += size
						if month == "08":
							project_dash["records"]["August"]["number"] += 1
							project_dash["records"]["August"]["size"] += size
						if month == "09":
							project_dash["records"]["September"]["number"] += 1
							project_dash["records"]["September"]["size"] += size
						if month == "10":
							project_dash["records"]["October"]["number"] += 1
							project_dash["records"]["October"]["size"] += size
						if month == "11":
							project_dash["records"]["November"]["number"] += 1
							project_dash["records"]["November"]["size"] += size
						if month == "12":
							project_dash["records"]["December"]["number"] += 1
							project_dash["records"]["December"]["size"] += size

					dashboard["projects"].append(project_dash)

				return fk.Response(json.dumps(dashboard), mimetype='application/json')
			else:
				return fk.redirect('http://52.26.127.180:5000/?action=dashboard_failed')
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)


@app.route(CLOUD_URL + '/user/update/<hash_session>', methods=['POST'])
@crossdomain(origin='*')
def user_update(hash_session):
	if fk.request.method == 'POST':
		if fk.request.data:
			data = json.loads(fk.request.data)
			application = stormpath_manager.application()
			user_model = UserModel.objects(session=hash_session).first()
			print fk.request.path
			if user_model is None:
				return fk.redirect('http://52.26.127.180:5000/?action=update_denied')
			else:
				allowance = user_model.allowed("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
				print "Allowance: "+allowance
				if allowance == hash_session:
					#Update stormpath user if password is affected
					#Update local profile data and picture if other data are affected.
					return fk.redirect('http://52.26.127.180:5000/?action=update_success')
				else:
					return fk.redirect('http://52.26.127.180:5000/?action=update_failed')
		else:
			return fk.make_response("Missing mandatory fields.", status.HTTP_400_BAD_REQUEST)
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)


@app.route(CLOUD_URL + '/user/contactus', methods=['POST'])
@crossdomain(origin='*')
def user_contactus():
	if fk.request.method == 'POST':
		if fk.request.data:
			data = json.loads(fk.request.data)
			try:
				email = data.get("email", "")
				message = data.get("message", "")
				msg = MIMEText("Dear user,\n You contacted us regarding the following matter:\n-------\n%s\n-------\nWe hope to reply shortly.\nBest regards,\n\nDDSM team."%message)
				msg['Subject'] = 'DDSM -- You contacted us!'
				msg['From'] = "yannick.congo@gmail.com" # no_reply@ddsm.nist.gov
				msg['To'] = email
				msg['CC'] = "yannick.congo@gmail.com"
				s = smtplib.SMTP('localhost')
				s.sendmail("yannick.congo@gmail.com", email, msg.as_string())
				s.quit()
				return fk.Response('Logout succeed', status.HTTP_200_OK)
			except:
				print str(traceback.print_exc())
				return fk.make_response("Could not send the email.", status.HTTP_503_SERVICE_UNAVAILABLE)
		else:
			return fk.make_response("Missing mandatory fields.", status.HTTP_400_BAD_REQUEST)
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)


@app.route(CLOUD_URL + '/user/trusted/<hash_session>', methods=['GET'])
@crossdomain(origin='*')
def user_truested(hash_session):
	if fk.request.method == 'GET':
		user_model = UserModel.objects(session=hash_session).first()
		print fk.request.path
		if user_model is None:
			return fk.make_response('Trusting failed.', status.HTTP_401_UNAUTHORIZED)
		else:
			allowance = user_model.allowed("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
			print "Allowance: "+allowance
			if allowance == hash_session:
				return fk.Response('Trusting succeed', status.HTTP_200_OK)
			else:
				return fk.make_response('Trusting failed.', status.HTTP_401_UNAUTHORIZED)
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

@app.route(CLOUD_URL + '/user/home', methods=['GET'])
@crossdomain(origin='*')
def user_home():
	if fk.request.method == 'GET':
		users = UserModel.objects()
		projects = ProjectModel.objects()
		records = RecordModel.objects()
		containers = ContainerModel.objects()
		print fk.request.path

		users_stat = {"number":len(users)}
		users_stat["history"] = [str(user.created_at) for user in users]

		projects_stat = {"number":len(projects)}
		projects_stat["history"] = [str(project.created_at) for project in projects]

		containers_stat = {}
		containers_stat["history"] = [str(container.created_at) for container in containers]
		amount = 0
		for container in containers:
			try:
				amount += container.image["size"]
			except:
				amount += 0

		containers_stat["size"] = size(amount)

		records_stat = {"number":len(records)}
		records_stat["history"] = [str(record.created_at) for record in records]

		return fk.Response(json.dumps({'users':users_stat, 'projects':projects_stat, 'records':records_stat, 'containers':containers_stat}), mimetype='application/json')
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)


@app.route(CLOUD_URL + '/user/account/<hash_session>', methods=['GET'])
@crossdomain(origin='*')
def user_account(hash_session):
	if fk.request.method == 'GET':
		user_model = UserModel.objects(session=hash_session).first()
		print fk.request.path
		if user_model is None:
			return fk.make_response('Trusting failed.', status.HTTP_401_UNAUTHORIZED)
		else:
			return fk.Response(json.dumps({'username':'Empty for now', 'email':user_model.email, 'session':user_model.session, 'api':user_model.api_token}), mimetype='application/json')
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)


@app.route(CLOUD_URL + '/user/renew/<hash_session>', methods=['GET'])
@crossdomain(origin='*')
def user_renew(hash_session):
	if fk.request.method == 'GET':
		user_model = UserModel.objects(session=hash_session).first()
		print fk.request.path
		if user_model is None:
			return fk.make_response('Trusting failed.', status.HTTP_401_UNAUTHORIZED)
		else:
			allowance = user_model.allowed("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
			print "Allowance: "+allowance
			if allowance == hash_session:
				user_model.retoken()
				return fk.Response(json.dumps({'api':user_model.api_token}), mimetype='application/json')
			else:
				return fk.make_response('Trusting failed.', status.HTTP_401_UNAUTHORIZED)
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)
