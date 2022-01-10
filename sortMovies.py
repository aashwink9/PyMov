import psycopg2

nameAsc = """
            SELECT * FROM Movie
            ORDER BY title ASC
            """

nameDesc = """
            SELECT * FROM Movie
            ORDER BY title DESC
            """

studioAsc = """
            SELECT * FROM Movie
            ORDER BY studio ASC
            """

studioDesc = """
            SELECT * FROM Movie
            ORDER BY studio DESC
            """

genreAsc = """
            SELECT * FROM Movie
            ORDER BY genretitle ASC
            """

genreDesc = """
            SELECT * FROM Movie
            ORDER BY genretitle DESC
            """

releasedYearAsc = """
            SELECT * FROM Movie
            ORDER BY releasedate ASC
            """

releasedYearDesc = """
            SELECT * FROM Movie
            ORDER BY releasedate DESC
            """


def sortMovie(curs, sql):
    try:
        if sql == "nameAsc":
            curs.execute(nameAsc)
        elif sql == "nameDesc":
            curs.execute(nameDesc)
        elif sql == "studioAsc":
            curs.execute(studioAsc)
        elif sql == "studioDesc":
            curs.execute(studioDesc)
        elif sql == "genreAsc":
            curs.execute(genreAsc)
        elif sql == "genreDesc":
            curs.execute(genreDesc)
        elif sql == "releasedYearAsc":
            curs.execute(releasedYearAsc)
        elif sql == "releasedYearDesc":
            curs.execute(releasedYearDesc)

        movieList = curs.fetchall()
        for row in movieList:
            print('title: ', row[1])
            print('length: ', row[2])
            print('MPAA rating: ', row[3])
            print('average rating: ', row[4])
            print('release year: ', row[5])
            print('genre title: ', row[6])
            print('studio: ', row[7], '\n')

    except psycopg2.Error as e:
        print(e, "Error, please select a valid sorting option!")


# call sort movie
def callSortMovie(conn, curs):
    print("Welcome to the sort movie options! You can sort movies by:\n"
          "nameAsc, nameDesc, studioAsc, studioDesc, genreAsc, genreDesc, releasedYearAsc, releasedYearDesc")
    command = input("Select one of the above to sort the movies: ")
    sortMovie(curs, command)
