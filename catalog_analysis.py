
import math

movies = [
    {"title": "The Dune Chronicles",
     "year": 2021,
     "genres": {"sci-fi", "drama"},
     "rating": 8.6,
     "duration_min": 155,
     "actors": ["T. Chalamet", "R. Ferguson", "O. Isaac"]},
    {"title": "Kitchen Stories", "year": 2019, "genres": {"comedy", "drama"},
     "rating": 7.1, "duration_min": 98, "actors": ["A. Novak", "M. Ferguson"]},
    {"title": "silent hours", "year": 2016, "genres": {"thriller", "drama"},
     "rating": 6.4, "duration_min": 112, "actors": ["J. Bloom", "K. Lee"]},
    {"title": "Comet Racers", "year": 2023, "genres": {"sci-fi", "action"},
     "rating": 5.9, "duration_min": 101, "actors": ["O. Isaac", "P. Diaz"]},
    {"title": "The Last Bakery", "year": 2014, "genres": {"comedy"},
     "rating": 7.8, "duration_min": 89, "actors": ["A. Novak", "T. Chalamet"]},
    {"title": "midnight in oslo", "year": 2020, "genres": {"thriller", "mystery"},
     "rating": 8.9, "duration_min": 124, "actors": ["K. Lee", "R. Ferguson"]},
    {"title": "Garden of Static", "year": 2022, "genres": {"drama"},
     "rating": 4.8, "duration_min": 137, "actors": ["P. Diaz", "J. Bloom"]},
    {"title": "The Quiet Algorithm", "year": 2024, "genres": {"sci-fi", "drama"},
     "rating": 9.2, "duration_min": 118, "actors": ["M. Ferguson", "O. Isaac"]},
    {"title": "Two Left Shoes", "year": 2011, "genres": {"comedy"},
     "rating": 6.0, "duration_min": 95, "actors": ["A. Novak", "K. Lee"]},
    {"title": "Red Harbor", "year": 2018, "genres": {"action", "thriller"},
     "rating": 7.3, "duration_min": 129, "actors": ["P. Diaz", "T. Chalamet"]},
]


def average_rating(movies: list[dict]) -> float:
    """Вернуть среднюю оценку по каталогу, округлённую до 1 знака."""
    total = sum(movie['rating'] for movie in movies)
    return round(total / len(movies), 1)


def catalog_age_stats(
    movies: list[dict], current_year: int = 2026
) -> tuple[int, int, int]:
    """Вернуть возраст самого старого, самого нового и средний возраст фильма."""
    ages = [current_year - movie['year'] for movie in movies]
    return max(ages), min(ages), math.ceil(sum(ages) / len(ages))


def duration_in_hours(minutes: int) -> str:
    """Перевести длительность в минутах в формат 'Xч Yм'."""
    return f'{minutes // 60}ч {minutes % 60}м'


def rating_tier(rating: float) -> str:
    """Вернуть категорию фильма по оценке."""
    if rating >= 9:
        return 'шедевр'
    elif rating >= 7:
        return 'хорошо'
    return 'средне' if rating >= 5 else 'слабо'


def decade_label(year: int) -> str:
    """Вернуть метку фильма по году выпуска."""
    match year:
        case _ if year > 2020:
            return 'новые'
        case _ if 2015 <= year <= 2020:
            return 'недавние'
        case _ if year < 2015:
            return 'старые'


def count_long_movies(movies: list[dict], threshold: int = 120) -> int:
    """Посчитать количество фильмов длинее threshold минут"""
    counter = 0
    for movie in movies:
        if movie['duration_min'] > threshold:
            counter += 1
    return counter


def normalize_title(title: str) -> str:
    """Привести название к формату Title Case."""
    words = [word[0].upper() + word[1:] for word in title.split()]
    return ' '.join(words)


def make_slug(title: str) -> str:
    """Превратить название в слаг."""
    return title.lower().replace(' ', '-')


def format_report_line(movie: dict) -> str:
    """Вернуть строку с описанием фильма."""
    title = normalize_title(movie['title'])
    year = movie['year']
    rating = movie['rating']
    duration = duration_in_hours(movie['duration_min'])
    genres = ', '.join(sorted(movie['genres']))
    return f'"{title}" ({year}) — {rating}/10, {duration}, жанры: {genres}'


def count_by_genre(movies: list[dict]) -> dict[str, int]:
    """Вернуть словарь с количеством фильмов по каждому жанру."""
    genre_counts = {}
    for movie in movies:
        for genre in movie['genres']:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1
    return genre_counts


def actor_filmography(movies: list[dict]) -> dict[str, list[str]]:
    """Вернуть словарь с фильмами каждого актёра."""
    filmography = {}
    for movie in movies:
        for actor in movie['actors']:
            filmography.setdefault(actor, []).append(movie['title'])
    return filmography


def all_genres(movies: list[dict]) -> set[str]:
    """Вернуть множество всех уникальных жанров."""
    genres = set()
    for movie in movies:
        genres |= movie['genres']
    return genres


def common_actors(movie1: dict, movie2: dict) -> set[str]:
    """Вернуть актёров, снимавшихся в обоих фильмах."""
    return set(movie1['actors']) & set(movie2['actors'])


def genres_only_in_one(movies_a: list[dict], movies_b: list[dict]) -> set[str]:
    """Вернуть жанры, которые есть в movies_a, но нет в movies_b."""
    return all_genres(movies_a) - all_genres(movies_b)


def iter_high_rated(movies: list[dict], min_rating: float = 8.0):
    """Лениво отдавать фильмы с рейтингом не ниже min_rating."""
    for movie in movies:
        if movie['rating'] >= min_rating:
            yield movie


def build_report(movies: list[dict]) -> None:
    """Вывести полный отчёт по каталогу."""
    _, _, avg_age = catalog_age_stats(movies)
    print('ОТЧЁТ ПО КАТАЛОГУ')
    print(f'Средний рейтинг: {average_rating(movies)}')
    print(f'Средний возраст фильмов: {avg_age} лет')
    print()
    print('Топ-3 фильма:')
    top3 = sorted(movies, key=lambda movie: movie['rating'], reverse=True)[:3]
    for movie in top3:
        print(f'  {format_report_line(movie)}')
    print()
    print('Фильмов по жанрам:')
    genre_counts = sorted(
        count_by_genre(movies).items(),
        key=lambda item: (-item[1], item[0]),
    )
    for genre, count in genre_counts:
        print(f'  {genre} — {count}')
    print()
    print(f'Все жанры каталога: {", ".join(sorted(all_genres(movies)))}')


def main() -> None:
    """Запустить анализ каталога."""
    # 3.1 Вывести не комедии
    for movie in movies:
        if 'comedy' in movie['genres']:
            continue
        print(movie['title'])

    # 3.2 Найти фильм с рейтингом выше 9.0
    i = 0
    while i < len(movies):
        if movies[i]['rating'] > 9.0:
            print(movies[i]['title'])
            break
        i += 1
    else:
        print('Шедевров не найдено')

    # 6.3 Словарь с фильмами выше среднего
    avg = average_rating(movies)
    top_movies = {
        movie['title']: movie['rating']
        for movie in movies
        if movie['rating'] > avg
    }
    print(top_movies)

    # 8.2 Продемонстрировать iter_high_rated
    for movie in iter_high_rated(movies):
        print(format_report_line(movie))

    # 8.3 Подсчет суммарной длительности фильмов с рейтингом 7+
    total_minutes = sum(
        movie['duration_min'] for movie in movies if movie['rating'] > 7
    )
    print(total_minutes)

    # 9 Вывести отчет по каталогу
    build_report(movies)


if __name__ == '__main__':
    main()