# My resume/portfolio data holder

This repository is meant to store the data for my resume and portfolio.

It is also built to deploy a static website using `GitHub pages` and `Jekyll` offering a pretty representation of this data (see [jekyll subfolder](jekyll/README.md)).

## The data file: [`me.yml`](me.yml)

This file contains the description of my profile, for reuse in a portfolio or resume.

It shall respect a precise format. An example can be seen in [`me.yml` file](me.yml).

| Name | Description |
| --- | --- |
| `profile` | Single-element list |
| `profile[0].name` | Your name |
| `profile[0].subtitle` | [Optional] Additional details (e.g. your job) |
| `profile[0].share-title` | [Optional] Explicit name of the webpage |
| | |
| `about` | Single-element list |
| `about[0].subtitle` | [Optional] Any text describing your *about me* section |
| `about[0].share-title` | [Optional] Explicit name of the webpage |
| `about[0].text` | [Optional] Paragraph for the about page |
| `about[0].list` | [Optional] List of bullet points |
| `about[0].list[?].name` | Main text of the bullet point |
| `about[0].list[?].description` | Secondary text of the bullet point |
| | |
| `education` | |
| `education.schools` | List of schools (can be empty) |
| `education.schools[?].name` | School name |
| `education.schools[?].subtitle` | [Optional] Short subtitle for the school |
| `education.schools[?].share-title` | [Optional] Explicit name of the webpage |
| `education.schools[?].description` | Description of the school |
| `education.schools[?].weblink` | [Optional] URL of the school's website |
| | |
| `projects` | List of accomplished or on-going projects |
| `projects[?].title` | Short title/name of the project |
| `projects[?].description` | Description of the project, can be quite long |
| `projects[?].cover-img` | Path to a cover image for this project, from [jekyll folder](jekyll/) |
| `projects[?].subtitle` | [Optional] Project longer subtitle |
| `projects[?].start-date` | [Optional] Date of the project beginning (`dd-mm-yyyy`) |
| `projects[?].end-date` | [Optional] Date of the project ending (`dd-mm-yyyy`) |
| `projects[?].weblink` | [Optional] URL to the project result (or website) |
| `projects[?].source-code` | [Optional] URL to the project source code |
| `projects[?].skills` | [Optional] List of skills involved in the project |


## Automatic format check

If you want to check the format of your `me.yml` file, you can use `pyfolio` python library in [`tools` directory](tools/).
