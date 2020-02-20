def grouped(iterable, n):
    "s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ..."
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


def get_score(signup_duration, book_values, books_per_day, signup_day, end_day):
    return 0


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
    :param library_selection : [{"library_id" : 1, "nb_books": 3, "book_ids": [1, 5, 6, 4}]
    :return:
    """
    return 0


def submit_solutions(solutions: [{}]):
    """

    :param d: [{"library_id" : 1, "nb_books": 3, "book_ids": [1, 5, 6, 4}]
    """
    pass


def brut_force_solve(problem, libraries_selection):
    best_selection = []
    for library_id, library in enumerate(problem["librairies"]):
        if library_id not in libraries_selection:
            best_selection_that_include_this_library = brut_force_solve(
                problem,
                libraries_selection + [{"library_id": library_id, "nb_books": len(library["l_books_ids"]),
                                        "book_ids": library["l_books_ids"]}]
            )
            this_selection_score = get_selection_score(
                problem,
                best_selection_that_include_this_library
            )
            best_selection_score = get_selection_score(problem, best_selection)
            if this_selection_score > best_selection_score:
                best_selection = best_selection_that_include_this_library

    return best_selection


def main():
    print("hello world !")
    from pprint import pprint
    pprint(parse_input_file("input/a_example.txt"))


if __name__ == '__main__':
    main()
