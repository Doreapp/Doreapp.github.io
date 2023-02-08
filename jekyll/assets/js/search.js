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

const buildResultTextContent = (result) => {
    const wrapper = document.createElement("div");
    wrapper.classList.add("content-wrap");

    const title = document.createElement("h3");
    title.classList.add("post__title");
    title.innerText = result.title;
    wrapper.appendChild(title);

    if (result.subtitle) {
        const subtitle = document.createElement("span");
        subtitle.classList.add("post__subtitle");
        subtitle.innerText = result.subtitle;
        wrapper.appendChild(subtitle);
    }

    const description = document.createElement("p");
    description.classList.add("post__description");
    description.classList.add("description");
    description.innerText = result.description;
    wrapper.appendChild(description);

    if (result.skills) {
        const skillsContainer = document.createElement("div");
        skillsContainer.classList.add("skills");

        for (let skill of result.skills.split(" ; ")) {
            const skillElement = document.createElement("span");
            skillElement.classList.add("chip");
            skillElement.innerText = skill;
            skillElement.style.margin = "1px";
            skillsContainer.appendChild(skillElement);
        }

        wrapper.appendChild(skillsContainer);
    }
    return wrapper;
}

const buildResultImgContent = (result) => {
    if (result.coverimg) {
        const wrapper = document.createElement("div");
        wrapper.classList.add("image-wrap");

        const image = document.createElement("div");
        image.classList.add("image");
        image.style.backgroundImage = `url(${result.coverimg})`;
        image.setAttribute("data-img-src", result.coverimg);
        image.setAttribute("alt", "Thumbnail");
        wrapper.appendChild(image);
        return wrapper;
    }
}

const buildResultListItem = (result) => {
    const listItem = document.createElement("li");
    listItem.classList.add("post");
    listItem.classList.add("related");

    const linkElement = document.createElement("a");
    linkElement.href = result.url;
    listItem.appendChild(linkElement);

    const contentContainer = document.createElement("div");
    contentContainer.classList.add("flex");
    linkElement.appendChild(contentContainer);

    const textContent = buildResultTextContent(result);
    const imgContent = buildResultImgContent(result);
    contentContainer.appendChild(textContent);
    contentContainer.appendChild(imgContent);

    return listItem;
}

const displaySearchResults = (results) => {
    const container = document.getElementById('search-results');

    if (results.length) { // Are there any results?
        for (const result of results) {
            const resultElement = buildResultListItem(result);
            container.appendChild(resultElement);
        }
    } else {
        container.innerText = "No results found";
    }
}

(() => {
    window.addEventListener("load", () => {
        const searchTerm = getQueryVariable('query');

        if (searchTerm) {
            document.getElementById('search-box').setAttribute("value", searchTerm);

            let miniSearch = new MiniSearch({
                fields: ['title', 'subtitle', 'description', 'skills'], // fields to index for full-text search
                storeFields: ['title', 'url', 'subtitle', 'description', 'skills', 'coverimg'] // fields to return with search results
            })
            miniSearch.addAll(window.store);

            let results = miniSearch.search(searchTerm);
            displaySearchResults(results, window.store);
        }
    })
})()
