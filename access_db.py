import psycopg2


def check_login(cur, user_id, login_pw):
    # ユーザー情報の取得
    SELECT_LOGIN_INFO = f'''SELECT user_id, login_pw, nick_name, icon FROM user_tbl WHERE user_id = '{user_id}';'''
    cur.execute(SELECT_LOGIN_INFO)
    user_info = cur.fetchall()
    # user_idが1つしかない場合以外はERROR
    if len(user_info) == 1:
        # パスワードが間違っていたらERROR
        if user_info[0][1] == login_pw:
            return True, '', user_info[0][2], user_info[0][3]
    return False, 'ユーザーID 又は パスワードが間違っています。', '', ''

def select_talk_user_info(cur, user_id):
    # 自身以外のユーザー一覧の取得
    SELECT_TALK_USER_INFO = f"""SELECT user_id, nick_name FROM user_tbl WHERE user_id != '{user_id}';"""
    cur.execute(SELECT_TALK_USER_INFO)
    nick_name_list = cur.fetchall()
    return len(nick_name_list), nick_name_list

def select_user_info(cur, user_id):
    # 自身のユーザー情報の取得
    SELECT_USER_INFO = f"""SELECT user_id, nick_name, icon FROM user_tbl WHERE user_id = '{user_id}';"""
    cur.execute(SELECT_USER_INFO)
    user_info = cur.fetchall()
    return user_info[0]

def update_user_info(cur, user_id, nick_name):
    UPDATE_USER_INFO_NULL = f"""UPDATE user_tbl set nick_name = '{nick_name}' WHERE user_id = '{user_id}';"""
    cur.execute(UPDATE_USER_INFO_NULL)

def insert_user_info(cur, user_id, nick_name, password):
    SELECT_USER_ID = f"""SELECT EXISTS (SELECT user_id FROM user_tbl WHERE user_id = '{user_id}');"""
    cur.execute(SELECT_USER_ID)
    user_exists = cur.fetchall()
    if user_exists[0][0] == True:
        return False
    else:
        INSERT_USER_INFO = f"""INSERT INTO user_tbl (user_id, nick_name, login_pw, icon) VALUES ('{user_id}', '{nick_name}', '{password}', NULL);"""
        cur.execute(INSERT_USER_INFO)
        return True
