from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(db.Integer(), nullable=False)
    alias = db.Column(db.String(length=50), nullable=True)
    answering = db.Column(db.Integer(), default=None, nullable=True)
    questions = db.relationship('Question', backref='asked_by', lazy=True)
    answers = db.relationship('Answer', backref='answered_by', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(length=1000))
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
    answers = db.relationship('Answer', backref='answers', lazy=True)

class Answer(db.Model):
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    question_id = db.Column(db.Integer(), db.ForeignKey('question.id'), primary_key=True)
    text = db.Column(db.String(length=1000))
