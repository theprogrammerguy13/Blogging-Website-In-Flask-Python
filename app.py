from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Blog(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(100),nullable=False)
	author_name = db.Column(db.String(100),nullable=False)
	content = db.Column(db.String(10000),nullable=False)
	date_created = db.Column(db.DateTime,default=datetime.utcnow)
	def __repr__(self):
		return '<Task %r>' % self.id
@app.route('/', methods=['GET','POST'])
def main():
	posts = Blog.query.order_by(Blog.id.desc()).all()
	return render_template('home.html',posts=posts)
# def delete():
# 	id = 1
# 	task_to_delete = Blog.query.get(id)
# 	try:
# 		db.session.delete(task_to_delete) 
# 		db.session.commit()
# 		return redirect('/')
# 	except:
# 		return "There was a problem deleting that task. Try again later."
@app.route('/contact', methods=['GET','POST'])
def contact():
	if request.method == 'POST':
		req = request.form
		name = req['name']
		email = req['emailid']
		text = req['msgtext']
		phone_number = req['number']
		try:
			server = smtplib.SMTP("smtp.gmail.com",587)
			server.starttls()
			server.login("sayantannandi9e1roll21@gmail.com", "hellodexter")
			server.sendmail(email,"sayantannandi9e1roll21@gmail.com",f"{name}({email}) says {text}")
			server.quit()
			return redirect('/contact')
		except:
			return "There was a problem in sending your message"
	else:
		return render_template('contact.html')
@app.route('/search', methods=['GET','POST'])
def search():
	if request.method == 'POST':
		req = request.form
		search_text = req['query']
		posts = Blog.query.order_by(Blog.date_created).all()
		return render_template('search.html', posts=posts, search_text=search_text)
	else:
		return redirect('/')

@app.route('/blogpost/<int:id>', methods=['GET','POST'])
def post(id):
	post = Blog.query.get(id)
	return render_template('post.html',post=post)
@app.route('/about')
def about():
	return render_template('about.html')
@app.route('/createpost', methods=['GET','POST'])
def createpost():
	if request.method == 'POST':
		req = request.form
		text = req['msgtext']
		name = req['name']
		title = req['title']
		new_post = Blog(title=title,author_name=name,content=text)
		try:
			db.session.add(new_post)
			db.session.commit()
			return redirect('/createpost')
		except:
			return "There was a problem uploading your post"
	else:
		return render_template('createpost.html')
if __name__ == '__main__':
	app.run(debug=True)
