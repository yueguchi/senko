# 書類選考AI API

##  環境構築

* `docker-compose up -d --build`
  
* bash
  * `docker exec -it [コンテナID] bash`

## 備考

* requiments.txtはpip installしたものからfreezeして吐き出したもの

## 設計

```
host:9999でnginx受け付けて、nginxからappサーバuwsgiに8080でproxyする。
uwsgiは8080で受けて、5000のflaskに接続する。
443はALBからしか使われないので、この領域はhttpになる。local以外のostは:80になる。
```

# jwt_tokenについて

```
デフォルトで
access tokens 15分
refresh tokens 30日
```

# redis

```
▼senko-app(python)

import redis
r = redis.StrictRedis(host='senko-redis', port=6379, db=0)
r.set("KEY", "VALUE")
print(r.get("KEY").decode())

▼redisコンテナ
$ docker exec -it **** bash
root@cc364fe05b17:/data# redis-cli 
127.0.0.1:6379> get KEY
"VALUE"
```

# migration

```
▼migrate
# python manage.py version_control
# python manage.py upgrade[ or downgrade]

▼Add
# python manage.py script "add hoges table"
```

