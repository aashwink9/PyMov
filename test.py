def moviesearch(curs):
    title = "Emma"
    query = """
            SELECT movie.title, director.name, castmember.name, movie.length, movie.mpaa_rating, movie.avgrating
            FROM movie JOIN director ON (movie.id = director.movie_id)
            JOIN castmember ON (movie.id = castmember.movie_id)
            WHERE castmember.name LIKE %(title)s
            ORDER BY movie.title ASC, movie.releasedate ASC
            """

    curs.execute(query, ({'title': '%{}%'.format(title)}))
    mlist = curs.fetchall()

    for i in range(0, len(mlist)):
        m = mlist[i]

        title = m[0]
        dir = m[1]
        cas = m[2]
        leng = m[3]
        mpar = m[4]
        avgr = m[5]

        print("Title: ", title,
              "\nDirector: ", dir,
              "\nCast Members: ", cas,
              "\nLength: ", leng,
              "\nMPAA Rating: ", mpar,
              "\nAverage User Rating: ", avgr, "\n"
              )


def check_col(curs, usnm):
    getcols = "SELECT collectionid FROM public.usercollection WHERE username = %s"
    curs.execute(getcols, (usnm,))
    colst = curs.fetchall()

    if colst is None:
        return False
    else:
        return True


def addmovie(conn, curs, usnm):
    if check_col(curs, usnm):
        colname = input("Enter the collection you want to add a movie to: ")

        curs.execute("SELECT collectionid FROM public.usercollection WHERE colname = %s", (colname,))
        colexists = curs.fetchone()

        if colexists is not None:
            colid = colexists[0]
            getmov = input("Collection selected! Enter the name of a movie you want to add: ")
            curs.execute("SELECT movieid from public.movie WHERE title = %s", (getmov,))
            movexists = curs.fetchone()
            if movexists is not None:
                movid = movexists[0]
                curs.execute("INSERT INTO public.moviecollection (movieid, collectionid) VALUES(%s,%s)", (movid, colid))
                conn.commit()
                print("Movie ", getmov, " added to the collection!")
            else:
                print("Error, please select a valid movie!")
        else:
            print("Collection not found, please try again")

    else:
        print("It looks like you have not made any collections yet\n"
              "Please go back and make one.")
