# 2018/03/05.....nginx:1.12 (stable/stretch/Dockerfile) -> mainline 1.13 stretch
# https://hub.docker.com/_/nginx/
FROM nginx:1.13
COPY nginx.conf /etc/nginx/nginx.conf
COPY server.conf /etc/nginx/conf.d/default.conf
RUN touch /var/log/nginx/access.log \
    && touch /var/log/nginx/error.log
