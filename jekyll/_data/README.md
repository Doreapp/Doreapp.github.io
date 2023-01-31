# The `_data` folder

This directory holds the actual content of the website, in an almost un-order way.

## Re-use

If you want to re-use this project, here are the description of the data files.

### Generalities

Each element of a list that is used to generate a data page can contain the following elements:

| Field | Description |
| --- | --- | 
| `page-name` | Name of the resulting file |
| `title` | Large page title | 
| `subtitle` | Page subtitle |
| `share-title` | Page title (in tab for example) |

### [me.yml](me.yml)

It contains the description of *my* profile. Each element is under the list format, so that *data pages* can be generated from it.

#### `me` 

The `me` key is used to generate the home page (`index.html`)

- [General fields](#generalities)
    - Where `page-name` shall remain `index`

#### `about` 

The `about` key generates the *About me* page (at `/about`)

- [General fields](#generalities)

| Field | Description |
| --- | --- | 
| `text` | Main text of the about page. For me, the answer to the appeal question |
| `list` | List of `name`/`description` elements. For me, answers to the appeal question |

### [schools.yml](schools)

The schools generates a set of pages at `/schools/xxx`.

- [General fields](#generalities)

| Field | Description |
| --- | --- | 
| `short-name` | Short name of the school, e.g. MIT |
| `long-name` | Long name of the school, e.g. Massachusetts Institute of Technology |
| `city` | Optional city of the school, e.g. Cambridge |
| `country` | Optional country of the school, e.g. USA |
| `description` | Long description for the school |
| `weblink` | Optional URL to the school's website |
| `start-date` | Optional date of your entrance in the school |
| `end-date` | Optional date the end of your studies in the school |
