const getQueryVariable = (variable) => {
    const query = window.location.search.substring(1);
    const vars = query.split('&');
    for (let i = 0; i < vars.length; i++) {
        const pair = vars[i].split('=');
        if (pair[0] === variable) {
            return decodeURIComponent(pair[1].replace(/\+/g, '%20'));
        }
    }
}

const displaySearchResults = (results) => {
    console.log(results)
}

(() => {
    window.addEventListener("load", () => {
        const searchTerm = getQueryVariable('query');

        if (searchTerm) {
            document.getElementById('search-box').setAttribute("value", searchTerm);

            let miniSearch = new MiniSearch({
                fields: ['title', 'subtitle', 'description', 'skills'], // fields to index for full-text search
                storeFields: ['title', 'url', 'subtitle', 'description', 'skills', 'cover-img'] // fields to return with search results
            })
            miniSearch.addAll(window.store);

            let results = miniSearch.search(searchTerm);
            displaySearchResults(results, window.store);
        }
    })
})()
