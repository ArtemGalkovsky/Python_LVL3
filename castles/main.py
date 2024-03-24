from flask import Flask, render_template, request, make_response, redirect
from db import databases
from json import loads, dumps
from uuid import uuid4
from datetime import timedelta
from time import time
from shutil import copyfile
from os import listdir, mkdir
from urllib.parse import unquote

STATIC_FOLDER = "www"
TEMP_FOLDER = f"{STATIC_FOLDER}/files/temp"

app = Flask(__name__, template_folder=STATIC_FOLDER, static_folder=STATIC_FOLDER)


def get_all_castles_names_and_urls():
    castle_names_and_urls = []

    for castle in databases.castles.get_all_castles_names():
        castle_id = databases.castles.get_castle_id(castle)
        preview = databases.castles.get_preview(castle_id)

        castle_names_and_urls.append((castle, preview[-1]))
    return castle_names_and_urls


@app.route("/index.html")
@app.route("/")
def index():
    all_castles_preview = []

    all_castles_names = databases.castles.get_all_castles_names()
    for castle in all_castles_names:
        castle_id = databases.castles.get_castle_id(castle)
        preview = databases.castles.get_preview(castle_id)

        all_castles_preview.append(preview)

    return render_template("index.html", previews=all_castles_preview,
                           castle_names=get_all_castles_names_and_urls())


@app.route("/quiz.html")
def quiz():
    return render_template("quiz.html", castle_names=get_all_castles_names_and_urls())


@app.route("/photos.html")
def gallery():
    all_castles_images = []

    for castle_name in databases.castles.get_all_castles_names():
        castle_id = databases.castles.get_castle_id(castle_name)
        all_castles_images.extend(databases.castles.get_images(castle_id))

    return render_template("photos.html", all_images=all_castles_images,
                           castle_names=get_all_castles_names_and_urls())


@app.route("/check_login_credentials", methods=["POST"])
def check_login_credentials():
    login_data_json = loads(request.data)
    login = login_data_json["login"]
    password_hash = login_data_json["passwordHash"]

    print(password_hash, "PH", login)
    if databases.admins.is_admin(login, password_hash):
        session_id = uuid4().hex
        expiration_delta = timedelta(days=1)
        expiration_timestamp = time() + expiration_delta.total_seconds()

        databases.sessions.add_session(login, session_id, expiration_timestamp)

        response = make_response("TRUE")
        response.set_cookie("session_id", session_id, expiration_delta)
        response.set_cookie("login", login, expiration_delta)

        return response

    return "FALSE"


@app.route("/favicon.ico")
def ico():
    return ""


@app.route("/load", methods=["POST"])
def load_castle_data():
    castle_url = unquote(request.data.decode("utf-8"))

    try:
        castle_name = databases.castles.get_castle_name_by_url(castle_url)
    except:
        return dumps({"msg": "Такого замка нет!"})

    castle_id = databases.castles.get_castle_id(castle_name)

    images = databases.castles.get_images(castle_id)
    paragraphs = databases.castles.get_paragraphs(castle_id)
    preview = databases.castles.get_preview(castle_id)

    return dumps({
        "images": images,
        "paragraphs": paragraphs,
        "preview": preview
    })


def check_if_castle_image_folder_exists(page: str, image_folder: str) -> bool:
    return page in listdir(image_folder)


def refactor_image_url(image_url: str, request) -> str:
    return image_url.replace(request.url_root, "").replace(STATIC_FOLDER, "").replace("//", "")


def get_new_image_url(image_url: str, page: str):
    if "files/temp" in image_url:
        image_folder = f"{app.static_folder}/files/img"
        new_image_folder = f"{app.static_folder}/files/img/{page}/"

        if not check_if_castle_image_folder_exists(page, image_folder):
            mkdir(image_folder + "/" + page)

        new_image_location = new_image_folder.replace(app.static_folder + "/", "") + image_url.split("/")[-1]

        copyfile(
            f"{app.static_folder}/{image_url}",
            f"{app.static_folder}/{new_image_location}"
        )

        return new_image_location

    return image_url


@app.route("/save", methods=["POST"])
def save_data():
    json = request.json

    page = json["id"]
    title = json["title"]
    description = json["description"]
    preview = get_new_image_url(refactor_image_url(json["preview"], request), page)
    paragraphs = json["paragraphs"]
    images = json["images"]
    images_refactored_urls = []

    for image in images:
        image_url = refactor_image_url(image, request)
        images_refactored_urls.append(get_new_image_url(image_url, page))
    try:
        databases.castles.update_castle_data(page, title, description, preview, paragraphs, images_refactored_urls)
    except Exception as e:
        print("SAVE EXCEPTION", e)
        return "ERROR"

    return "OK"


@app.route("/create_castle", methods=["POST"])
def create_castle():
    json = request.json

    databases.castles.add_castle(json["title"], "", "", json["page"], [], [])

    return "OK"


@app.route("/delete_castle", methods=["POST"])
def delete_castle():
    page = request.data.decode("UTF-8")

    databases.castles.delete(page)

    return "OK"


@app.route("/admin_panel")
def admin_panel():
    if databases.sessions.is_session_active(request.cookies.get("login"), request.cookies.get("session_id")):
        return render_template("admin_panel.html",
                               castle_names=get_all_castles_names_and_urls(),
                               is_admin_panel=1)

    return redirect("/")


@app.route("/download_to_temp", methods=["POST"])
def download_temp_image():
    file = request.data
    name = request.args.get("name")

    if file and name:
        name = f"{uuid4()}{name}"

        with open(TEMP_FOLDER + "/" + name, "wb") as fl:
            fl.write(file)

    return TEMP_FOLDER + "/" + name


@app.route("/sign_out", methods=["POST", "GET"])
def sign_out():
    session_id = request.cookies.get("session_id")
    login = request.cookies.get("login")

    databases.sessions.remove_session(login, session_id)

    return redirect("/")


@app.route("/admin_panel_login")
def admin_panel_login():
    if databases.sessions.is_session_active(request.cookies.get("login"), request.cookies.get("session_id")):
        return redirect("/admin_panel")

    return render_template("admin_login.html")


@app.route("/<castle_url>")
def return_castle_html(castle_url: str):
    castle_url = castle_url.replace(".html", "")

    try:
        castle_name = databases.castles.get_castle_name_by_url(castle_url)
        castle_id = databases.castles.get_castle_id(castle_name)

        castle_data = databases.castles.get_preview(castle_id)
        paragraphs = databases.castles.get_paragraphs(castle_id)
        images = databases.castles.get_images(castle_id)

        return render_template("castles_descriptions.html",
                               castle_data=castle_data,
                               paragraphs=paragraphs,
                               images=images,
                               castle_names=get_all_castles_names_and_urls())
    except Exception as e:
        print(e)
        return "Замок не найден", 404


if __name__ == '__main__':
    app.run(debug=True)
