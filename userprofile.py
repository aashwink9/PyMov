def view_num_collections(curs, usnm):
    getcols = "SELECT colname FROM public.usercollection WHERE username = %s"
    curs.execute(getcols, (usnm,))
    colst = curs.fetchall()

    if colst is not None:
        return len(colst)
    else:
        return 0


def get_num_followers(curs, usnm):
    curs.execute("SELECT followers FROM public.users WHERE username = %s", (usnm,))
    followerlst = curs.fetchone()
    followers = followerlst[0]
    return followers


def get_num_following(curs, usnm):
    curs.execute("SELECT username FROM public.userfollow WHERE follower = %s", (usnm,))
    following = curs.fetchall()
    if following is None:
        return 0
    else:
        return len(following)


def top_ten_movie(cur, username):
    cur.execute("SELECT movieid FROM public.rating WHERE username = %s"
                "GROUP BY ratingid, username, userrating, movieid ORDER BY MAX(userrating) DESC LIMIT 10", (username,))
    movies = cur.fetchall()
    if not movies:
        print("No movie has been rated by this user")
    else:
        for movie in movies:
            cur.execute("SELECT title FROM public.movie WHERE movieid = %s", (movie,))
            mo = cur.fetchall()
            if len(mo) is not 0:
                m = mo[0][0]
                print(m)


def view_profile(curs, usnm):
    numcols = view_num_collections(curs, usnm)
    numfollowers = get_num_followers(curs, usnm)
    numfollowing = get_num_following(curs, usnm)
    details = "Here are " + usnm + "'s details:\n" + "Number of Collections: " + str(numcols) + "\n" + "Number of " \
                                                                                                       "followers: " \
              + str(numfollowers) + "\n" + "Number of following: " + str(numfollowing) + "\n "
    print(details)

    print("Top 10 movies by this user\n (if they have not rated enough movies it'll display all the movies they have "
          "rated so far)\n")
    top_ten_movie(curs, usnm)
