from django.contrib.auth.models import User
from django.test import TestCase
from catalog.models import Author, Book, BookInstance, Genre
import datetime


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_dead').verbose_name
        self.assertEquals(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 50)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name, author.first_name}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')


class BookInstanceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            password='1X<ISRUkw+tuK',
            email='testuser1@test.com'
        )

        self.author = Author.objects.create(
           first_name='Anton',
           last_name='Chekhov'
        )

        self.book = Book.objects.create(
            title='Hamlet',
            author=self.author,
            summary='Published in 1890',
            isbn='123456789123'
        )

        genre_objects_for_book = Genre.objects.all()
        self.book.genre.set(genre_objects_for_book)

    def test_book_is_not_overdue_if_due_back_date_is_today(self):
        due_date = datetime.date.today()
        book = BookInstance.objects.create(
           book=self.book,
           borrower=self.user,
           due_back=due_date,
           status='o'
        )
        self.assertFalse(book.is_overdue, "book should not be overdue")

    def test_book_is_not_overdue_if_due_back_date_is_later_than_today(self):
        due_date = datetime.date.today() + datetime.timedelta(days=5)
        book = BookInstance.objects.create(
           book=self.book,
           borrower=self.user,
           due_back=due_date,
           status='o'
        )
        self.assertFalse(book.is_overdue, "book should not be overdue")

    def test_book_is_not_overdue_if_due_back_date_is_none(self):
        due_date = None
        book = BookInstance.objects.create(
           book=self.book,
           borrower=self.user,
           due_back=due_date,
           status='o'
        )
        self.assertFalse(book.is_overdue, "book should not be overdue")

    def test_book_is_overdue_if_due_back_date_is_past(self):
        due_date = datetime.date.today() - datetime.timedelta(days=5)
        book = BookInstance.objects.create(
           book=self.book,
           borrower=self.user,
           due_back=due_date,
           status='o'
        )
        self.assertTrue(book.is_overdue, "book should be overdue")


# class BookModelTest(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         author = Author(first_name='Big', last_name='Bob')
#         language = Language(name="English")
#         author.save()
#         language.save()
#         Book.objects.create(title='fable', author=author, language=language)
#
#     def test_title_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('title').verbose_name
#         self.assertEquals(field_label, 'title')
#
#     def test_title_max_length(self):
#         book = Book.objects.get(id=1)
#         max_length = book._meta.get_field('title').max_length
#         self.assertEquals(max_length, 200)
#
#     def test_author_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('author').verbose_name
#         self.assertEquals(field_label, 'author')
#
#     def test_summary_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('summary').verbose_name
#         self.assertEquals(field_label, 'summary')
#
#     def test_summary_max_length(self):
#         book = Book.objects.get(id=1)
#         max_length = book._meta.get_field('summary').max_length
#         self.assertEquals(max_length, 1000)
#
#     def test_isbn_label(self):
#         book = Book.objects.get(id=1)
#         field_label = book._meta.get_field('isbn').verbose_name
#         self.assertEquals(field_label, 'ISBN')
#
#     def test_isbn_max_length(self):
#         book = Book.objects.get(id=1)
#         max_length = book._meta.get_field('isbn').max_length
#         self.assertEquals(max_length, 13)
#
#     def test_get_absolute_url(self):
#         book = Book.objects.get(id=1)
#         self.assertEquals(book.get_absolute_url(), '/catalog/book/1')
#
#     def test_method_getting_str(self):
#         book = Book.objects.get(id=1)
#         expected_object_name = book.title
#         self.assertEquals(expected_object_name, str(book))
