import os
from flask import Flask,render_template,url_for,request
from agents.src.JD_embeddings import job_embedding

#defining frontendpath
temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'frontend','templates')
# static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'frontend','static')


#flask init...zation
application = Flask(__name__,template_folder=temp_dir)
app = application

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/job_desc',methods=["POST"])
def job_desc():
    job_desc_text = request.form["job_description"]
    job_desc_embedding = job_embedding(job_desc_text)
    if job_desc_embedding:
        print("embedding success")
    return "job description success"




if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)