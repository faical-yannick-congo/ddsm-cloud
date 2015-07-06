from ddsmdb.common.models import UserModel
from ddsmdb.common.models import ProjectModel
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
from cloud import load_image
import mimetypes

CLOUD_VERSION = 1
CLOUD_URL = '/cloud/v{0}'.format(CLOUD_VERSION)


@app.route(CLOUD_URL + '/<hash_session>/project/dashboard', methods=['GET'])
@crossdomain(origin='*')
def project_dashboard(hash_session):
	if fk.request.method == 'GET':
		current_user = UserModel.objects(session=hash_session).first()
		print fk.request.path
		if current_user is None:
			return fk.redirect('http://52.26.127.180:5000/?action=logout_denied')
		else:
			allowance = current_user.allowed("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
			print "Allowance: "+allowance
			if allowance == hash_session:
				projects = ProjectModel.objects(owner=current_user).order_by('+created_at')
				summaries = []
				for p in projects:
					project = {"project":json.loads(p.summary_json())}
					records = RecordModel.objects(project=p)
					project["activity"] = {"number":len(records), "records":[{"id":str(record.id), "created":str(record.created_at)} for record in records]}
					summaries.append(project)
				return fk.Response(json.dumps({'number':len(summaries), 'projects':summaries}), mimetype='application/json')
			else:
				return fk.redirect('http://52.26.127.180:5000/?action=update_failed')
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

@app.route(CLOUD_URL + '/<hash_session>/project/record/<project_name>', methods=['GET'])
@crossdomain(origin='*')
def project_records(hash_session, project_name):
	if fk.request.method == 'GET':
		current_user = UserModel.objects(session=hash_session).first()
		print fk.request.path
		if current_user is None:
			return fk.redirect('http://52.26.127.180:5000/?action=logout_denied')
		else:
			allowance = current_user.allowed("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
			print "Allowance: "+allowance
			if allowance == hash_session:
				project = ProjectModel.objects(owner=current_user, name=project_name).first_or_404()
				return fk.Response(project.activity_json(), mimetype='application/json')
			else:
				return fk.redirect('http://52.26.127.180:5000/?action=update_failed')
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)

@app.route(CLOUD_URL + '/<hash_session>/record/pull/<project_name>/<record_id>', methods=['GET'])
@crossdomain(origin='*')
def pull_record(hash_session, project_name, record_id):
	if fk.request.method == 'GET':
		current_user = UserModel.objects(session=hash_session).first()
		print fk.request.path
		if current_user is None:
			return fk.redirect('http://52.26.127.180:5000/?action=logout_denied')
		else:
			allowance = current_user.allowed("%s%s"%(fk.request.headers.get('User-Agent'),fk.request.remote_addr))
			print "Allowance: "+allowance
			if allowance == hash_session:
				try:
					record = RecordModel.objects.with_id(record_id)
					project = ProjectModel.objects.with_id(record.project.id)
					if (project.name == project_name) and ((project.private and (project.owner == current_user)) or (not project.private)):
						if record.container:
							container = record.container
							if container.image['location']:
								image = load_image(record)
								# print image[1]
								return fk.send_file(
									image[0],
									mimetypes.guess_type(image[1])[0],
									as_attachment=True,
									attachment_filename=str(current_user.id)+"-"+project_name+"-"+str(record_id)+"-record.zip",
								)
							else:
								print "Failed because of container location not found."
								return fk.make_response('Empty location. Nothing to pull from here!', status.HTTP_204_NO_CONTENT)
						else:
							print "No container image."
							return fk.make_response('No container image. Nothing to pull from here!', status.HTTP_204_NO_CONTENT)
					else:
						print "Project name and Record id not match."
						return fk.make_response('Pull failed.', status.HTTP_401_UNAUTHORIZED)
					# return fk.Response(project.activity_json(), mimetype='application/json')
				except:
					print traceback.print_exc()
					print "Exception occured."
					return fk.make_response('Pull failed.', status.HTTP_401_UNAUTHORIZED)
			else:
				return fk.redirect('http://52.26.127.180:5000/?action=update_failed')
	else:
		return fk.make_response('Method not allowed.', status.HTTP_405_METHOD_NOT_ALLOWED)