BASEDIR=$(dirname "$0")

cp $BASEDIR/../me.yml $BASEDIR/_data/

cd $BASEDIR && bundle exec jekyll serve --host 0.0.0.0
