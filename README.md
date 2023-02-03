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
| `profile[0].email` | [Optional] Email where to contact you |
| `profile[0].github` | [Optional] GitHub username,  e.g. `Doreapp` |
| `profile[0].linkedin` | [Optional] LinkedIn id (after `linkedin.com/in/` in URL) |
| `profile[0].stackoverflow` | [Optional] StackOverFlow  username |
| `profile[0].google-play` | [Optional] Full google play weblink (to an app or list of apps) |
| `profile[0].gitlab` | [Optional] GitLab username |
| `profile[0].facebook` | [Optional] [**Not tested**] Facebook id |
| `profile[0].twitter` | [Optional] [**Not tested**] Twitter id |
| `profile[0].reddit` | [Optional] [**Not tested**] Reddit id |
| `profile[0].snapchat` | [Optional] [**Not tested**] Snapchat id |
| `profile[0].instagram` | [Optional] [**Not tested**] Instagram id |
| `profile[0].youtube` | [Optional] [**Not tested**] Youtube id |
| `profile[0].spotify` | [Optional] [**Not tested**] Spotify id |
| `profile[0].telephone` | [Optional] [**Not tested**] Phone number |
| `profile[0]....` | [Optional] [**Not tested**] And others... See [social-networks-links.html](jekyll/_includes/social-networks-links.html)|
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
| `education.schools[?].cover-img` | Path to a cover image for this school, from [jekyll folder](jekyll/) |
| `education.schools[?].subtitle` | [Optional] Short subtitle for the school |
| `education.schools[?].share-title` | [Optional] Explicit name of the webpage |
| `education.schools[?].description` | [Optional] Description of the school |
| `education.schools[?].weblink` | [Optional] URL of the school's website |
| `education.schools[?].start-date` | [Optional] Date of your entrance in this school (`dd-mm-yyyy`) |
| `education.schools[?].end-date` | [Optional] Date when you left this school (`dd-mm-yyyy`) |
| | |
| `work` | |
| `work.companies` | List of companies (can be empty) |
| `work.companies[?].name` | Company name |
| `work.companies[?].cover-img` | Path to a cover image for this company, from [jekyll folder](jekyll/) |
| `work.companies[?].subtitle` | [Optional] Short subtitle for the company |
| `work.companies[?].share-title` | [Optional] Explicit name of the webpage |
| `work.companies[?].description` | [Optional] Description of the company |
| `work.companies[?].weblink` | [Optional] URL of the company's website |
| `work.companies[?].start-date` | [Optional] Date of your entrance in this company (`dd-mm-yyyy`) |
| `work.companies[?].end-date` | [Optional] Date when you left the company (`dd-mm-yyyy`) |
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
