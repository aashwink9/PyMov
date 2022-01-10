import usercollection
import movie
import userLR
import userprofile


def search_users(conn, curs, usnm):
    print("Welcome to your Users Options Menu! To follow or unfollow someone,\n"
          "You'll need to search for the user first.\n")
    while True:
        search = input("Enter whether you'd like to search by email or username (email/usnm/q to exit): ")

        if search == "email":
            email = input("Enter the email for this user: ")
            targetuser = userLR.search_user(curs, search, email)
            if targetuser is not None:
                user_options(conn, curs, usnm, targetuser)
            else:
                print("User not found! Please Try again.")

        elif search == "usnm":
            usr = input("Enter the username for this user: ")
            targetuser = userLR.search_user(curs, search, usr)

            if targetuser is not None:
                user_options(conn, curs, usnm, targetuser)
            else:
                print("User not found! Please Try again.")

        elif search == "q":
            print("Okay, going back!")
            print("Welcome back to your movies simulation!\n"
                  "Here are your options:\n"
                  "(1) Collection Options\n"
                  "(2) Movie Options\n"
                  "(3) Users\n"
                  "(q) Logout\n")
            break

        else:
            print("Error, please enter a valid option!")


def user_options(conn, curs, usnm, targetuser):
    print("User Found! Here are your options:\n"
          "(1) Follow\n"
          "(2) Unfollow\n"
          "(3) View Profile\n"
          "(q) Go back")

    backgreeting = "\nWelcome back to the options for the user " + targetuser + " Here are your options:\n" \
                                                                                "(1) Follow\n" \
                                                                                "(2) Unfollow\n" \
                                                                                "(3) View Profile\n" \
                                                                                "(q) Go back"

    while True:
        inp = input("Enter your command: ")

        if inp == "1":
            if usnm == targetuser:
                print("You can't follow yourself!")
            else:
                userLR.follow_usr(conn, curs, usnm, targetuser)
                print(backgreeting)
            break
        elif inp == "2":
            if usnm == targetuser:
                print("You can't unfollow yourself!")
            else:
                userLR.unfollow_usr(conn, curs, usnm, targetuser)
                print(backgreeting)
            break
        elif inp == "3":
            userprofile.view_profile(curs, targetuser)
            print(backgreeting)
        elif inp == "q":
            print("Welcome back to your Follow Options Menu! To follow or unfollow someone,\n"
                  "You'll need to search for the user first.\n")
            break
        else:
            print("Error, please enter a valid option!")


def simulate(conn, curs, usnm):
    print("Welcome to your simulation!\n"
          "Here are your options:\n"
          "(1) Collection Options\n"
          "(2) Movie Options\n"
          "(3) Users\n"
          "(q) Logout\n")

    while True:
        cmd = input("Enter your command: ")

        if cmd == "1":
            usercollection.collection_options(conn, curs, usnm)
        elif cmd == "2":
            movie.movie_options(conn, curs, usnm)
        elif cmd == "3":
            search_users(conn, curs, usnm)
        elif cmd == "q":
            print("Welcome back to your Login Screen!\n"
                  "Please choose how you would like to begin:\n"
                  "(1): Login\n"
                  "(2): Register\n"
                  "(q): Quit\n"
                  )
            break
        elif cmd == "exit":
            print("Bye!")
            exit()
        else:
            print("Error, please enter a valid command out of these:\n"
                  "(1) Collection Options\n"
                  "(2) Movie Options\n"
                  "(3) Users\n"
                  "(q) Logout\n")
