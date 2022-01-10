import numpy as np
import random
from movie import update_avgrating
from datetime import datetime
import csv

path = "userrates.csv"


def populate_ratemovie(curs):
    curs.execute("SELECT username FROM public.users")
    usnms = curs.fetchall()
    userlist = []
    for u in usnms:
        userlist.append(u[0])

    print(userlist)


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


def ratemovie(conn, curs):
    with open(path, encoding="utf8") as f:
        reader = csv.reader(f, delimiter=',')
        line = 0
        for col in reader:

            if line == 0:
                line += 1
            else:
                last_access = datetime.now()
                usnm = col[0]
                movid = col[1]
                rating = col[2]

                curs.execute("SELECT movieid from public.movie WHERE movieid = %s", (movid,))

                exists = curs.fetchone()

                if exists is not None:
                    movid = exists[0]
                    curs.execute(
                        "INSERT INTO public.rating (username, userrating, movieid, ratingtime) VALUES(%s,%s,%s,%s)",
                        (usnm, rating,
                         movid, last_access))
                    conn.commit()
                    print("Successfully Rated!")
                    update_avgrating(conn, curs, movid)
