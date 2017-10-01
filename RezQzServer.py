from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
import dataset

app = Flask (__name__)

@app.route("/")
def login():
    return redirect("/members", code=302)

@app.route("/members")
def members():
    return redirect("/members/jill", code=302)

@app.route("/members/<string:name>/")
def getMember(name):

    db = dataset.connect('sqlite:///mydatabase.db')

    dogset = db.query("SELECT dog FROM user_table WHERE name ='"+name+"'")
    dog_dict = next((x for x in dogset), None)
    dog_name = dog_dict["dog"]

    id_set = db.query("SELECT id FROM user_table WHERE name ='"+name+"'")
    id_dict = next((x for x in id_set), None)
    id = id_dict["id"]

    message_set = db.query("SELECT message FROM message_table WHERE user_id = " + str(id))


    return render_template('members.html', **locals())

@app.route("/message_post", methods=['POST'])
def submitMessage():
    data = request.form.get('transmission')
    id = request.form.get('hidden_id')
    db = dataset.connect('sqlite:///mydatabase.db')

    table = db['message_table']
    table.insert(dict(message=data, user_id=id))
    return redirect("/members")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

