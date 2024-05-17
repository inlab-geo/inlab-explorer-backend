# Backend for [InLab Explorer](https://inlab.au/inlab-explorer)

This package is designed to parse hierarchical classification of what are included 
in CoFI, Espresso, and CoFI Examples. The generated JSON file will be loaded into the 
public folder in the frontend.

[A workflow](https://github.com/inlab-geo/inlab-explorer-backend/actions/workflows/jobs.yaml) 
is triggered automatically when there are changes in any of the cofi, cofi-examples 
and espresso repositories.

## Generate data files manually

If you want to change any content, please clone this repo:

```bash
$ git clone https://github.com/inlab-geo/inlab-explorer-backend.git
$ cd inlab-explorer-backend
```

To run the backend manually, please first place the 'cofi', 'espresso', and 
'cofi-examples' repositories under the 'pysearch_tool' directory. Then execute the 
following command:

```bash
python main.py
```

This command generates three JSON files. Copy them into the 'public' folder in the 
[frontend](https://github.com/inlab-geo/inlab-explorer) for visualisation update.

## Developer reference

- `config.py`: configurations including path, working directories, link prefix, etc.
- `main.py`: the entrypoint of this program. It initiates the search script in the 
  `pysearch` folder (`dir_search.py`), and then packages the tree. 
- `relation_dict.py`: the tree data structure is defined here

The GitHub Action for the backend works by first downloading the source files, then running the script, and finally pushing the generated JSON files (which are located in the root folder) to the 'public' folder in the frontend.
