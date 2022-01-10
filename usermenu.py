import userLR


def menu(conn, curs):
    print("Hi, welcome to your very own movie simulation!\n"
          "We have tons of movies in our great catalogue.\n"
          "Please choose how you would like to begin:\n"
          "(1): Login\n"
          "(2): Register\n"
          "(q): Quit\n"
          )

    lmenu = "Welcome to your User Login Menu!\n" \
            "Please enter your username and password down below:\n"

    rmenu = "Welcome to your User Register Menu!\n" \
            "Please enter your details as below:\n"

    while True:
        cmd = input("Enter your Command: ")
        if cmd == "1":
            print(lmenu)
            usnm = input("Enter your username: ")
            pswd = input("Enter your Password: ")
            lparams = [conn, curs, usnm, pswd]
            userLR.login(*lparams)

        elif cmd == "2":
            print(rmenu)
            fname = input("Enter your first name: ")
            lname = input("Enter your last name: ")
            usnm = input("Enter your username: ")
            email = input("Enter your email: ")
            pswd = input("Enter your password: ")
            rparams = [conn, curs, usnm, pswd, lname, fname, email]
            userLR.register(*rparams)

        elif cmd == "q" or cmd == "exit":
            print("Bye!")
            break

        else:
            print("Error, Please input either 1, 2 or q for your choice.")
