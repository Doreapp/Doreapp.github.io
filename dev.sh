if [ ! -z $1 ]
then
    rm -rf "$1-tmp/"
    cp "me.$1.yml" "jekyll-$1/_data/me.yml"
    make -C tools translate_$1
    cd "$1-tmp/"
else
    cd "jekyll/"
fi

./dev.sh
