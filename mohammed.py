example = [{"library_id" : 1, "nb_books": 3, "book_ids": [1, 5, 6, 4]},
        {"library_id": 3, "nb_books": 2, "book_ids": [1, 5]},
        {"library_id": 5, "nb_books": 7, "book_ids": [1, 5, 6, 4,6,6,7]},
        {"library_id": 2, "nb_books": 6, "book_ids": [1, 5, 6, 4,6,6]},
        {"library_id": 4, "nb_books": 3, "book_ids": [1, 5, 6]}]

def submit_solutions(d: [{}]):
    """
    :param d: [{"library_id" : 1, "nb_books": 3, "book_ids": [1, 5, 6, 4}]
    """
    with open("output.txt",'w') as f:
        f.write(str(len(d)))
        for item in d:
            f.write('\n')
            f.write(str(item["library_id"])+ " " + str(item["nb_books"]) )
            f.write('\n')
            f.write(' '.join([ str(i) for i in item["book_ids"]]))

    f.close()




submit_solutions(example)