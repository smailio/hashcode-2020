import random
import math
import toolz


def grouped(iterable, n):
    return zip(*[iter(iterable)] * n)


def line_to_ints(l):
    return tuple([int(s) for s in l.split(" ")])


def parse_input_file(path):
    with open(path, "r") as f:
        lines = f.readlines()
        [nb_books, nb_libraries, nb_days] = line_to_ints(lines[0])
        books_score = line_to_ints(lines[1])

        def parse_libraries():
            for (i, (l1, l2)) in enumerate(grouped(lines[2:], 2)):
                (l_nb_books, signup_time, shipping_rate) = line_to_ints(l1)
                l_books_ids = line_to_ints(l2)
                yield {
                    "library_id": i,
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
        signup_duration: int, book_ids: tuple, book_values: tuple,
        books_per_day: int, signup_day, end_day,
        scanned_book_ids: list,
):
    assert len(book_ids) == len(book_values)
    book_index = tuple(
        i for i in range(len(book_ids)) if book_ids[i] not in scanned_book_ids)
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
    sending_record = []
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
        value += added
        scanned_book_ids.extend(new_scanned_book_ids)
        sending_record.append([
            library_id,
            len(new_scanned_book_ids),
            new_scanned_book_ids,
        ])
    return value, sending_record


def submit_solutions(solutions: [{}]):
    """

    :param d: [{"library_id" : 1, "nb_books": 3, "book_ids": [1, 5, 6, 4}]
    """
    pass


def brut_force_solve(problem, libraries_selection):
    best_selection = []
    selected_ids = [l['library_id'] for l in libraries_selection]
    # print("selected_ids ", selected_ids)
    all_availabe = [
        library_id
        for library_id, library in enumerate(problem["libraries"])
        if library_id not in selected_ids
    ]
    available = random.sample(all_availabe, min(2, len(all_availabe)))
    # print("available ", available)
    if len(available) == 0:
        return libraries_selection
    for library_id, library in enumerate(problem["libraries"]):

        if library_id in available:
            # print("available2", available)
            yololo = libraries_selection + [{
                "library_id": library_id,
                "nb_books": len(library["l_books_ids"]),
                "book_ids": library["l_books_ids"]
            }]
            best_selection_that_include_this_library = brut_force_solve(
                problem,
                yololo
            )
            this_selection_score, sending_record = get_selection_score(
                problem,
                best_selection_that_include_this_library
            )
            # print("this_selection", this_selection_score, yololo)
            best_selection_score, _ = get_selection_score(problem,
                                                          best_selection)
            if this_selection_score >= best_selection_score:
                best_selection_that_include_this_library = [
                    {**s, 'nb_books': sending_record[i][1],
                     "book_ids": sending_record[i][2]}
                    for (i, s) in
                    enumerate(best_selection_that_include_this_library)
                ]
                best_selection = best_selection_that_include_this_library

    return best_selection


def add_stats(problem):
    problem["libraries"] = [
        {
            **library,
            "biggest_books": sorted(
                library["l_books_ids"],
                key=lambda book_id: problem["books_score"][book_id],
                reverse=True
            )
        }
        for library in problem["libraries"]
    ]
    problem["libraries"] = [
        {
            **library,
            "s_books_ids": set(library["l_books_ids"])
        }
        for library in problem["libraries"]
    ]
    problem["book_specialness"] = {
        book_id: sum([
            1
            for other_library in problem["libraries"]
            if book_id in other_library["s_books_ids"]
        ])
        for book_id in set(toolz.concatv(
            [library["l_books_ids"] for library in problem["libraries"]])
        )
    }
    problem["libraries"] = [
        {
            **library,
            "specialness": - sum(
                sum(problem["book_specialness"][l_book_id])
                for l_book_id in library["l_books_ids"]
            )
        }
        for library in problem["libraries"]
    ]


def solve_sort(problem):
    add_stats(problem)
    solutions = {
        "libraries": [],
        "selected_books": [],
        "remaining_days": problem["nb_days"]
    }
    i = 0
    while remaining_days(problem,
                         solutions["libraries"]) > 0 and available_libraries(
        problem, solutions):
        s = best_next_library(problem, solutions)
        solutions["libraries"] += [s]
        solutions["selected_books"] = selected_books(solutions["libraries"])
        solutions["remaining_days"] = remaining_days(problem,
                                                     solutions["libraries"])
        i += 1
        print("i", i)
        # solutions[i] = s
        # problem['libraries'] = [
        #     l
        #     for (i, l) in enumerate(problem['libraries'])
        #     if i != s["library_id"]
        # ]
    return solutions


def remaining_days(problem, selection):
    libraries = problem['libraries']
    nb_days = problem["nb_days"]
    return nb_days - sum([
        libraries[library_id]["signup_time"]
        for library_id in [s["library_id"] for s in selection]
    ])


def available_libraries(problem, solution):
    selected_libraries = {l["library_id"] for l in solution["libraries"]}

    return [
        library for library in problem["libraries"]
        if library['library_id'] not in selected_libraries
    ]


def selected_books(solution):
    return {
        book_id
        for l in solution
        for book_id in l["book_ids"]
    }


def best_next_library(problem, solution: []):
    """

    :param problem:
    :param solution: [{"library_id" : 1, "nb_books": 3, "book_ids": [1, 5, 6, 4}]
    :return:
    """

    def best_book_selection(library, solution, fill_with_shit=False):
        signup_time = library["signup_time"]
        shipping_rate = library["shipping_rate"]
        l_unselected_books_ids = [
            book_id
            for book_id in library['biggest_books']
            if book_id not in solution["selected_books"]
        ]
        volume = min(1,
                     shipping_rate * (solution["remaining_days"] - signup_time))
        books_selection = l_unselected_books_ids[:volume]
        if fill_with_shit:
            return books_selection + l_unselected_books_ids[volume:]
        else:
            return books_selection

    def turnover(library):
        books_score = problem["books_score"]
        books_selection = best_book_selection(library, solution)
        return sum(books_score[book_id] for book_id in books_selection)

    # def speciallness(library, solution):
    #     return len([library])

    def sort_key(library):
        corrected_signup_time = - round(math.log(library["signup_time"], 3), 2)
        return corrected_signup_time, library["specialness"], turnover(library)

    next_library = max(available_libraries(problem, solution), key=sort_key)
    next_library_books_id = best_book_selection(next_library, solution)
    return {
        "library_id": next_library["library_id"],
        "book_ids": next_library_books_id,
        "nb_books": len(next_library_books_id)
    }


# def keep_best_half(problem):
#     return {
#         **problem,
#         "libraries": sorted(problem["libraries"], key=lambda l: sum([
#             problem['books_score'][book_id] for book_id in l["l_books_ids"]
#         ]))[:10],
#
#     }


def google_score(problem, solution):
    books_score = problem["books_score"]
    nb_days = problem["nb_days"]
    libraries = problem['libraries']
    score = 0
    selected_book_ids = set()
    for l in solution["libraries"]:
        l_id = l['library_id']
        l_sign_up_time = libraries[l_id]['signup_time']
        nb_days -= l_sign_up_time
        for book_id in l["book_ids"]:
            if book_id not in selected_book_ids:
                selected_book_ids.add(book_id)
                score += books_score[book_id]
    return score


def submit_solutions(problem_file_name, d: [{}]):
    """
    :param d: [{"library_id" : 1, "nb_books": 3, "book_ids": [1, 5, 6, 4}]
    """
    with open(f"{problem_file_name}_solution.txt", 'w') as f:
        f.write(str(len(d['libraries'])))
        for item in d["libraries"]:
            f.write('\n')
            f.write(str(item["library_id"]) + " " + str(item["nb_books"]))
            f.write('\n')
            f.write(' '.join([str(i) for i in item["book_ids"]]))

    f.close()


def main():
    print("hello world !")
    from pprint import pprint
    print("==problem====")
    problem_filename = "input/a_example.txt"
    problem = parse_input_file(problem_filename)
    pprint(problem)
    print("============")
    solution = solve_sort(problem)
    print("*************")
    pprint(solution)
    print('Oo' * 20)
    print(google_score(problem, solution))
    # submit_solutions(problem_filename, solution)


def main3():
    paths = [
        "input/a_example.txt",
        "input/b_read_on.txt",
        "input/c_incunabula.txt",
        "input/d_tough_choices.txt",
        "input/e_so_many_books.txt",
        "input/f_libraries_of_the_world.txt",
    ]
    for p in paths:
        problem = parse_input_file(p)
        solution = solve_sort(problem)
        print(google_score(problem, solution))
        submit_solutions(p, solution)


if __name__ == '__main__':
    main3()
