from bp_posts.dao.post import Post
from bp_posts.dao.post_dao import PostDAO
import pytest


def check_fields(post):
    fields = ["poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"]
    for field in fields:
        assert hasattr(post, field), f"Нет поля {field}"


class TestPostsDao:
    @pytest.fixture
    def post_dao(self):
        post_dao_instance = PostDAO("./bp_posts/tests/post_mock.json")
        return post_dao_instance

    # Функция получения всех

    def test_get_all_types(self, post_dao):
        posts = post_dao.get_all()
        assert type(posts) == list, "Incorrect type for result"
        post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"

    def test_get_all_fields(self, post_dao):
        posts = post_dao.get_all()
        post = post_dao.get_all()[0]
        check_fields(post)

    def test_get_all_correct_ids(self, post_dao):
        posts = post_dao.get_all()
        correct_pks = {1, 2, 3}
        pks = set([post.pk for post in posts])
        assert pks == correct_pks, "Не совпадают полученные id"

    # Функция получения одного по pk

    def test_get_by_pk_types(self, post_dao):
        post = post_dao.get_by_pk(1)
        assert type(post) == Post, "Incorrect type for result single item"

    def test_get_by_pk_fields(self, post_dao):
        post = post_dao.get_by_pk(1)
        check_fields(post)

    def test_get_by_pk_none(self, post_dao):
        post = post_dao.get_by_pk(911)
        assert post is None, "Should be None for not existing pk"

    @pytest.mark.parametrize("pk", [1, 2, 3])
    def test_get_by_pk_correct_id(self, post_dao, pk):
        post = post_dao.get_by_pk(pk)
        assert post.pk == pk, f"Incorrect post.pk for requested post with pk = {pk}"

    # Функция получения постов по вхождению строки

    def test_search_in_content_types(self, post_dao):
        posts = post_dao.search_in_content("Ага")
        assert type(posts) == list, "Incorrect type of result"
        post = post_dao.get_all()[0]
        assert type(post) == Post, "Incorrect type for result single item"

    def test_search_in_content_fields(self, post_dao):
        posts = post_dao.search_in_content("Ага")
        post = post_dao.get_all()[0]
        check_fields(post)

    def test_search_in_content_not_found(self, post_dao):
        posts = post_dao.search_in_content("777")
        assert posts == [], "Should be empty [] for substring which is not found"

    @pytest.mark.parametrize("s, pks", [
        ("Ага", {1}),
        ("Вышел", {2}),
        ("на", {1, 2, 3})
    ])
    def test_search_in_content_results(self, post_dao, s, pks):
        posts = post_dao.search_in_content(s)
        post_pks = set([post.pk for post in posts])
        assert post_pks == pks, f"Incorrect result was searching for {s}"
