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
