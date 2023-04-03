from flask import Flask, render_template, redirect, request, session
import pymongo
import os
from werkzeug.utils import secure_filename
import certifi
import time
import datetime
from datetime import date
import calendar
from bson.objectid import ObjectId

UPLOAD_FOLDER = 'D:\\Web Projects\\Club Manager hackathon\\static\\user_uploads'

connectionString = "mongodb://Northstar:UYdGLGJ5qHpu9QBe@information-shard-00-00.aqqbz.mongodb.net:27017,information-shard-00-01.aqqbz.mongodb.net:27017,information-shard-00-02.aqqbz.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-hjmyx7-shard-0&authSource=admin&retryWrites=true&w=majority"
client = pymongo.MongoClient(connectionString, tlsCAFile=certifi.where())
database = client["Clubs"]
events = database["Events"]
users = database["Users"]

app = Flask("Clubs")
app.config['SECRET_KEY']='13579qwertyasdf8642'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=['GET','POST'])
def login():
    session['Week'] = str(date.today())
    if 'Success' not in session:
        if (request.method == 'GET'):
            event = events.find({})
            event = list(event)
            for e in event:
                if not (str(e['Date']).split("-")[0] == (session['Week'].split("-")[0]) or int(str(e['Date']).split("-")[1])>=int(session['Week'].split("-")[1])):
                    event.remove(e)
            event1 = []
            event2 = []
            for i in event:
                tim = i['Time']
                tim = int(tim.split(':')[0])
                print(tim)
                if(tim<12):
                    event1.append(i)
                else:
                    event2.append(i)
            return render_template('index.html', events=event, events1=event1, events2=event2)
        else:
            doc = dict(request.form)
            print(doc)
            if ('Login' in doc):
                d = users.find_one({'Email':doc['Email'], 'Pass':doc['Pass']})
                if d is not None:
                    session['Success'] = True
                    session['Name'] = d['Name']
                    session['Email'] = d['Email']
                    session['Pic'] = d['Pic']
                    return redirect('/home')
            else:
                file = request.files['Image']
                if len(file.filename)>0:
                    print(request.files['Image'])
                    name = doc['Email'] + str(time.time()) + secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
                else:
                    name = 'Generic-Profile-1600x1600-550x550.png'
                users.insert_one({'Name':doc['Name'], 'Email':doc['Email'], 'Pass':doc['Pass'], 'Pic':name})
            return redirect('/')
    return redirect('/home')

@app.route('/home', methods=['GET','POST'])
def home():
    if (request.method == 'GET'):
        event = events.find({})
        event = list(event)
        for e in event:
            if  (str(e['Date']).split("-")[0] < session['Week'].split("-")[0] or int(str(e['Date']).split("-")[1])<int(session['Week'].split("-")[1])):
                event.remove(e)
        event1 = []
        event2 = []
        for i in event:
            tim = i['Time']
            tim = int(tim.split(':')[0])
            print(tim)
            if(tim<12):
                event1.append(i)
            else:
                event2.append(i)
        return render_template('home.html', events=event, events1=event1, events2=event2)
    else:
        doc=dict(request.form)
        print(doc)
        times = doc['Time'].split('T')
        if 'Lead' in doc and doc['Lead'] == 'on':
            who = "Club Leaders Only"
        else:
            who = "Everyone"
        events.insert_one({"Title":doc['Title'], 'Desc':doc['Content'],'Date':times[0], 'Time':times[1], 'Day':findDay(times[0].replace('-'," ")), 'Allowed':who})
        return redirect("/")


def findDay(date):
    born = datetime.datetime.strptime(date, '%Y %m %d').weekday()
    return (calendar.day_name[born])

@app.route('/<event_id>', methods=['GET','POST'])
def event(event_id):
    if request.method == 'GET':
        event = events.find_one({"_id":ObjectId(event_id)})
        return render_template('event.html', event=event)
    else:
        doc=dict(request.form)
        print(doc)
        times = doc['Time'].split('T')
        if 'Lead' in doc and doc['Lead'] == 'on':
            who = "Club Leaders Only"
        else:
            who = "Everyone"
        events.insert_one({"Title":doc['Title'], 'Desc':doc['Content'],'Date':times[0], 'Time':times[1], 'Day':findDay(times[0].replace('-'," ")), 'Allowed':who})
        return redirect("/")

@app.route('/edit-profile', methods = ['GET', 'POST'])
def edit():
    if request.method == 'GET':
        d = users.find_one({'Email':session['Email']})
        return render_template('edit-profile.html', d=d)
    else:
        user = users.find_one({"Email":session['Email']})
        d = dict(request.form)
        if 'CPass' in d and user['Pass'] == d['CPass']:
            if 'Image' in d:
                file = request.files['Image']
                name = session['Email'] + str(time.time())+ secure_filename(file.filename) 
                name = name.replace(" ","-")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
                users.update_one(user,{'$set':{'Pic':name}})
            if 'NName' in d and len(d['NName']) >= 0:
                users.update_one(user,{'$set':{'Name':d['NName']}})
            if 'NPass' in d and 'NPassConf' in d and d['NPass'] == d['NPassConf']:
                users.update_one(user,{'$set':{'Pass':d['NPass']}})
            return redirect('/')

@app.route('/get-data', methods = ['GET', 'POST'])
def getData():
    if request.method == 'GET':
        return {"Text":"This is a value of text"}
    else:
        d = request.form.to_dict()
        user = users.find_one({'Email':session['Email']})
        if(len(d['CPass'])>0 and d['CPass'] == user['Pass']):
            print(d)
            if('Image' in request.files):
                file = request.files['Image']
                if(len(file.filename)>0):
                    name = session['Email'] + str(time.time())+ secure_filename(file.filename) 
                    name = name.replace(" ","-")
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], name))
                    users.update_one(user,{'$set':{'Pic':name}})
            if(len(d['NName'])>0):
                users.update_one(user,{'$set':{'Name':d['NName']}})
            if(d['NPass']==d['NPassConf'] and len(d['NPass'])>0):
                users.update_one(user,{'$set':{'Pass':d['NPass']}})
            elif(len(d['NPass'])==0 and len(d['NPassConf'])==0):
                pass
            else:
                return 'nomatch'
            return "Success"
        elif(len(d['CPass'])<=0):
            return 'nopass'
        elif(d['CPass'] != user['Pass']):
            return 'wrongpass'
        
@app.route('/delete-event/<event_id>')
def delete_event(event_id):
    events.delete_one(events.find_one({'_id':ObjectId(event_id)}))
    return redirect('/')

@app.route('/logout')
def logout():
    session['Success'] = False
    session.clear()
    return redirect('/')
    
app.run(debug=True, port=8080)