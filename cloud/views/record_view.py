from cloud import app

@app.route('/record/view/<objectid:id>')
def record_view(id):
    return 'record for {0}'.format(id)
