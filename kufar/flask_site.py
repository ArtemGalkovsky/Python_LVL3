from flask import Flask, render_template, request, redirect
from db import database
from os import listdir
from tg import IMAGES_FOLDER, send_post as bot_send_post, get_bot
from asyncio import run

app = Flask(__name__)


@app.route("/")
def index():
    posts = database.moderation_posts.get_all_posts_on_moderation()

    images = {post[0]: listdir(f"{IMAGES_FOLDER}/{post[0]}") for post in posts}

    return render_template("moderation.html", posts=posts, images=images)


@app.route("/delete", methods=["POST"])
def decline_post():
    async def send_decline_post_tg_message():
        await (await get_bot()).send_message(data[1],
                                             f"ПОСТ {data[2]} с описанием {data[3]}, \n\n\n<b>НЕ ПРОШЁЛ ПРОВЕРКУ! ("
                                             f"Удалён)</b>")

    post_unique_id = request.args.get("uniqueid")

    data = database.moderation_posts.get_post_data_by_post_id(post_unique_id)
    database.moderation_posts.remove(post_unique_id)

    run(send_decline_post_tg_message())


@app.route("/send", methods=["POST"])
def send_post():
    async def send_post_to_tg():
        await bot_send_post(post_unique_id)
        await (await get_bot()).send_message(data[1],
                                             f"ПОСТ {data[2]} с описанием {data[3]}, \n\n\n<b>ПРОШЁЛ ПРОВЕРКУ! ("
                                             f"Отправлен)</b>")

    post_unique_id = request.args.get("uniqueid")

    data = database.moderation_posts.get_post_data_by_post_id(post_unique_id)

    run(send_post_to_tg())
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
