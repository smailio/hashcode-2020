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
    from pprint import pprint
    pprint(parse_input_file("input/a_example.txt"))


if __name__ == '__main__':
    main()
