from datetime import datetime


def most_popular_movie_90days(cur):
    print("Here are the most popular movies in the last 90 days:")
    cur.execute("SELECT movieid FROM public.rating WHERE ratingtime >= '2021-09-01 00:00:00' "
                "AND ratingtime <= '2021-12-01 00:00:00' GROUP BY movieid "
                "ORDER BY MAX(userrating) DESC LIMIT 20")

    movies = cur.fetchall()

    if movies is not None:
        for movie in movies:
            cur.execute("SELECT title FROM public.movie WHERE movieid = %s", (movie,))
            m = cur.fetchall()
            if len(m) is not 0:
                print(m[0][0])


def popular_movie_among_friends(cur, username):
    print("Here are the most popular movies among your friends:")
    cur.execute("SELECT username FROM public.userfollow WHERE follower = %s", (username,))
    friend = cur.fetchall()
    for i in friend:
        cur.execute("SELECT movieid FROM public.rating WHERE username = %s"
                    "GROUP BY userrating, movieid ORDER BY MAX(userrating) DESC LIMIT 20", i)
        movielst = cur.fetchall()

        if movielst is not None:
            for movie in movielst:
                cur.execute("SELECT title FROM public.movie WHERE movieid = %s", (movie,))
                mo = cur.fetchone()
                if mo is not None:
                    for m in mo:
                        print(m)


def new_release(cur):
    print("Here are the new movie releases:")
    now = datetime.now()
    date = now.strftime("%Y")
    cur.execute("SELECT movieid, title FROM public.movie WHERE releasedate = %s"
                "GROUP BY movieid, title ORDER BY MAX(avgrating) DESC LIMIT 5", (date,))
    movies = cur.fetchall()
    for movie in movies:
        print(movie[1])


def recommend_movie(cur, username):
    print("Here are movie recommendations based on your ratings and watch history:")

    cur.execute("SELECT movieid FROM public.rating WHERE username = %s  AND userrating >= 4 "
                "GROUP BY movieid ORDER BY MAX(userrating)", (username,))
    movies = cur.fetchall()
    if not movies:
        print("No recommendations")
    else:
        for movie in movies:
            cur.execute("SELECT title FROM public.movie WHERE movieid = %s", (movie,))
            mo = cur.fetchall()
            if len(mo) is not 0:
                m = mo[0][0]
                print(m)


def trend_options(curs, username):
    print("Welcome to the movie Trends menu!\n"
          "Here are your options:\n"
          "(1) Display most popular movies in the last 90 days\n"
          "(2) Display popular movies among friends\n"
          "(3) New Releases\n"
          "(4) Recommend movies\n")

    backgreet = "Welcome to the movie Trends menu!\n" \
                "Here are your options:\n" \
                "(1) Display most popular movies in the last 90 days\n" \
                "(2) Display popular movies among friends\n" \
                "(3) New Releases\n" \
                "(4) Recommend movies\n"

    while True:
        cmd = input("Enter your command: ")

        if cmd == "1":
            most_popular_movie_90days(curs)
            print(backgreet)
        elif cmd == "2":
            popular_movie_among_friends(curs, username)
            print(backgreet)
        elif cmd == "3":
            new_release(curs)
            print(backgreet)
        elif cmd == "4":
            recommend_movie(curs, username)
            print(backgreet)
        elif cmd == "q":
            print(backgreet)
            break
        else:
            print("Please enter a valid option!")