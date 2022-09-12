import json
from json import JSONDecodeError
from pprint import pprint as pp
from bp_posts.dao.post import Post
from exceptions.data_exceptions import DataSourceError


class PostDAO:
    """Менеджер постов, загружает, ищет в тексте, вытаскивает по номеру и имени пользователя """
    def __init__(self, path):
        self.path = path

    def _load_data(self):
        """Загружает данные из JSON и возвращает список словарей  """

        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)

        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Не удается получить данные из файла {self.path}")

        return posts_data

    def _load_posts(self):
        """Возвращает список экземпляров Post"""

        posts_data = self._load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data]
        return list_of_posts

    def get_all(self):
        """
        получает все посты и возвращает список экземпляров класса Post
        """
        posts = self._load_posts()
        return posts

    def get_by_pk(self, pk):
        """
        получает пост по 'pk'
        """
        if type(pk) != int:
            raise TypeError("Должно быть число!")
        posts = self._load_posts()
        for post in posts:
            if post.pk == pk:
                return post

    def search_in_content(self, substring):
        """ищет посты, где в тексте встречается substring"""
        if type(substring) != str:
            raise TypeError("Должно быть слово!")
        substring = substring.lower()
        posts = self._load_posts()
        matching_post = [post for post in posts if substring in post.content.lower()]
        return matching_post

    def get_by_poster(self, user_name):
        """ищет посты с определенным автором"""
        if type(user_name) != str:
            raise TypeError("Должно быть имя!")
        user_name = user_name.lower()
        posts = self._load_posts()
        matching_post = [post for post in posts if post.poster_name.lower() == user_name]
        return matching_post

    # Пользователь



