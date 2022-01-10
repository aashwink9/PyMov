def createCol(conn, curs, usnm):
    cname = input("Create a collection name: ")
    if len(cname) > 18:
        print("Collection name is too long! Please try again.")

    else:
        # -------------Check if collection exists for this user---------------------
        curs.execute("SELECT colname FROM public.usercollection WHERE username = %s AND colname = %s ", (usnm, cname))
        exists = curs.fetchone()
        # --------------------------------------------------------------------------

        if exists is None:
            curs.execute("INSERT INTO public.usercollection (username, colname) VALUES(%s,%s)", (usnm, cname))
            conn.commit()
            print("Collection created Successfully!")

        else:
            print("Collection Name already exists! Please choose another name\n")


def modifyName(conn, curs, usnm):
    cname = input('Enter the collection you want to modify: ')

    # -------------Check if collection exists---------------------
    curs.execute("SELECT colname FROM public.usercollection WHERE username = %s AND colname = %s", (usnm, cname))
    exists = curs.fetchone()
    # ------------------------------------------------------------

    if exists:
        newname = input("Collection found!\n Enter the new name of your collection: ")
        getcid = "SELECT collectionid FROM public.usercollection WHERE colname = %s"
        curs.execute(getcid, (cname,))
        cid = curs.fetchone()[0]
        curs.execute("UPDATE public.usercollection SET colname = %s WHERE collectionid = %s", (newname, cid))
        conn.commit()
        print("Changed the collection name to ", newname, " Successfully!")


"""
Checks if a collection exists
"""


def check_col(curs, usnm):
    getcols = "SELECT collectionid FROM public.usercollection WHERE username = %s"
    curs.execute(getcols, (usnm,))
    colst = curs.fetchall()

    if colst is None:
        return False
    else:
        return True


def viewcollections(curs, usnm):
    getcols = "SELECT colname FROM public.usercollection WHERE username = %s"
    curs.execute(getcols, (usnm,))
    colst = curs.fetchall()

    if colst is not None:
        total_cols = ""
        print("Here is a list of your collections!")

        for i in range(0, len(colst)):
            total_cols += str(i + 1) + ". " + colst[i][0] + "\n"
        print(total_cols)
    else:
        print("Hmmm it looks like you don't have any collections!\n"
              "Please go back and create one!")


def view_single_col(curs, usnm):
    if check_col(curs, usnm):
        cname = input("Enter the name of the collection you want to view: ")
        curs.execute("SELECT collectionid FROM usercollection WHERE colname = %s", (cname,))
        exists = curs.fetchone()
        if exists is not None:
            colid = exists[0]
            curs.execute("SELECT movieid FROM public.moviecollection WHERE collectionid = %s", (colid,))
            moviexist = curs.fetchall()
            if moviexist is not None:
                curs.execute("SELECT movie.title FROM public.moviecollection INNER JOIN public.movie on "
                             "(moviecollection.movieid = movie.movieid) WHERE moviecollection.collectionid = %s",
                             (colid,))
                movielst = curs.fetchall()
                movies = ""
                print("Here are the movies in this collection:\n")
                for i in range(0, len(movielst)):
                    movies += "Movie " + str(i + 1) + ": " + movielst[i][0] + "\n"

                print(movies)

            else:
                print("Looks like this collection does not have any movies in it\n"
                      "Please go back and add some movies to your collection.")

        else:
            print("Error, please enter a valid collection")

    else:
        print("It looks like you have not made any collections yet\n"
              "Please go back to the collections menu and and make one.")


def addmovie(conn, curs, usnm):
    if check_col(curs, usnm):
        colname = input("Enter the collection you want to add a movie to: ")

        curs.execute("SELECT collectionid FROM public.usercollection WHERE colname = %s", (colname,))
        colexists = curs.fetchone()

        if colexists is not None:
            colid = colexists[0]
            getmov = input("Collection selected! Enter the name of a movie you want to add: ")
            curs.execute("SELECT title FROM public.movie WHERE title LIKE %(getmov)s",
                         ({'getmov': '%{}%'.format(getmov)}))
            movexists = curs.fetchone()

            if movexists is not None:
                movtitle = movexists[0]
                curs.execute("SELECT movieid FROM public.movie WHERE title = %s", (movtitle,))
                movid = curs.fetchone()[0]
                curs.execute("SELECT moviecolid from public.moviecollection WHERE movieid = %s AND collectionid = %s",
                             (movid, colid))
                alreadyder = curs.fetchone()

                if alreadyder is None:
                    curs.execute("INSERT INTO public.moviecollection (movieid, collectionid) VALUES(%s,%s)",
                                 (movid, colid))
                    conn.commit()
                    print("Movie", movtitle, "added to the collection!")

                else:
                    print("Movie already in collection!")
            else:
                print("Error, please select a valid movie!")
        else:
            print("Collection not found, please try again")
    else:
        print("It looks like you have not made any collections yet\n"
              "Please go back and make one.")


def removemovie(conn, curs, usnm):
    if check_col(curs, usnm):
        colname = input("Enter the collection you want to remove a movie from: ")
        curs.execute("SELECT collectionid FROM public.usercollection WHERE colname = %s", (colname,))
        colexists = curs.fetchone()

        if colexists is not None:
            colid = colexists[0]
            curs.execute("SELECT movieid FROM public.moviecollection WHERE collectionid = %s", (colid,))
            empty = curs.fetchall()

            if empty is not None:
                moviename = input("Collection selected! Please enter the name of the movie you'd like to remove: ")
                curs.execute("SELECT movieid FROM public.movie WHERE title = %s", (moviename,))
                movidexists = curs.fetchone()

                if movidexists is not None:
                    movid = movidexists[0]
                    curs.execute("SELECT movieid FROM public.moviecollection WHERE movieid = %s", (movid,))
                    movieincollection = curs.fetchone()

                    if movieincollection is not None:
                        curs.execute("DELETE FROM public.moviecollection WHERE movieid = %s AND collectionid = %s",
                                     (movid, colid))
                        conn.commit()
                        print("Movie removed successfully!")

                    else:
                        print("This movie does not exist in your collection, please select a valid movie!")

                else:
                    print("Error, Please enter a valid movie!")


            else:
                print("Looks like this collection is already empty\n"
                      "Please try again for a different collection!")

    else:
        print("It looks like you have not made any collections yet\n"
              "Please go back and make one.")


def collection_options(conn, curs, usnm):
    print("Welcome to you collections menu! Here are your options:\n"
          "(1) Create a collection\n"
          "(2) Rename a collection\n"
          "(3) View your Collections\n"
          "(4) View a Collection\n"
          "(5) Add Movie to Collection\n"
          "(6) Remove Movie From Collection\n"
          "(q) Go back\n"
          )

    backgreet = "\nWelcome back to your collections menu simulation!\n " \
                "Here are your options:\n" \
                "(1) Create a collection\n" \
                "(2) Rename a collection\n" \
                "(3) View your Collections\n" \
                "(4) View a Collection\n" \
                "(5) Add Movie to Collection\n" \
                "(6) Remove Movie From Collection\n" \
                "(q) Go back\n"
    while True:
        options = input("Enter your option: ")
        if options == "1":
            createCol(conn, curs, usnm)
            print(backgreet)
        elif options == "2":
            modifyName(conn, curs, usnm)
            print(backgreet)
        elif options == "3":
            viewcollections(curs, usnm)
            print(backgreet)
        elif options == "4":
            view_single_col(curs, usnm)
            print(backgreet)
        elif options == "5":
            addmovie(conn, curs, usnm)
            print(backgreet)
        elif options == "6":
            removemovie(conn, curs, usnm)
            print(backgreet)

        elif options == "q":
            print(backgreet)
            break
        else:
            print("Error, please select a valid option!")
