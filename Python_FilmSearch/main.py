import sys
import mysql_connector
import formatter
import log_writer
import log_stats

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def paginate_and_display(fetch_fn, count_fn, log_type, params):
    offset = 0
    total = count_fn(**params)
    if total == 0:
        print("No results found for your query.")
        return False

    print(f"Results found for your query {total} films.\n")

    while True:
        results = fetch_fn(**params, offset=offset)
        if not results:
            print("No more results.")
            return False

        log_writer.log_query(
            search_type=log_type,
            params={**params, "offset": offset}, 
            results_count=len(results)
        )

        formatter.print_key_word_results(results)

        while True:
            show_desc = input("Would you like to see the movie descriptions?(y/n): ").strip().lower()
            if show_desc == 'y':
                formatter.print_descriptions(results)
                break
            elif show_desc == 'n':
                break
            else:
                print("Please enter 'y' or 'n'.")

        while True:
            more = input("Would you like to see more movies(y/n): ").strip().lower()
            if more == 'y':
                offset += 10
                if offset >= total:
                    print("The list of films is fully displayed.")
                    return True
                break
            elif more == 'n':
                return False
            else:
                print("Please enter 'y' or 'n'.")


def print_descriptions(results):
    print("\nFilm descriptions:")
    for i, row in enumerate(results, start=1):
        description = row[2] 
        print(f"{i}. {description}")
        print("-" * 80)


def welcome_and_show_genres():
    text1 = Text(
        "Welcome to our search service! We are delighted to assist you in finding exactly what you’re looking for.\n"
        "Enjoy a seamless and efficient experience as you explore our extensive database.",
        style="bold white on cyan"
    )
    
    text2 = Text("We suggest you take a look at the genres and chronological order in the library:\n", style="bold bright_magenta")
    text3 = Text("Available genres list:\n", style="bold cyan")
    
    console.print(Panel(text1, title="[bold magenta]Welcome[/bold magenta]", border_style="bold cyan", expand=True))
    console.print(text2)
    console.print(text3)

    genres = mysql_connector.get_genre()
    if genres:
        for i, (genre,) in enumerate(genres, start=1):
            print(f"{i}. {genre}")
    else:
        print("Genres are unavailable.")

    min_year, max_year = mysql_connector.get_year_range()
    if min_year is not None and max_year is not None:
        film_range_text = Text(f"\nFilm release range: {min_year} – {max_year}\n", style="bold cyan")
        console.print(film_range_text)
    else:
        print("\nYear range is unavailable.\n")

    while True:
        ch = input("Continue search — by genre (g), by year (y) or to the main menu (m)? ").lower()
        if ch in ('g', 'y', 'm'):
            return ch
        print("Enter a correct value.")


def search_by_actor():
    name = input("Enter the actor’s first or last name: ").strip()
    if not name:
        print("Actor’s name cannot be blank.")
        return False

    total = mysql_connector.count_by_actor(name)
    if total == 0:
        print("No results found for your query.")
        return False

    return paginate_and_display(
        fetch_fn=mysql_connector.find_by_actor,
        count_fn=mysql_connector.count_by_actor,
        log_type="actor",
        params={"actor_name": name}
    )

def search_by_rating_and_year_range():

    ratings_map = {
        'G': 'G: General Audiences',
        'PG': 'PG: Parental Guidance Suggested',
        'PG-13': 'PG-13: Parents Strongly Cautioned',
        'R': 'R: Restricted',
        'NC-17': 'NC-17: No One 17 & Under Admitted'
    }

    print("\nAvailable ratings:")
    for i, desc in enumerate(ratings_map.values(), start=1):
        print(f"{i}. {desc}")

    rating_input = input("\nEnter a rating from the list: ").strip().upper()

    if rating_input not in ratings_map:
        print("Error: Invalid rating.")
        return False

    selected_rating = rating_input  # Код рейтинга, например 'PG'

    min_year, max_year = mysql_connector.get_year_range()
    if min_year is not None and max_year is not None:
        print(f"\nFilm release range: {min_year} – {max_year}")
    else:
        print("Year range is unavailable.")
        return False

    while True:
        start = input("Enter the starting year: ").strip()
        end = input("Enter the ending year: ").strip()
        if not (start.isdigit() and end.isdigit()):
            print("Error: numeric input required.")
            continue

        start_year = int(start)
        end_year = int(end)
        if start_year > end_year:
            print("Error: the starting value is greater than the ending value.")
            continue
        if start_year < min_year or end_year > max_year:
            print("Error: years are outside the valid range.")
            continue
        break

    total = mysql_connector.count_by_rating_and_year_range(selected_rating, start_year, end_year)
    if total == 0:
        print("No results found for your query.")
        return False

    return paginate_and_display(
        fetch_fn=mysql_connector.find_by_rating_and_year_range,
        count_fn=mysql_connector.count_by_rating_and_year_range,
        log_type="rating_year_range",
        params={"rating": selected_rating, "start_year": start_year, "end_year": end_year}
    )


def search_by_genre():
    print("\nAvailable genres list:\n")
    genres = mysql_connector.get_genre()
    if genres:
        for i, (genre,) in enumerate(genres, start=1):
            print(f"{i}. {genre}")
    else:
        print("Genres are unavailable.")
        return False

    genre_input = input("\nEnter the genre name: ").strip()
    if not genre_input:
        print("The genre cannot be blank.")
        return False

    total = mysql_connector.count_by_genre(genre_input)
    if total == 0:
        print("No results found for your query.")
        return False

    cont = paginate_and_display(
        fetch_fn=mysql_connector.find_by_genre,
        count_fn=mysql_connector.count_by_genre,
        log_type="genre",
        params={"genre": genre_input}
    )
    return cont


def search_by_year():
    min_year, max_year = mysql_connector.get_year_range()
    if min_year is None or max_year is None:
        print("Year range is unavailable.")
        return False

    print(f"\nAvailable year range: {min_year} – {max_year}")

    print("\nSelect search mode:")
    print("1 — Search by exact year")
    print("2 — Search by year range")

    mode = input("Your choice: ").strip()

    if mode == '1':
        year = input("Enter the year: ").strip()
        if not year.isdigit():
            print("Error: input must be a number.")
            return False

        year = int(year)
        if not (min_year <= year <= max_year):
            print("Year is out of the allowed range.")
            return False

        if mysql_connector.count_by_year(year) == 0:
            print("No results found for your query.")
            return False

        return paginate_and_display(
            fetch_fn=mysql_connector.find_by_year,
            count_fn=mysql_connector.count_by_year,
            log_type="year",
            params={"year": year}
        )

    elif mode == '2':
        start = input("Enter the start year: ").strip()
        end = input("Enter the end year: ").strip()

        if not (start.isdigit() and end.isdigit()):
            print("Error: input must be numeric.")
            return False

        start_year, end_year = int(start), int(end)

        if start_year > end_year:
            print("The start year cannot be greater than the end year.")
            return False

        if start_year < min_year or end_year > max_year:
            print("Years are out of the allowed range.")
            return False

        if mysql_connector.count_by_year_range(start_year, end_year) == 0:
            print("No results found for your query.")
            return False

        return paginate_and_display(
            fetch_fn=mysql_connector.find_by_year_range,
            count_fn=mysql_connector.count_by_year_range,
            log_type="year_range",
            params={"start_year": start_year, "end_year": end_year}
        )

    else:
        print("Error: please enter 1 or 2.")
        return False

def search_by_keyword():
    while True:
        key = input("Enter a keyword: ").strip()
        if not key:
            print("The keyword cannot be blank.")
            return False

        total = mysql_connector.count_by_key_word(key)
        if total == 0:
            print("No results found for your query.")
            return False

        cont = paginate_and_display(
            fetch_fn=mysql_connector.find_by_key_word,
            count_fn=mysql_connector.count_by_key_word,
            log_type="key_word",
            params={"keyword": key}
        )
        return cont

def search_by_genre_and_year_range():
    genres = mysql_connector.get_genre()
    if not genres:
        print("Genres are unavailable.")
        return False

    print("\nAvailable genres:")
    for i, (genre,) in enumerate(genres, start=1):
        print(f"{i}. {genre}")

    genre_input = input("\nEnter the genre: ").strip()
    if not genre_input:
        print("The genre cannot be blank.")
        return False

    min_year, max_year = mysql_connector.get_year_range()
    if min_year is None or max_year is None:
        print("Year range is unavailable.")
        return False

    print(f"Available year range: {min_year} – {max_year}")

    while True:
        start = input("Enter the start year: ").strip()
        end = input("Enter the end year: ").strip()
        if not (start.isdigit() and end.isdigit()):
            print("Error: please enter numbers.")
            continue
        start_year, end_year = int(start), int(end)
        if start_year > end_year:
            print("The start year cannot be greater than the end year.")
            continue
        if start_year < min_year or end_year > max_year:
            print("Years are out of the allowed range.")
            continue
        break

    
    total = mysql_connector.count_by_genre_and_year_range(genre_input, start_year, end_year)
    if total == 0:
        print("No results found for your query.")
        return False

    print(f"Results found for your query {total} films.\n")

    return paginate_and_display(
        fetch_fn=mysql_connector.find_by_genre_and_year_range,
        count_fn=mysql_connector.count_by_genre_and_year_range,
        log_type="genre_year_range",
        params={"genre": genre_input, "start_year": start_year, "end_year": end_year}
    )

def show_actor_stats():
    data = log_stats.get_actor_stats()
    formatter.print_actor_stats_table(data)

def show_rating_stats():
    data = log_stats.get_rating_stats()
    formatter.print_rating_stats_table(data)


def main_menu():
    while True:
        print("\nSelect an action:")
        print("1 — Search by title")
        print("2 — Search by year")
        print("3 — Search by genre")
        print("4 — Search by genre and year range")
        print("5 — Search by actor")
        print("6 — Search by rating and year range")
        print("7 — Show statistics")
        print("8 — Exit")
        choice = input("Your choice: ").strip()

        match choice:
            case '1':
                if not search_by_keyword():
                    continue
            case '2':
                if not search_by_year():
                    continue
            case '3':
                if not search_by_genre():
                    continue
            case '4':
                if not search_by_genre_and_year_range():
                    continue
            case '5':
                if not search_by_actor():
                    continue           
            case '6':
                if not search_by_rating_and_year_range():
                    continue        
            case '7':
                while True:
                    print("\n Log statistics — please select an option: ")
                    print("1 — Detailed logs (all queries)")
                    print("2 — Overview of request types")
                    print("3 — Most frequent queries")
                    print("4 — Statistics by actors")
                    print("5 — Statistics by ratings")
                    print("6 — Return to the main menu")
            
                    log_choice = input("Your choice: ").strip()
            
                    match log_choice:
                        case '1':
                            log_stats.get_raw_logs()
                        case '2':
                            log_stats.get_grouped_logs()
                        case '3':
                            log_stats.get_most_frequent_logs()
                        case '4':
                            log_stats.get_actor_stats()
                        case '5':
                             log_stats.get_rating_stats()
                        case '6':
                            print("Return to the main menu")
                            break
                        case _:
                            print("Error: enter a number between 1 and 6.")

            case '8':
                farewell_text = Text("You have completed the search.\nThank you for using our service, and we wish you all the best!",
                style="bold white on cyan")
                console.print(Panel(farewell_text, title="[bold magenta]Goodbye[/bold magenta]", border_style="bold cyan", expand=True))
                sys.exit(0)
            case _:
                print("Error: enter a number between 1 and 8.")


if __name__ == "__main__":
    while True:
        action = welcome_and_show_genres()
        if action == 'g':
            search_by_genre()
            main_menu()
        elif action == 'y':
            search_by_year()
            main_menu()
        elif action == 'm':
            main_menu()
        else:
            continue