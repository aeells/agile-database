agile-database
==============
Rewrite of continuous-db in Python (which integrates better with Boto and Fabric).
Previous incarnation also needed to be embedded within the using project - control has been inverted such that agile-database is an external dependency. 

Usage
-----
```python
python bin/agile_database baseline|patch|rollback <path_to_sql_scripts>
```

Requirements
------------
Standard directory structure required at root of <i>\<path_to_sql_scripts\></i>:

- config/
    - agile-database.yaml
- baseline/
    - install.txt
    - table-a.sql
    - table-b.sql
- patches/
    - 1/
        - install.txt
        - patch/
            - a.sql
            - b.sql
        - rollback/
            - a.sql
            - b.sql
    - 2/
        - install.txt
        - patch/
            - c.sql
            - d.sql
        - rollback/
            - c.sql
            - d.sql

Assuming the above example, where none of the patches in vanity subdirectories (1, 2) have yet been applied, patches will be executed in order:
  a, b, c, d.sql
Rollbacks only occur on the most recent patch so as to avoid rolling back to the beginning of time. They occur in reverse vanity subdirectory order and then reverse order within the install.txt:
  d, c, b, a.sql
  


