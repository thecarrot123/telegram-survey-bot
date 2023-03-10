import os
from flask import Flask
from models import *

app = Flask(__name__)
env_config = os.getenv("APP_SETTINGS","flask_config.DevelopmentConfig")
app.config.from_object(env_config)
db.init_app(app)

def start(chat_id, alias):
    with app.app_context():
        user = User.query.filter_by(chat_id=chat_id).first()
        if user is None:
            user = User (
                chat_id = chat_id,
                alias = alias,
            )
            db.session.add(user)
        else:
            user.alias = alias
        db.session.commit()
        return f"Hello {user.alias}! Use </help> to get help."

def ask(chat_id, message):
    with app.app_context():
        message = message.split(' ',1)
        if len(message) == 1:
            return "Write your question after </ask>"
        question_text = message[1]
        user = User.query.filter_by(chat_id=chat_id).first()
        if user is None:
            return "Unregister user"
        new_question = Question(
            text = question_text,
            owner = user.id,
        )
        db.session.add(new_question)
        db.session.commit()
        return f"Question token: {new_question.id}"
        
def messageHandler(chat_id, message):
    with app.app_context():
        user = User.query.filter_by(chat_id=chat_id).first()
        if user is None:
            return "Unregister user"
        if user.answering is None:
            question = Question.query.filter_by(id=message).first()
            if question is None:
                return "Invalid token. Use </help> for more info."
            else:
                user.answering = question.id
                db.session.commit()
                return question.text
        else:
            question = Question.query.filter_by(id=user.answering).first()
            if question is None:
                return "Invalid question token. Use </help> for more info."
            answer = Answer.query.filter_by(user_id=user.id, question_id=question.id).first()
            if answer is None:
                answer = Answer(
                    user_id = user.id,
                    question_id = question.id,
                    text = message,
                )
                db.session.add(answer)
            else:
                answer.text = message
            user.answering = None
            db.session.commit()
            return "Answer saved!"

def collectAnswers(chat_id, message):
    with app.app_context():
        if len(message) == 1:
            return "Use <\help>"
        question_id = message[1]
        question = Question.query.filter_by(id=question_id).first()
        if question is None:
            return "Invalid question token."
        user = User.query.filter_by(chat_id=chat_id).first()
        if question.owner != user.id:
            return "Permission denied."
        answers = Answer.query.filter_by(question_id=question_id)
        reply = "Answers:\n"
        for answer in answers:
            reply += f" {answer.answered_by.alias}: {answer.text}\n"
        return reply

def testCollect():
    user = User.query.filter_by(alias="MURH4F").first()
    message = "/collect 2".split(' ',1)
    testAns = collectAnswers(user.chat_id, message)
    correctAns = """Answers:\n MURH4F: asd\n StiveMan1: yep\n"""
    return (testAns == correctAns)

def runTests():
    with app.app_context():
        print("Testing...")
        tests = []
        tests.append(testCollect())
        failed = False
        for test in tests:
            if test:
                print('.')
            else:
                print('!')
                failed = True
        if failed:
            print("Tests Failed.")
        else:
            print("Okay!")
        exit(failed)

@app.route("/")
def hello_world():
    return "<h1> hello world </h1>"


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
