FROM python:3.6-stretch
COPY ./project /project
RUN pip install -r /project/requirements.txt

# ポートは8080
EXPOSE 8080
# サーバー起動コマンド
CMD ["uwsgi","--ini","/project/uwsgi.conf"]
