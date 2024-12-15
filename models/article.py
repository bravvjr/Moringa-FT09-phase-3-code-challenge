class Article:
    def __init__(self, id, title, content, author, magazine):
        self._id = id
        self._title = title
        self._content = content
        self._author = author
        self._magazine = magazine

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if 5 <= len(value) <= 50:
            self._title = value
        else:
            raise ValueError("Title must be between 5 and 50 characters.")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    def __repr__(self):
        return f"<Article {self.title} by {self.author.name}>"

    def get_author(self, cursor):
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self._author.id,))
        author_data = cursor.fetchone()
        return Author(author_data["id"], author_data["name"])

    def get_magazine(self, cursor):
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self._magazine.id,))
        magazine_data = cursor.fetchone()
        return Magazine(magazine_data["id"], magazine_data["name"], magazine_data["category"])
