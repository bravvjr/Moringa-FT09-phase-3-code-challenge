class Author:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise AttributeError("Name cannot be changed once assigned.")

    def __repr__(self):
        return f"<Author {self.name}>"
    # Method to fetch articles written by the author
    def articles(self, cursor):
        cursor.execute("""
            SELECT articles.id, articles.title, articles.content, articles.magazine_id, magazines.name, magazines.category
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            INNER JOIN magazines ON articles.magazine_id = magazines.id
            WHERE authors.id = ?
        """, (self.id,))
        articles_data = cursor.fetchall()
        return [Article(article["id"], article["title"], article["content"], self, Magazine(article["magazine_id"], article["name"], article["category"])) for article in articles_data]
    # Method to fetch magazines associated with the author
    def magazines(self, cursor):
        cursor.execute("""
            SELECT magazines.id, magazines.name, magazines.category
            FROM magazines
            INNER JOIN articles ON articles.magazine_id = magazines.id
            WHERE articles.author_id = ?
        """, (self.id,))
        magazines_data = cursor.fetchall()
        return [Magazine(magazine["id"], magazine["name"], magazine["category"]) for magazine in magazines_data]
