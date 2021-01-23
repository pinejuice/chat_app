import responder
import psycopg2
import os

import access_db as db

app_name = 'チャットーク'
api = responder.API(
    static_dir='./static',
    templates_dir='./templates'
)
# connect postgreSQL
host = '127.0.0.1'
port = '5432'
users = 'postgres'
dbnames = 'chat_app'
passwords = 'postgres'

@api.route('/login')
class login():
    async def on_get(self, req, resp):
        # getの場合
        resp.content = api.template('login.html', APPNAME=app_name)

    async def on_post(self, req, resp):
        # postの場合
        data = await req.media()
        user_id = data.get('user_id')
        login_pw = data.get('password')
        # ログイン処理
        login_tf, message, nick_name, icon = db.check_login(cur, user_id, login_pw)
        conn.commit()
        if login_tf == False:
            loginredirect = '/login'
            resp.content = api.template('login.html', errmessages=message, APPNAME=app_name)
            return

        resp.session['user_id'] = user_id
        resp.session['nick_name'] = nick_name
        resp.session['icon'] = icon
        api.redirect(resp, '/top')

@api.route('/sign_up')
class sign_up():
    async def on_get(self, req, resp):
        # getの場合
        resp.content = api.template('sign_up.html', APPNAME=app_name)

    async def on_post(self, req, resp):
        # postの場合
        data = await req.media()
        user_id = data.get('user_id')
        login_pw = data.get('password')
        nick_name = data.get('nick_name')
        user_exists = db.insert_user_info(cur, user_id, nick_name, login_pw)
        if user_exists == True:
            api.redirect(resp, '/created')
        else:
            message = "このユーザIDは現在使用できません。"
            resp.content = api.template('sign_up', errmessages=message, APPNAME=app_name)
            return

@api.route('/created')
async def top(req, resp):
    resp.content = api.template(
        'created.html',
        page_title='アカウント発行完了',
        APPNAME=app_name
    )

@api.route('/top')
async def top(req, resp):
    # 必要情報の取得
    user_num, user_list = db.select_talk_user_info(cur, resp.session['user_id'])
    conn.commit()
    resp.content = api.template(
        'top.html',
        page_title='トップ',
        APPNAME=app_name,
        user_num=user_num,
        user_list=user_list,
        icon=resp.session['icon']
    )

@api.route("/chat/{who}")
def chat(req, resp, *, who):
    # 必要情報の取得
    user_num, user_list = db.select_talk_user_info(cur, resp.session['user_id'])
    conn.commit()
    resp.content = api.template(
        'chat.html',
        who=who,
        page_title='チャット',
        APPNAME=app_name,
        user_num=user_num,
        user_list=user_list,
        icon=resp.session['icon']
    )

@api.route('/user-setting')
async def user_setting(req, resp):
    # 必要情報の取得
    user_num, user_list = db.select_talk_user_info(cur, resp.session['user_id'])
    user_id, nick_name, icon = db.select_user_info(cur, resp.session['user_id'])
    conn.commit()
    resp.content = api.template(
        'user_setting.html',
        page_title='ユーザー設定',
        APPNAME=app_name,
        user_num=user_num,
        user_list=user_list,
        user_id=user_id,
        nick_name=nick_name,
        icon=icon
    )

@api.route('/user-setting-update')
async def user_setting_update(req, resp):
    data = await req.media()
    nick_name = data.get('nick_name')
    # icon = data.get('user_info_icon')
    # if icon != None:
    #     @api.background.task
    #     def _upload(icon, file_path):
    #         f = open(file_path, 'wb')
    #         f.write(icon)
    #         f.close()

    #     root, ext = os.path.splitext(icon)
    #     user_icon_path = '/static/img/user_img/' + resp.session['user_id'] + ext
    #     _upload(icon, user_icon_path)
    #     icon = user_icon_path
        
    db.update_user_info(cur, resp.session['user_id'], nick_name)
    api.redirect(resp, '/user-setting')
 
@api.route('/about')
async def about(req, resp):
    resp.content = api.template(
        'about.html',
        page_title=f'{app_name}について',
        APPNAME=app_name,
        icon=resp.session['icon']
    )

@api.route('/logout')
async def logout(req, resp):
    resp.session['user_id'] = ''
    resp.session['nick_name'] = ''
    resp.session['icon'] = ''
    resp.content = api.template('login.html', APPNAME=app_name)


if __name__ == '__main__':
    # connectionの生成
    conn = psycopg2.connect(f'host={host} port={port} user={users} dbname={dbnames} password={passwords}')
    # cursorの生成
    cur = conn.cursor()
    api.run(port=8888)
