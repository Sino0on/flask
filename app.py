from flask import Flask, url_for, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ijzlpuphreujlh:e11bef18740061b989440cde9c4a11a8241c2e5d65ee6ce0ae9590d528077bc8@ec2-63-34-223-144.eu-west-1.compute.amazonaws.com:5432/dc3ehfbft7bif'
app.config['SQLALCHAMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    intro = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Article %r>' % self.id

@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date).all()
    return render_template('posts.html', articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article = article)

@app.route('/posts/<int:id>/del')
def post_del(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        print('dasdasd')

@app.route('/posts/<int:id>/red', methods = ['POST', 'GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            print('dasdasd')

    else:
        article = Article.query.get(id)
        return render_template('post_update.html', article = article)



@app.route('/create-article', methods = ['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title = title, intro = intro, text = text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            print('dasdasd')

    else:
        return render_template('create-article.html')


if __name__ == '__main__':
    app.run()
