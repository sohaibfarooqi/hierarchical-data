## Overview
This project aims to compare different methods of storing and retrieving hirercharical data using Python (Flask Framework) and PostgreSQL. 

## Tools
Following tools are used for benchmarking
 - Python (3.5.2)
 - Flask (0.11.1)
 - Flask-SQLAlchemy (2.1)
 - PostgreSQL (9.5.4)
 - Marshmallow (2.9.1)

## Installation and Running
Run the following commands to set up the project and environment
 
 - `git clone https://github.com/SohaibFarooqi/hierarchical-data-model.git`
 - `virtualenv <your-env>`
 - `pip install -r requirements.txt`
 - `flask run`

If you wish to insert dummy records in your table, Please go through the next section before running the application.

## Populating Table Rows
`task.py` defines a job which can be triggered to insert rows in database table. It uses `PyInvoke` to execute. By default it inserts 10 rows, However you can 
modify this behaviour by updating *NUM_RECORDS* in `config.py`. If you are inserting significantly large number of rows you should also consider updating *CHUNK_SIZE* variable in `config.py`. This variable defines the number of rows after which SQLAlchemy should issue a commit command to the db. After successful completion of the job you can see records in your `first_model` table.

## Implemented Methods Overview:
Following methods are used for benchmarking response and query time.
 
 - ### Adjcency List

 - ### Lineage Column

 - ### Nested Set

## Routes
Application provides following end-points:
 - ### Adjcency List End-Points
    
    | function                     |Route                              |Description                                                                                 |
    |---------------------------|----------------------------------|------------------------------------------------------------------------------------------------|
    | get_subtree               |`/subtree/<id>`          	       |Get sub tree based on parent id provided in path params. It returns whole tree if no parent id is provided |
    | get_root                  |`/root/`                          |Get list of all root nodes. Accepts no argument                                                 |
    | get_leaf                  |`/leaf/<id>`          	           |Get leaf nodes based on a parent id. If parent id has no direct leaf nodes it recursively traverse tree and return leaf nodes of decendents      |
    | get_child                 |`/child/<id>`          	       |Get all immidiate childs based on parent id provided in path params                             |

*Note: All routes are relative to base url*

