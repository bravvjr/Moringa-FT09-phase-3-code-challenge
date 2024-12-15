class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self._name = name
        self._category = category

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be between 2 and 16 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string.")

    def __repr__(self):
        return f"<Magazine {self.name}>"

    # Method to fetch articles associated with the magazine
    def contributors(self, cursor):
        cursor.execute("""
            SELECT authors.id, authors.name
            FROM authors
            INNER JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        authors_data = cursor.fetchall()
        return [Author(author["id"], author["name"]) for author in authors_data]  # Ensures name is passed

    def articles(self, cursor):
        cursor.execute("""
            SELECT articles.id, articles.title, articles.content, articles.author_id
            FROM articles
            INNER JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        """, (self.id,))
        articles_data = cursor.fetchall()
        return [Article(article["id"], article["title"], article["content"], Author(article["author_id"], article["author_name"]), self) for article in articles_data]

    # Method to fetch titles of all articles written for the magazine
    def article_titles(self, cursor):
        cursor.execute("""
            SELECT title FROM articles
            WHERE magazine_id = ?
        """, (self.id,))
        titles = cursor.fetchall()
        return [title["title"] for title in titles] if titles else None

    # Method to fetch authors who have written more than 2 articles for the magazine
    def contributing_authors(self, cursor):
        cursor.execute('''
            SELECT authors.id, authors.name, COUNT(*) as count 
            FROM authors
            INNER JOIN articles ON articles.author_id = authors.id
            WHERE magazine_id = ?
            GROUP BY authors.id, authors.name
            HAVING count > 2
        ''', (self.id,))
        authors_data = cursor.fetchall()
        return [Author(author["id"], author["name"]) for author in authors_data] if authors_data else None