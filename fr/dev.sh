BASEDIR=$(dirname "$0")

cp $BASEDIR/../me.fr.yml $BASEDIR/_data/me.yml

cd $BASEDIR && bundle exec jekyll serve -b /fr --host 0.0.0.0
