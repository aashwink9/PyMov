import movierec
import sortMovies
from datetime import datetime


def search_movie(curs, search_p):
    mlist = []
    if search_p == "title":
        inp = input("Enter the movie title: ")
        query = 'SELECT movie.title, director.directorname, castmember.name, movie.mlength, movie.mpaa_rating, ' \
                'movie.avgrating ' \
                'FROM movie JOIN director ON (movie.movieid = director.movieid) ' \
                'JOIN castmember ON (movie.movieid = castmember.movieid) ' \
                'WHERE movie.title LIKE %(inp)s'
        curs.execute(query, ({'inp': '%{}%'.format(inp)}))
        mlist = curs.fetchall()

    elif search_p == "rdate":
        inp = input("Enter the movie release date: ")
        query = 'SELECT movie.title, director.directorname, castmember.name, movie.mlength, movie.mpaa_rating, ' \
                'movie.avgrating ' \
                'FROM movie JOIN director ON (movie.movieid = director.movieid) ' \
                'JOIN castmember ON (movie.movieid = castmember.movieid) ' \
                'WHERE movie.releasedate LIKE %(inp)s' \
                'ORDER BY movie.title ASC, movie.releasedate ASC'
        curs.execute(query, ({'inp': '%{}%'.format(inp)}))
        mlist = curs.fetchall()

    elif search_p == "cmember":
        inp = input("Enter the movie cast member: ")
        query = 'SELECT movie.title, director.directorname, castmember.name, movie.mlength, movie.mpaa_rating, ' \
                'movie.avgrating ' \
                'FROM movie JOIN director ON (movie.movieid = director.movieid) ' \
                'JOIN castmember ON (movie.movieid = castmember.movieid) ' \
                'WHERE castmember.name LIKE %(inp)s' \
                'ORDER BY movie.title ASC, movie.releasedate ASC'
        curs.execute(query, ({'inp': '%{}%'.format(inp)}))
        mlist = curs.fetchall()

    elif search_p == "studio":
        inp = input("Enter the movie studio: ")
        query = 'SELECT movie.title, director.directorname, castmember.name, movie.mlength, movie.mpaa_rating, ' \
                'movie.avgrating ' \
                'FROM movie JOIN director ON (movie.movieid = director.movieid) ' \
                'JOIN castmember ON (movie.movieid = castmember.movieid) ' \
                'WHERE movie.studio LIKE %(inp)s' \
                'ORDER BY movie.title ASC, movie.releasedate ASC'
        curs.execute(query, ({'inp': '%{}%'.format(inp)}))
        mlist = curs.fetchall()

    else:
        print("Invalid command, please enter a valid option!")

    if mlist is None:
        print("It looks like we couldn't find any results, please try again!")
        return

    print("Searching the movie...Here are the results!\n")

    for i in range(0, len(mlist)):
        m = mlist[i]

        title = m[0]
        direc = m[1]
        cas = m[2]
        leng = m[3]
        mpar = m[4]
        avgr = m[5]

        print("Title: ", title,
              "\nDirector: ", direc,
              "\nCast Members: ", cas,
              "\nLength: ", leng,
              "\nMPAA Rating: ", mpar,
              "\nAverage User Rating: ", avgr, "\n"
              )


def search_movie_options(curs):
    print("Welcome to the Movie Search Options menu! You can search a movie by:\n"
          "1. Title (keyword: title)\n"
          "2. Case Member Rate a movie (keyword: cmember)\n"
          "3. Release Date Watch a movie (keyword: rdate)\n"
          "4. Studio (keyword: studio)\n"
          "5. Length of movie (keyword: length)\n"
          "6. Average Rating of a movie (keyword: rating)\n"
          "To go back enter q")

    backgreet = "\nWelcome to the Movie Search Options menu! You can search a movie by:\n" \
                "1. Title (keyword: title)\n" \
                "2. Case Member Rate a movie (keyword: cmember)\n" \
                "3. Release Date Watch a movie (keyword: rdate)\n" \
                "4. Studio (keyword: studio)\n" \
                "5. Length of movie (keyword: length)\n" \
                "6. Average Rating of a movie (keyword: rating)\n" \
                "To go back enter q"

    while True:
        inp = input("Enter your option: ")

        if inp == "title":
            search_movie(curs, "title")
            print(backgreet)
        elif inp == "cmember":
            search_movie(curs, "cmember")
            print(backgreet)
        elif inp == "rdate":
            search_movie(curs, "rdate")
            print(backgreet)
        elif inp == "studio":
            search_movie(curs, "rating")
            print(backgreet)
        elif inp == "length":
            search_movie(curs, "length")
            print(backgreet)
        elif inp == "rating":
            search_movie(curs, "rating")
            print(backgreet)
        elif inp == "q":
            print(backgreet)
            break
        else:
            print("Invalid command, please enter the one of the following commands:\n"
                  "1. Title (keyword: title)\n"
                  "2. Case Member Rate a movie (keyword: cmember)\n"
                  "3. Release Date Watch a movie (keyword: rdate)\n"
                  "4. Studio (keyword: studio)\n"
                  "5. Length of movie (keyword: length)\n"
                  "6. Average Rating of a movie (keyword: rating)\n"
                  "To go back enter q"
                  )


def update_avgrating(conn, curs, mid):
    curs.execute("SELECT userrating FROM public.rating WHERE movieid = %s", (mid,))
    ratinglst = curs.fetchall()
    countratings = len(ratinglst)

    avg = 0.0
    for i in range(0, countratings):
        currating = float(ratinglst[i][0])
        avg += currating

    avg = avg / countratings
    round(avg, 2)
    curs.execute("UPDATE public.movie SET avgrating = %s WHERE movieid = %s", (avg, mid))
    conn.commit()


def ratemovie(conn, curs, usnm):
    last_access = datetime.now()
    inptitle = input("Enter the movie name to rate: ")
    getmid = "SELECT movieid FROM public.movie WHERE title LIKE %(inptitle)s"
    curs.execute(getmid, ({'inptitle': '%{}%'.format(inptitle)}))
    exists = curs.fetchone()

    if exists is None:
        print("Please enter a valid movie title!")

    else:
        movid = exists[0]
        getmovtitle = "SELECT movie.title FROM public.movie WHERE movie.movieid = %s"
        curs.execute(getmovtitle, (movid,))
        movtitle = curs.fetchone()[0]

        # ---------Check if already rated-----------
        curs.execute("SELECT ratingid FROM public.rating WHERE username = %s AND movieid = %s", (usnm, movid))
        rated = curs.fetchone()
        # -------------------------------------------

        print("Your selected movie:", movtitle)
        rating = input("Enter the rating you'd like to give the movie: ")

        if float(rating) < 0.0 or float(rating) > 5.0:
            print("Please select a rating within the bounds of 0.0 and 5.0!")
            return

        if rated is None:
            curs.execute("INSERT INTO public.rating (username, userrating, movieid, ratingtime) VALUES(%s,%s,%s,%s)",
                         (usnm, rating,
                          movid, last_access))
            conn.commit()
            print("Successfully Rated!")
            update_avgrating(conn, curs, movid)

        else:
            rid = rated[0]
            again = input("You have already rated this movie!\n"
                          "Would you like to rate it again?(y/n): ")
            if again == "y":
                curs.execute("UPDATE public.rating SET userrating = %s, ratingtime = %s WHERE ratingid = %s", (rating,
                                                                                                               last_access,
                                                                                                               rid))
                conn.commit()
                print("New rating registered successfully!")
            elif again == "n":
                print("Okay! Going back...")


def watch_movie(conn, curs, usnm):
    mov = input("Select a movie title to watch: ")
    getmovid = "SELECT movieid FROM public.movie WHERE movie.title LIKE %(mov)s"
    curs.execute(getmovid, ({'mov': '%{}%'.format(mov)}))

    exists = curs.fetchone()

    if exists is None:
        print("Please enter a valid movie title!")

    else:
        movid = exists[0]
        getmovtitle = "SELECT movie.title FROM public.movie WHERE movie.movieid = %s"
        curs.execute(getmovtitle, (movid,))
        movtitle = curs.fetchone()[0]

        # ---------------------------Check if already watched--------------------------------
        curs.execute("SELECT watchid FROM public.watchmovie WHERE username = %s AND movieid = %s", (usnm, movid))
        watched = curs.fetchone()
        # -------------------------------------------------------------------------------------

        if watched is None:
            print("Watching the movie", movtitle, "...")
            populate_watchmov = "INSERT INTO public.watchmovie (username, movieid) VALUES(%s,%s)"
            curs.execute(populate_watchmov, (usnm, movid))
            print("Watched!")
            conn.commit()

        else:
            print("Movie already watched! Please select a different movie.")


def movie_options(conn, curs, usnm):
    print("Welcome to the movie options menu!\n"
          "Here are your options:\n"
          "(1) Search movie options\n"
          "(2) Rate a movie\n"
          "(3) Watch a movie\n"
          "(4) Sort Movies\n"
          "(5) Movie Trends\n"
          "(q) Go back")

    backgreeting = "\nWelcome back to the movie options menu!\n" \
                   "Here are your options:\n" \
                   "(1) Search movie options\n" \
                   "(2) Rate a movie\n" \
                   "(3) Watch a movie\n" \
                   "(4) Sort Movies\n" \
                   "(5) Movie Trends\n"\
                   "(q) Go back"
    while True:
        cmd = input("Enter your command: ")
        if cmd == "1":
            search_movie_options(curs)
            print(backgreeting)
        elif cmd == "2":
            ratemovie(conn, curs, usnm)
            print(backgreeting)
        elif cmd == "3":
            watch_movie(conn, curs, usnm)
            print(backgreeting)
        elif cmd == "4":
            sortMovies.callSortMovie(conn, curs)
            print(backgreeting)
        elif cmd == "5":
            movierec.trend_options(curs, usnm)
        elif cmd == "q":
            print("Welcome back to your movies simulation!\n "
                  "Here are your options:\n"
                  "(1) Collection Options\n"
                  "(2) Movie Options\n"
                  "(3) Users\n"
                  "(q) Logout\n")
            break
        else:
            print("Error, please enter a valid command")
