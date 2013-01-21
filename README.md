agile-database
==============
Rewrite of continuous-db in Python, which integrates better with Boto and Fabric (AWS tooling) and also allows for unit test cases.
<br/>The previous incarnation of this project also needed to be embedded within the using project - control has been inverted here such that agile-database is an external dependency. 

Features
--------
- Automated patching of database on project build (Maven, Ant etc) - no need to notify other developers, CI environments or release managers of your scripts.
- Automated rollback in reverse patch order. This step can never be fully guaranted but you can build test phases into your release lifecycle such as patch, rollback, patch in CI to ensure consistency.
- Full version control, including baseline scripts to enable complete rebuilds and new environments, and checksum verification of script signature.
- Full audit history of baseline, patch and rollback script execution for each database instance.

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

Behaviour
---------
Each patch and rollback execution is idempotent which is achieved by simply grouping the unapplied patches by a stateful release number, and incrementing this release number on patches but not on rollbacks. 

Assuming the above example, where none of the patches in vanity subdirectories (1, 2) have yet been applied, patches will be executed in order:<br/>
- a, b, c, d.sql<br/>

Rollbacks only occur on the most recent patch so as to avoid rolling back to the beginning of time. They occur in reverse vanity subdirectory order (2, 1) and then reverse order within the install.txt:<br/>
- d, c, b, a.sql
