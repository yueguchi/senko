FROM python:3.6-stretch
COPY ./project /project
RUN pip install -r /project/requirements.txt

RUN apt-get update \
    && apt-get install -y mysql-client

# ポートは8080
EXPOSE 8080
# サーバー起動コマンド
CMD ["uwsgi","--ini","/project/uwsgi.conf"]
