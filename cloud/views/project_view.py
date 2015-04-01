import flask as fk
from cloud import app
from ddsmdb.common.models import ProjectModel
from ddsmdb.common.models import RecordModel

@app.route('/project/view/<objectid:id>')
def project_view(id):
    project = ProjectModel.objects.with_id(id)
    records = RecordModel.objects(project=project)
    return fk.render_template('project.html', project=project, records=records, user=project.user)

