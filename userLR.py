from datetime import datetime
import simulateusers


def inc_follower_count(conn, curs, user):
    # --------------------Increase follower count for the person followed by 1-----------------------------------
    curs.execute("SELECT followers from public.users WHERE username = %s", (user,))
    f = curs.fetchone()[0]
    fcount = int(f)
    fcount += 1
    strfcount = str(fcount)
    curs.execute("UPDATE public.users SET followers = %s WHERE username = %s", (strfcount, user))
    conn.commit()


def dec_follower_count(conn, curs, user):
    # -------------------Decrease follower count for the user that got unfollowed by 1---------------------------
    curs.execute("SELECT followers from public.users WHERE username = %s", (user,))
    f = curs.fetchone()[0]
    fcount = int(f)
    if fcount > 0:
        fcount -= 1
    strfcount = str(fcount)
    curs.execute("UPDATE public.users SET followers = %s WHERE username = %s", (strfcount, user))
    conn.commit()


def check_follow(curs, user, follower):
    # check if the user is already followed
    curs.execute("SELECT friendid FROM public.userfollow WHERE username = %s AND follower = %s", (user, follower))
    fid = curs.fetchone()

    if fid is not None:
        return True
    else:
        return False


def follow_usr(conn, cur, username, usertofollow):
    # check if the person to follow is already followed
    if not check_follow(cur, usertofollow, username):
        cur.execute("INSERT INTO public.userfollow (username, follower) VALUES (%s, %s)", (usertofollow, username))
        inc_follower_count(conn, cur, usertofollow)
        conn.commit()
        print("User", usertofollow, "followed successfully!")
    else:
        print("You already follow this user!")


def unfollow_usr(conn, curs, username, usertounfollow):
    # check if the person to follow is already followed
    if check_follow(curs, usertounfollow, username):
        curs.execute("DELETE FROM public.userfollow WHERE username = %s AND follower = %s", (usertounfollow, username))
        dec_follower_count(conn, curs, usertounfollow)
        conn.commit()
        print("User", usertounfollow, "unfollowed Successfully!")
    else:
        print("Can't unfollow a user you're not following!")


def search_user(curs, option, inp):
    if option == "email":
        curs.execute("SELECT username from public.users WHERE email = %s", (inp,))
        userfound = curs.fetchone()

        if userfound is not None:
            return userfound[0]
        else:
            return

    elif option == "usnm":
        curs.execute("SELECT username from public.users WHERE username = %s", (inp,))
        userfound = curs.fetchone()
        if userfound is not None:
            return userfound[0]
        else:
            print("user not found!")
            return


def login(conn, cur, u, p):
    last_access = datetime.now()
    cur.execute("select username from public.users where username =  %s", (u,))
    uexists = cur.fetchone()

    cur.execute("select password from public.users where password =  %s", (p,))
    pexists = cur.fetchone()

    if uexists and pexists:
        username = uexists[0]
        password = pexists[0]
        cur.execute("select password from public.users where username =  %s", (username,))
        pas = cur.fetchone()
        cur.execute("select username from public.users where username =  %s", (username,))
        username = cur.fetchone()[0]
        if pas[0] != password:
            print("Password is wrong")
        else:
            cur.execute("UPDATE public.users SET lastaccessdate = %s WHERE username = %s", (last_access, username,))
            print("Successfully logged in! On", last_access)
            simulateusers.simulate(conn, cur, username)

            conn.commit()

    else:
        print("Your username or password is incorrect,\n"
              "Please enter a valid combination.\n\n"
              "Welcome back to the movies simulation,\n"
              "Please choose one of the options below:\n"
              "(1): Login\n"
              "(2): Register\n"
              "(q): Quit\n"
              )


def register(conn, cur, username, password, lastname, firstname, email):
    register_time = datetime.now()
    cur.execute("select username from public.users where username = %s", (username,))
    uexists = cur.fetchone()

    if uexists is None:
        cur.execute("insert into public.users (username, password, firstname, lastname, creationdate, lastaccessdate, "
                    "email)" "VALUES(%s,%s,%s,%s,%s,%s,%s)",
                    (username, password, firstname, lastname, register_time, register_time, email))
        conn.commit()
        print("Registered successfully!")
        simulateusers.simulate(conn, cur, username)
    else:
        print("\nUsername already taken!\n\n"
              "Welcome back to the movies simulation,\n"
              "Please choose one of the options below:\n"
              "(1): Login\n"
              "(2): Register\n"
              "(q): Quit\n"
              )
