# ogp_functions
Python package for working with the Open Geography Portal data



## API

### get_available_csv_file_names

```python
get_available_csv_file_names(
        )
```

### download_and_import_data

```python
download_and_import_data(
        csv_file_names = None,
        data_folder = '_data',
        database_name = 'ogp_data.sqlite',
        verbose=False
        )
```

### get_ogp_field_names_in_database

```python
get_ogp_field_names_in_database(
        data_folder = '_data',
        database_name = 'ogp_data.sqlite',
        )
```

### get_ogp_table_names_in_database

```python
get_ogp_table_names_in_database(
        data_folder = '_data',
        database_name = 'ogp_data.sqlite'
```
