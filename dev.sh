# Development commands wrapper
PROJECT_NAME="portfolio"
DOCKER_IMAGE="${PROJECT_NAME}-dev"
ROOT_DIR="${PWD}"

docker_build() {
    # Build docker ccontainer
    docker build -t "${DOCKER_IMAGE}" .
}

## Run a command within docker
run() {
    if ! docker images -q --filter "reference=*$DOCKER_IMAGE" | grep -q .; then
        docker_build
    fi

    cmd="docker run\
        --network=host \
        -u $(id -u):$(id -g) \
        -v $(pwd):/opt/share \
        -w /opt/share"
    if [ -n "$CI" ]; then
        cmd="$(DOCKER_RUN) -t"
    fi

    echo "$cmd $@"
    eval "$cmd $@"
}

dev() {
    run -it $DOCKER_IMAGE cd jekyll && ./dev.sh
}

## Activate an interactive prompt within docker, with pnpm and such
it() {
    run -it $DOCKER_IMAGE bash
}
alias interactive=it

## Prints help message
help() {
    filename="$ROOT_DIR/dev.sh"
    max_length=$(grep -E '^\s*[a-zA-Z_]+\(\)' "$filename" | sed 's/().*//' | awk '{print length}' | sort -n | tail -1)

    # Read the current file and extract function names with descriptions
    echo Available commands

    grep -E '^\s*##|^\s*[a-zA-Z_]+\(\)' "$filename" | \
    awk -v max_length="$max_length" '
    BEGIN { OFS = "" }
    /^\s*##/ { desc = substr($0, 4); next }
    /^[a-zA-Z_]+\(\)/ && length(desc) > 0 {
        # Remove "()" from the function name
        func_name = substr($1, 1, length($1) - 2)
        # Print the function name followed by the description, aligned
        printf "  %-" max_length "s  %s\n", func_name, desc
        desc = ""
    }
    '
}

main() {
    echo "$1"
    if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
        return 0
    fi

    if [ -z "$1" ]; then
        help
    else
        "$@"
    fi
}

main $@
