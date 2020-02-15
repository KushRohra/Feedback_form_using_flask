from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'prod':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kush5255@localhost/feedback_form_using_flask'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://aozppfoagneyoa:216f4408b030695f2616f2dbee2bf0effee37146665904143da4c208dce315d4@ec2-3-234-109-123.compute-1.amazonaws.com:5432/d6v0m39e1ob3t6'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text)

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        #print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message="Please enter required fields")

        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            #does not run on a proxy server
            #send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message="You have already submitted feedback")

if __name__ == '__main__':
    app.run()
