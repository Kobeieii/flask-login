from flask import Flask,jsonify,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy #query ได้ด้วย python
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user #usermixin เป็นตัวช่วยบอกว่าอันไหนคือ user

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.secret_key = '472b053e4442084fd6e879e9'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app) #ผูก login manager ไว้กับระบบนี้
login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): #กำหนดแต่ละ col
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False) #unique=true ซ้ำกันได้ null=false ไม่ให้ว่าง
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    return '<h1>Hello</h1>'

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/api/login_submit', methods=['POST'])
def login_submit():
    # print(request.form) #แสดง request ที่ส่งมา
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    # print(username)
    # print(user)
    if user:
        if user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            # print('1')
            return redirect(url_for('login'))
    else:
        # print('2')
        return redirect(url_for('login'))
    # return jsonify(request.form) #แสดง request ที่ส่งมา

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({'message': 'Logout success'})

if __name__ == "__main__":
    app.run(debug=True)
