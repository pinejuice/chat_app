import responder
import psycopg2
import access_db as db

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
        resp.content = api.template('login.html', APPNAME='chat_app')

    async def on_post(self, req, resp):
        # postの場合
        data = await req.media()
        # connectionの生成
        conn = psycopg2.connect(f'host={host} port={port} user={users} dbname={dbnames} password={passwords}')
        # cursorの生成
        cur = conn.cursor()
        user_id = data.get('user_id')
        login_pw = data.get('password')
        login_tf, message, nick_name = db.check_user_info(cur, user_id, login_pw)
        conn.commit()
        if login_tf == False:
            loginredirect = '/top'
            resp.content = api.template('login.html', errmessages=message, APPNAME='chat_app')
            return

        resp.session['user_id'] = user_id
        resp.session['nick_name'] = nick_name
        api.redirect(resp, '/top')

@api.route('/top')
async def top(req, resp):
    resp.content = api.template('top.html')


if __name__ == '__main__':
    api.run(port=8888)
