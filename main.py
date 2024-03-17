from flask import Flask, render_template, request, redirect
from db import databases


app = Flask(__name__, template_folder="www", static_folder="www")


@app.route("/files/<path:path>")
def redirection_for_files(path: str):
    return redirect("/www/files/" + path)


@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html", all_names=databases.nature_reserves.get_all_names())


@app.route("/<name>")
def reserve(name: str):
    names = databases.nature_reserves.get_all_names()

    if name in names:
        data = databases.nature_reserves.get_reserve_data_by_name(name)
        return render_template("reserve.html", name=data[1], preview=data[2],
                               images=data[4], description=data[3], all_names=databases.nature_reserves.get_all_names())

    return "Такого нет..."

@app.route("/photo.html")
def gallery():
    return render_template("photo.html")


@app.route("/quiz.html")
def quiz():
    return render_template("quiz.html")


if __name__ == '__main__':
    app.run(debug=True)
