from datetime import datetime
"""
Класс описывает публикацию от пользователя в сети. Конструктор класса получает автора, устанавливает время, а для комментариев создает списочный массив.
Свойства класса:
никнейм пользователя,
время публикации (пример в занятии),
количество лайков,
текст сообщения,
список комментариев.
Методы класса:
like() – увеличивает количество лайков,
dislike() – уменьшает количество лайков,
add_comment(comment_text) – добавляет комментарий,
all_comments() – выводит все комментарии.
"""


class Post:

  def __init__(self, author: str, text: str) -> None:
    self.author: str = author
    self.published_time: str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    self.likes_count: int = 0
    self.text: str = text
    self.comments = []

    print(f"New post created: {author=}, {self.published_time=}, {text=}")

  def like(self) -> None:
    self.likes_count += 1

  def dislike(self) -> None:
    self.likes_count -= 1

  def add_comment(self, comment_text) -> None:
    self.comments.append(comment_text)

  def all_comments(self) -> None:
    print("Comments are: " + ";\n".join(self.comments))


post = Post("Artem", "Hi, its my first post")

post.like()
post.like()
post.dislike()
print("Likes counter:", post.likes_count)

post.add_comment("WOW")
post.add_comment("oh")
post.all_comments()
