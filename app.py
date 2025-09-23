from flask import Flask , redirect , render_template , session , request
from dotenv import load_dotenv
import os
import requests


app = Flask(__name__)
load_dotenv()
app.secret_key = '@SRIRAM_NPR'

API_URL = os.getenv("APIURL")

routes={
    "event":"Uevent.html",
    "recent":"Urecent.html",
    "outreach":"Uout.html",
    "gallery":"Ugallery.html"
}

Edit_Routes={
    "update-event":"EEvent.html",
    "update-recent":"ERecent.html",
    "update-outreach":"Eout.html",
    "update-gallery":"Egallery.html"
}

def check():
    try:
       
        res = requests.get(f'{API_URL}/api/auth/me', cookies=request.cookies)
        data = res.json()
        if(data.get("Success")):
            return True
        else:
            return False
    except Exception as e:
        print("Error in check():", e)
        return False


@app.route('/')
def Home():
    return render_template("main.html"  ,   API = API_URL)
   

@app.route("/gallery")
def Gallery():
    API = API_URL
    return render_template("gallery.html" , API=API)

@app.route("/outreach")
def Outreach():
    API = API_URL
    return render_template("out.html" , API=API)

@app.route("/recent")
def Recent():
    API = API_URL
    return render_template("recent.html" , API=API)


@app.route('/logout')
def Logout():
    session.clear()
    return redirect("/")

@app.route('/acm')
def acm():
    auth = session.get('isauth')
    if not auth:
      return render_template('index.html')
    else:
        return redirect("/")
    
@app.route('/upload/<c_name>')
def Uploads(c_name):

    get_value = routes[c_name]
    if get_value:
        if(c_name=='event'):
            return render_template(get_value , API=API_URL)
        elif(c_name=='recent'):
            return render_template(get_value , API=API_URL)
        elif(c_name=='outreach'):
            return render_template(get_value , API=API_URL)
        elif(c_name=='gallery'):
            return render_template(get_value , API=API_URL)
        else:
            return f'Invalid names avalible names : {routes} '
    else:
        return 'No names Found'

@app.route('/<name>/<id>')
def Update_Event(name , id):
    try:
        file = Edit_Routes[name]
        try:
         return render_template(file , Eid=id , name=name , API=API_URL)
        except KeyError:
            return 'Invalid Aruguments'
    except:
        return 'Internal Server Error'



if __name__ == "__main__":
    app.run(debug=True , port=1212)
