import os
from flask import Flask,render_template,url_for,request,jsonify
from agents.src.JD_embeddings import job_embedding
from agents.src.agents import call_agent

#defining frontendpath
temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'frontend','templates')
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'frontend','static')
resumes_dir = os.path.join(os.path.dirname(__file__),"resumes")


#flask init...zation
application = Flask(__name__,template_folder=temp_dir,static_folder=static_dir)
app = application

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/job_desc',methods=["POST"])
def job_desc():
    data = request.get_json()
    job_desc_text = data.get("requirement","")
    job_desc_embedding = job_embedding(job_desc_text)
    if job_desc_embedding:
        print("embedding success")
    return jsonify({"status":"success"})

@app.route('/Review_panel',methods=["POST"])
def Review_panel():
    results = []
    if "resumes" not in request.files:
        return "No files are uploaded"
    files = request.files.getlist("resumes")
    for file in files:
        if file.filename.endswith(".pdf"):
            save_path = os.path.join(resumes_dir,file.filename)
            file.save(save_path)
            print(f"pdf are uploaded")
            resume_id = os.path.splitext(file.filename)[0]
            result = call_agent(resume_id,save_path)
            results.append(result)
    return f"results are : {results}"



    


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)