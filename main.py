from flask import Flask, render_template,redirect,url_for,request
from flask_bootstrap import Bootstrap5
import random
import smtplib
import os


EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')


participants = {
    'Bhavika': {'email': 'motabhavika@gmail.com', 'exclude': 'Mayur', 'giftee': ''},
    'Mayur': {'email': '1987mayur@gmail.com', 'exclude': 'Bhavika', 'giftee': ''},
    'Gezelle': {'email': 'aaa@gmail.com', 'exclude': 'Colin', 'giftee': ''},
    'Colin': {'email': 'aaa@gmail.com', 'exclude': 'Gezelle', 'giftee': ''},
    'Priya': {'email': 'aaa@gmail.com', 'exclude': 'Lalit', 'giftee': ''},
    'Lalit': {'email': 'aaa@gmail.com', 'exclude': 'Priya', 'giftee': ''},
    'Pritam': {'email': 'aaa@gmail.com', 'exclude': 'Pratiksha', 'giftee': ''},
    'Pratiksha': {'email': 'aaa@gmail.com', 'exclude': 'Pritam', 'giftee': ''},
}

santa_list = []
giftee_list = []
for person in participants:
    santa_list.append(person)
    giftee_list.append(person)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/santa',methods=['POST', 'GET'])
def assign():
    global santa_list
    global giftee_list
    global participants
    new_giftee_list = []
    # assignment
    for i in range(len(santa_list)):
        santa = santa_list[i]
        giftee = random.choice(giftee_list)
        count = 0
        while santa == giftee or giftee == participants[santa]['exclude']:
            giftee = random.choice(giftee_list)
            count += 1
            if count > 100:
                print('Rerun')
            break
        giftee_list.remove(giftee)
        new_giftee_list.append(giftee)
    i = 0
    for person in participants:
        participants[person]['giftee'] = new_giftee_list[i]
        i += 1

    if request.method == 'POST':
        name = request.form['name'].title()
        email = participants[name]['email']
        buddy = participants[name]['giftee']

    return redirect(url_for('send_mail', name=name, email=email, buddy=buddy))

@app.route('/players')
def show_list():
    return render_template('list.html', list=santa_list)


@app.route('/mailed')
def send_mail():
    name = request.args.get('name')
    email = request.args.get('email')
    buddy = request.args.get('buddy')
    with smtplib.SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(EMAIL, PASSWORD)
        connection.sendmail(
            from_addr= EMAIL,
            to_addrs= email,
            msg=f"Subject:Secret Santa\n\n "
                f"Hello {name},\n "
                f"You are the secret santa of {buddy} .\n"
                f"Remember the budget is 50SEK.\n MERRY cHRISTMAS!"
        )
    return render_template('mail.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
