from boggle import Boggle
from flask import Flask, redirect, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import os.path

app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "32j54hwcon49s1k"

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

guesses = []


def dir_last_updated(folder):
    return str(max(os.path.getmtime(os.path.join(root_path, f))
                   for root_path, dirs, files in os.walk(folder)
                   for f in files))
# credit: MarredCheese at https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
# is used to automatically update static files without having to hard refresh the browser for every change :D

@app.route("/")
def root():
    """root directory"""
    if (session.get("board", False) == False):
        session["board"] = boggle_game.make_board()
    else:
        boggle_game.board = session["board"]
    guesses.clear()
    print(boggle_game.board)
    session["h_score"] = session.get("h_score", 0)
    return render_template("base.html", board=session["board"], h_score=session["h_score"], last_updated=dir_last_updated("static"))

@app.route("/check")
def check_valid_word():
    """route that checks if words are valid and on the board"""
    word = request.args["word"].lower()
    if (guesses.count(word) != 0):
        return jsonify({'result': 'already-guessed'})
    else:
        guesses.append(word)
    check = boggle_game.check_valid_word(request.args["word"])
    return jsonify({'result': check})

@app.route("/gameover", methods=["POST"])
def end_game():
    """updates highscore"""
    if (int(session["h_score"]) < int(request.args["score"])):
        session["h_score"] = int(request.args["score"])
    return jsonify({'result': 'ok'})


# print(boggle_game.check_valid_word("melt"))