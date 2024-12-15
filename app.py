from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()

    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create an author
    cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
    author_id = cursor.lastrowid  # Use this to fetch the id of the newly created author

    # Create a magazine
    cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (magazine_name, magazine_category))
    magazine_id = cursor.lastrowid  # Use this to fetch the id of the newly created magazine

    # Create an article
    cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                   (article_title, article_content, author_id, magazine_id))

    conn.commit()

    # Query the database for inserted records
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()  # Fetch magazine data

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()  # Fetch author data

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()  # Fetch article data

    conn.close()

    # Display results
    print("\nMagazines:")
    for magazine in magazines:
        print(Magazine(magazine[0], magazine[1], magazine[2]))  # magazine[0], magazine[1], magazine[2] correspond to id, name, category

    print("\nAuthors:")
    for author in authors:
        print(Author(author[0], author[1]))  # author[0], author[1] correspond to id, name

    print("\nArticles:")
    for article in articles:
        # Find the corresponding Author and Magazine objects
        author_obj = next((author for author in authors if author[0] == article[3]), None)
        magazine_obj = next((magazine for magazine in magazines if magazine[0] == article[4]), None)
        
        if author_obj and magazine_obj:
            print(Article(article[0], article[1], article[2], author_obj, magazine_obj))

if __name__ == "__main__":
    main()
