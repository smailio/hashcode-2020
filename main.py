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
    book_index = tuple(i for i in range(len(book_ids)) if book_ids[i] not in scanned_book_ids)
    book_ids = tuple(book_ids[i] for i in book_index)
    book_values = tuple(book_values[i] for i in book_index)
    book_values_and_ids = tuple(zip(book_values, book_ids))
    """
    book_values_and_ids = ((0, 3), (2, 4))
    """
    book_values_and_ids = sorted(book_values_and_ids, reverse=True)
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
    scanned_book_ids = [2]
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
    :param library_selection : [{"library_id" : 1, "nb_books": 3, "book_ids": [1, 5, 6, 4}]
    :return:
    """
    value = 0
    day = 0
    nb_days = problem['nb_days']
    scanned_book_ids = []
    print("li", library_selection)
    for x in library_selection:
        library_id = x['library_id']
        library = problem['libraries'][library_id]
        signup_duration = library['signup_time']
        book_ids = library['l_books_ids']
        book_values = tuple(problem['books_score'][i] for i in book_ids)
        books_per_day = library['shipping_rate']
        signup_day = day
        day += signup_duration
        added, new_scanned_book_ids = get_score(
            signup_duration=signup_duration,
            book_ids=book_ids,
            book_values=book_values,
            books_per_day=books_per_day,
            signup_day=signup_day,
            end_day=nb_days - 1,
            scanned_book_ids=scanned_book_ids,
        )
        print("added", added)
        value += added
        scanned_book_ids.extend(new_scanned_book_ids)

    return value


def submit_solutions(solutions: [{}]):
    """

    :param d: [{"library_id" : 1, "nb_books": 3, "book_ids": [1, 5, 6, 4}]
    """
    pass


def brut_force_solve(problem, libraries_selection):
    # print("bfs",  libraries_selection)
    best_selection = []
    selected_ids = [l['library_id'] for l in libraries_selection]

    available = [
        library_id
        for library_id, library in enumerate(problem["libraries"])
        if library_id not in selected_ids
    ]
    if not available:
        return libraries_selection
    for library_id, library in enumerate(problem["libraries"]):
        if library_id in available:
            libraries_selection += [{
                "library_id": library_id,
                "nb_books": len(library["l_books_ids"]),
                "book_ids": library["l_books_ids"]
            }]
            best_selection_that_include_this_library = brut_force_solve(
                problem,
                libraries_selection
            )
            this_selection_score = get_selection_score(
                problem,
                best_selection_that_include_this_library
            )
            print("this_selection", this_selection_score, libraries_selection)
            best_selection_score = get_selection_score(problem, best_selection)
            if this_selection_score >= best_selection_score:
                best_selection = best_selection_that_include_this_library

    return best_selection


def main():
    print("hello world !")
    from pprint import pprint
    print("==problem====")
    problem = parse_input_file("input/a_example.txt")
    print(problem)
    print("============")
    solution = brut_force_solve(problem, [])
    print("*************")
    pprint(solution)


if __name__ == '__main__':
    main()
