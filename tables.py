import csv

path = 'moviess.csv'


def importMovie(conn, cursor):
    with open(path, encoding="utf8") as f:
        reader = csv.reader(f, delimiter=',')
        line = 0
        for column in reader:
            if line == 0:
                line += 1
            else:
                movie_id = column[0]
                title = column[2]
                length = column[9]
                MPAA_rating = column[8]
                releaseDate = column[7]
                genre = column[10]
                studio = column[11]

                cursor.execute("INSERT INTO public.movie VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                               (movie_id, title, length, MPAA_rating, 0.0,
                                releaseDate, genre, studio))
                conn.commit()
                line += 1


def importDirector(conn, cursor):
    with open(path, encoding="utf8") as f:
        reader = csv.reader(f, delimiter=',')
        line = 0
        for column in reader:
            if line == 0:
                line += 1
            else:
                movie_id = column[0]
                director = column[3]

                cursor.execute("INSERT INTO public.director VALUES (%s,%s)", (movie_id, director))
                conn.commit()
                line += 1


def importCastMember(conn, cursor):
    with open(path, encoding="utf8") as f:
        reader = csv.reader(f, delimiter=',')
        line = 0
        for column in reader:
            if line == 0:
                line += 1
            else:
                movie_id = column[0]
                cast = column[4]
                cursor.execute("INSERT INTO CastMember VALUES (%s,%s)", (movie_id, cast))
                conn.commit()
                line += 1
