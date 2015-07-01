from cloud import app
import flask as fk
import dashboard_cloud
import project_view
import record_view
import user_cloud
import project_cloud

@app.route('/')
@app.route('/index')
def index_view():
    return fk.render_template('index.html')

@app.route('/learn')
def learn_view():
    return fk.redirect(fk.url_for('index_view'))



