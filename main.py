def grouped(iterable, n):
    return zip(*[iter(iterable)]*n)


def line_to_ints(l):
    return tuple([int(s) for s in l.split(" ")])


def parse_input_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
        [nb_books, nb_libraries, nb_days] = line_to_ints(lines[0])
        books_score = line_to_ints(lines[1])

        def parse_libraries():
            for (l1, l2) in grouped(lines[2:], 2):
                (l_nb_books, signup_time, shipping_rate) = line_to_ints(l1)
                l_books_ids = line_to_ints(l2)
                yield {
                    "l_nb_books": l_nb_books,
                    "signup_time": signup_time,
                    "shipping_rate": shipping_rate,
                    "l_books_ids": l_books_ids
                }
        return {
            'nb_books': nb_books,
            'nb_libraries': nb_libraries,
            'nb_days': nb_days,
            'books_score': books_score,
            'libraries': list(parse_libraries())
        }


def get_score(
        signup_duration: int, book_ids: tuple, book_values: tuple, books_per_day: int, signup_day, end_day,
        scanned_book_ids: list,
):
    assert len(book_ids) == len(book_values)
    book_index = (i for i in range(len(book_ids)) if book_ids[i] not in scanned_book_ids)
    book_ids = tuple(book_ids[i] for i in book_index)
    book_values = tuple(book_values[i] for i in book_index)
    book_values_and_ids = tuple((book_ids[i], book_values[i]) for i in range(len(book_ids)))
    book_values_and_ids = sorted(book_values_and_ids)
    book_values = tuple(value for value, _ in book_values_and_ids)
    book_ids = tuple(i for _, i in book_values_and_ids)
    scan_days = end_day - signup_day + 1 - signup_duration
    value = 0
    i = 0
    sent_ids = []
    for day in range(scan_days):
        stop_i = min(i + books_per_day, len(book_values))
        value += sum(book_values[i:stop_i])
        sent_ids.extend([index for index in book_ids[i:stop_i]])
        i = stop_i
        if stop_i >= len(book_values):
            break
    return value, sent_ids


def test_get_score():
    signup_duration = 2
    book_ids = (0, 2, 3)
    book_values = (1, 2, 3)
    books_per_day = 2
    signup_day = 2
    end_day = 5
    scanned_book_ids = []
    value, sent_ids = get_score(
        signup_duration=signup_duration,
        book_ids=book_ids,
        book_values=book_values,
        books_per_day=books_per_day,
        signup_day=signup_day,
        end_day=end_day,
        scanned_book_ids=scanned_book_ids,
    )
    print(value)
    print(sent_ids)


def get_selection_score(problem, library_selection):
    """

    :param problem: {
            'nb_books': nb_books,
            'nb_libraries': nb_libraries,
            'nb_days': nb_days,
            'books_score': books_score,
            'libraries': list(parse_libraries()),
            '
        }
    :param library_selection : ["library_id_1", 'library_id_5"]
    :return:
    """
    return 0


def submit_solutions(d: [{}]):
    """

    :param d: [{"library_id" : 1, "nb_books": 3, "book_ids": [1, 5, 6, 4}]
    """
    pass


def brut_solve(problem, day, librairies_selection):
    def this_day_possibilities():
        for n_day, library in enumerate(problem["librairies"]):
            score_with_this_libray = brut_solve(problem, librairies_selection + [library])
            score_without_this_library = get_selection_score(problem, librairies_selection + [library])
            if score_with_this_libray > score_with_this_libray:
                return


def main():
    print("hello world !")
    data = parse_input_file("input/a_example.txt")
    from pprint import pprint
    # pprint(data)
    test_get_score()


if __name__ == '__main__':
    main()
