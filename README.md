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

