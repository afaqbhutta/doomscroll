from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from azure.storage.blob import BlobServiceClient
import uuid
import os

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)

# Blob Storage Client
blob_service_client = BlobServiceClient.from_connection_string(app.config['BLOB_CONNECTION_STRING'])
container_client = blob_service_client.get_container_client(app.config['BLOB_CONTAINER_NAME'])

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    blob_url = db.Column(db.String(500), nullable=False)

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['video']
        title = request.form['title']
        if file:
            blob_name = str(uuid.uuid4()) + "_" + file.filename
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(file, overwrite=True)
            blob_url = blob_client.url

            video = Video(title=title, blob_url=blob_url)
            db.session.add(video)
            db.session.commit()
            return redirect(url_for('watch', video_id=video.id))
    return render_template("upload.html")

@app.route("/video/<int:video_id>")
def watch(video_id):
    video = Video.query.get_or_404(video_id)
    return render_template("video.html", video=video)

if __name__ == "__main__":
    app.run(debug=True)
