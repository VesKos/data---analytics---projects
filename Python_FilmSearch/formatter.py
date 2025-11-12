from tabulate import tabulate
import textwrap

def print_key_word_results(results):
    if results:
        table = []
        for i, row in enumerate(results, start=1):
            title = row[1]
            release_year = row[3]

            # Duration — ограничим длину отображения (обычно и не нужно)
            duration = str(row[4])

            # Актёры — добавим перенос строк каждые N символов
            actors_raw = row[7] or "Actors are not provided."
            wrapped_actors = '\n'.join(textwrap.wrap(actors_raw, width=40))  # перенос каждые 40 символов

            language = row[5]
            rating = row[6]

            table.append([i, title, release_year, duration, rating, language, wrapped_actors])

        headers = ["No.", "Title", "Year", "Duration, min", "Language", "Rating", "Actors"]
        print(tabulate(table, headers=headers, tablefmt="grid", stralign="left"))
    else:
        print("No results found for your query.")



def print_descriptions(results):
    print("\nFilm descriptions:")
    for i, row in enumerate(results, start=1):
        description = row[2] or "No description available."
        print(f"{i}. {description}")
        print("-" * 80)

