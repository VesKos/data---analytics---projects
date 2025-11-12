import pymysql
from pymysql import OperationalError, MySQLError
from local_settings import dbconfig


def _safe_execute(query, params=()):
    connection = None
    try:
        connection = pymysql.connect(**dbconfig)
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except OperationalError as e:
        print(f"Database connection error: {e}")
    except MySQLError as e:
        print(f"[MySQL] Failed to execute query: {e}")
    except Exception as e:
        print(f"[MySQL] Unexpected error: {e}")
    finally:
        if connection:
           connection.close()
    return None


def _safe_count(query, params=()):
    result = _safe_execute(query, params)
    return result[0][0] if result else 0


def find_by_key_word(keyword, offset):
    return _safe_execute(
        """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.length,
            f.rating,
            l.name AS language,
            GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
        FROM film AS f
        JOIN language AS l ON f.language_id = l.language_id
        LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
        LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE f.title LIKE %s
        GROUP BY f.film_id
        ORDER BY f.title
        LIMIT 10 OFFSET %s;
        """,
        ('%' + keyword + '%', offset)
    )


def count_by_key_word(keyword):
    return _safe_count(
        "SELECT COUNT(*) FROM film WHERE title LIKE %s",
        ('%' + keyword + '%',)
    )


def get_genre():
    return _safe_execute("SELECT DISTINCT name FROM category ORDER BY name") or []


def find_by_genre(genre, offset):
    return _safe_execute(
        """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.length,
            f.rating,
            l.name AS language,
            GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
        FROM film AS f
        JOIN language AS l ON f.language_id = l.language_id
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS c ON fc.category_id = c.category_id
        LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
        LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE c.name LIKE %s
        GROUP BY f.film_id
        ORDER BY f.title
        LIMIT 10 OFFSET %s;
        """,
        ('%' + genre + '%', offset)
    )


def count_by_genre(genre):
    return _safe_count(
        """
        SELECT COUNT(*)
        FROM film AS f
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS c ON fc.category_id = c.category_id
        WHERE c.name LIKE %s
        """,
        ('%' + genre + '%',)
    )


def find_by_year(year, offset):
    return _safe_execute(
        """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.length,
            f.rating,
            l.name AS language,
            GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
        FROM film AS f
        JOIN language AS l ON f.language_id = l.language_id
        LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
        LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE f.release_year = %s
        GROUP BY f.film_id
        ORDER BY f.title
        LIMIT 10 OFFSET %s;
        """,
        (year, offset)
    )


def count_by_year(year):
    return _safe_count(
        "SELECT COUNT(*) FROM film WHERE release_year = %s",
        (year,)
    )


def find_by_year_range(start_year, end_year, offset):
    return _safe_execute(
        """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.length,
            f.rating,
            l.name AS language,
            GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
        FROM film AS f
        JOIN language AS l ON f.language_id = l.language_id
        LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
        LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE f.release_year BETWEEN %s AND %s
        GROUP BY f.film_id
        ORDER BY f.release_year, f.title
        LIMIT 10 OFFSET %s;
        """,
        (start_year, end_year, offset)
    )


def count_by_year_range(start_year, end_year):
    return _safe_count(
        "SELECT COUNT(*) FROM film WHERE release_year BETWEEN %s AND %s",
        (start_year, end_year)
    )


def get_year_range():
    result = _safe_execute("SELECT MIN(release_year), MAX(release_year) FROM film")
    if result:
        return result[0][0], result[0][1]
    return None, None

def find_by_genre_and_year_range(genre, start_year, end_year, offset):
    return _safe_execute(
        """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.length,
            f.rating,
            l.name AS language,
            GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
        FROM film AS f
        JOIN language AS l ON f.language_id = l.language_id
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS c ON fc.category_id = c.category_id
        LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
        LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE c.name LIKE %s AND f.release_year BETWEEN %s AND %s
        GROUP BY f.film_id
        ORDER BY f.title
        LIMIT 10 OFFSET %s;
        """,
        ('%' + genre + '%', start_year, end_year, offset)
    )


def count_by_genre_and_year_range(genre, start_year, end_year):
    return _safe_count(
        """
        SELECT COUNT(*)
        FROM film AS f
        JOIN film_category AS fc ON f.film_id = fc.film_id
        JOIN category AS c ON fc.category_id = c.category_id
        WHERE c.name LIKE %s AND f.release_year BETWEEN %s AND %s
        """,
        ('%' + genre + '%', start_year, end_year)
    )

def find_by_actor(actor_name, offset=0, limit=10):
    return _safe_execute(
        """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.length,
            f.rating,
            l.name AS language,
            GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
        FROM film AS f
        JOIN language AS l ON f.language_id = l.language_id
        JOIN film_actor AS fa ON f.film_id = fa.film_id
        JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE LOWER(CONCAT(a.first_name, ' ', a.last_name)) LIKE %s
           OR LOWER(a.first_name) LIKE %s
           OR LOWER(a.last_name) LIKE %s
        GROUP BY f.film_id
        ORDER BY f.release_year DESC
        LIMIT %s OFFSET %s
        """,
        (f'%{actor_name.lower()}%', f'%{actor_name.lower()}%', f'%{actor_name.lower()}%', limit, offset)
    )


def count_by_actor(actor_name):
    query = """
        SELECT COUNT(*)
        FROM film
        JOIN film_actor ON film.film_id = film_actor.film_id
        JOIN actor ON film_actor.actor_id = actor.actor_id
        WHERE LOWER(CONCAT(actor.first_name, ' ', actor.last_name)) LIKE %s
           OR LOWER(actor.first_name) LIKE %s
           OR LOWER(actor.last_name) LIKE %s
    """
    keyword = f"%{actor_name.lower()}%"
    return _safe_count(query, (keyword, keyword, keyword))


def find_by_rating_and_year_range(rating, start_year, end_year, offset):
    return _safe_execute(
        """
        SELECT 
            f.film_id,
            f.title,
            f.description,
            f.release_year,
            f.length,
            f.rating,
            l.name AS language,
            GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
        FROM film AS f
        JOIN language AS l ON f.language_id = l.language_id
        LEFT JOIN film_actor AS fa ON f.film_id = fa.film_id
        LEFT JOIN actor AS a ON fa.actor_id = a.actor_id
        WHERE f.rating = %s AND f.release_year BETWEEN %s AND %s
        GROUP BY f.film_id
        ORDER BY f.title
        LIMIT 10 OFFSET %s;
        """,
        (rating, start_year, end_year, offset)
    )


def count_by_rating_and_year_range(rating, start_year, end_year):
    return _safe_count(
        """
        SELECT COUNT(*)
        FROM film
        WHERE rating = %s AND release_year BETWEEN %s AND %s
        """,
        (rating, start_year, end_year)
    )