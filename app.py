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

    try:
        # Create an author
            cursor.execute('INSERT INTO authors (name) VALUES (?)', (author_name,))
            author_id = cursor.lastrowid

            author = Author(author_id, author_name)  # Create author object

            # Create a magazine
            cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (magazine_name, magazine_category))
            magazine_id = cursor.lastrowid

            magazine = Magazine(magazine_id, magazine_name, magazine_category)  # Create magazine object

           # Create an article
            cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)',
                        (article_title, article_content, author_id, magazine_id))

            conn.commit()

            authors_dict = {author.id: author for author in [Author(row[0], row[1]) for row in cursor.execute('SELECT * FROM authors')]}
            magazines_dict = {magazine.id: magazine for magazine in [Magazine(row[0], row[1], row[2]) for row in cursor.execute('SELECT * FROM magazines')]}

            print("Authors:")
            for author in authors_dict.values():
                print(author)

            print("\nMagazines:")
            for magazine in magazines_dict.values():
                print(magazine)

            print("\nArticles:")
            for article in cursor.execute('SELECT * FROM articles'):
                author_id = article[3]
                magazine_id = article[4]

                author_obj = authors_dict.get(author_id)
                magazine_obj = magazines_dict.get(magazine_id)

                if author_obj and magazine_obj:
                    print(Article(article[0], article[1], article[2], author_obj, magazine_obj))



    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback changes on error

    finally:
        conn.close()
    
if __name__ == "__main__":
    main()