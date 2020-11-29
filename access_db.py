import psycopg2


def check_user_info(cur, user_id, login_pw):
    # ユーザ情報の取得
    SELECT_LOGIN_INFO = f'''SELECT user_id, login_pw, nick_name FROM user_tbl WHERE user_id = '{user_id}';'''
    cur.execute(SELECT_LOGIN_INFO)
    user_info = cur.fetchall()
    # user_idが1つしかない場合以外はERROR
    if len(user_info) == 1:
        # パスワードが間違っていたらERROR
        if user_info[0][1] == login_pw:
            return True, '', user_info[0][2]
    return False, 'ユーザーID 又は パスワードが間違っています。', ''
