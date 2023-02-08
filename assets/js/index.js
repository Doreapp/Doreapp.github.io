(() => {
    window.addEventListener("load", () => {
        // Init `View More` buttons
        const viewMore = (event) => {
            const parent = event.target.parentElement;
            const toDisplay = parent.querySelectorAll(".view-more")
            let i = 0;
            for (element of toDisplay) {
                element.classList.remove("view-more");
                if (++i >= 3) {
                    break;
                }
            }
            if (toDisplay.length <= 3) { // Hide the button
                target.style.display = "none";
            }
        }
        document.querySelectorAll("button.view-more-button").forEach((button) => {
            button.onclick = viewMore;
        })
    })
})()