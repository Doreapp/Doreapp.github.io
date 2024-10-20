# Development docker
FROM ruby:3.2.2-bullseye

RUN gem install jekyll bundler \
    && chmod -R 777 /usr/local
