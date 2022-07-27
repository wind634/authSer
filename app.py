from datetime import timedelta

import requests
from celery import Celery
from flask import Flask, request
from flask_redis import FlaskRedis

from config import TOKEN_KEY, AUTH_HEADER, HOST_PATH

redis_client = FlaskRedis()
app = Flask(__name__)

redis_client.init_app(app)


app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['CELERYBEAT_SCHEDULE'] = {
        'refresh_token': {
            'task': 'refresh_token',
            'schedule': timedelta(seconds=300)
        }
}


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# 定时导入
@celery.task(name="refresh_token")
def refresh_token():
    print("定时任务：每10秒执行一次")


@app.route('/redirect_auth', methods=["GET"])
def redirect_auth():
    scope = request.args.get("scope", "")
    code = request.args.get("code", "")
    state = request.args.get("state", "")

    print("scope:%s, code:%s, state:%s" % (scope, code, state))
    headers = {
        'Authorization': AUTH_HEADER,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    resp =  requests.post("https://graph.fin-shine.com/oauth2/token",
                  headers=headers,
                  data={
                      "grant_type": "authorization_code",
                      "scope": "User.Profile.Read User.Profile.ReadWrite User.Files.Read User.Files.ReadWrite",
                      "code": code,
                      "redirect_uri": HOST_PATH+ "/redirect_auth",
                  }
                  )
    json_data= resp.json()
    token = json_data.get("access_token", "")
    if token:
        redis_client.set(TOKEN_KEY, token)
    return 'Success'


@app.route('/get_token', methods=["GET"])
def get_token():
    token = redis_client.get(TOKEN_KEY)
    if token:
        return token
    return ''


if __name__ == '__main__':
    app.run()