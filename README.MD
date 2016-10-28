## Overview
This project aims to compare different methods of retrieving hirercharical data using Python (Flask Framework) and PostgreSQL. It will benchmark query, response time and also provides brief note on pros and cons of each methods.

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
There is a module in this application that can be use to insert test data in any specific model. `task.py` defines this job. It uses `PyInvoke` to execute. 

**Example Usage**: `invoke build --type aj`
For all possible options please see `invoke --help build`.

By default it inserts 10 rows, However you can modify this behaviour by updating *NUM_RECORDS* in `config.py`. If you are inserting significantly large number of rows you should also consider updating *CHUNK_SIZE* variable in `config.py`. This variable defines the number of rows after which SQLAlchemy should issue a commit command to the db. After successful completion of the job you can see records in your specified table.

**Note**: This job currently support single tree insertions. Future releases of this project will include multi-tree support.

## Methods Overview:
Following methods are used for benchmarking response and query time.
 
 - ### Adjcency List

 - ### Lineage Column

 - ### Nested Set

## Routes
Application provides following end-points:

| function      | Route             | Description  |
| ------------- |-------------------|--------------|
| get_subtree   | `/subtree/<id>`   | Get sub tree based on parent id provided in path params. It returns whole tree if no parent id is provided |
| get_root      | `/root/`          | Get list of all root nodes. Accepts no argument                                                            |
| get_leaf      | `/leaf/<id>`      | Get leaf nodes based on a parent id. If parent id has no direct leaf nodes it recursively traverse tree and return leaf nodes of decendents |
| get_child     | `/child/<id>`     | Get all immidiate childs based on parent id provided in path params                                        |
*Note: All routes are relative to base url*

**Query Params**: To test the requests mentioned above, you need to provide `type = aj`, `type = mp` and `type = ns` for adjcency list, materialized path views and nested set. If `type` param is absent, the request will throw an error.

**Example Request:** `www.mydomain.com/subtree/1/?type=ns`

## Benchmarking
HTTP request time benchmarking is performed using [wrk](https://github.com/wg/wrk). First test is done on 
`getSubTree()` with 100 tree nodes. 

Nested set produced following results:
![Nested Set Model Results](https://unsgdg.bl3301.livefilestore.com/y3mNFl8niH8yIeZFFQztmsvsgj9cUErVGo-YUmrAsocR108JUPgxLxc_wEzNs3AaMLJkKgPdTS6jLtAbkvonnYoiLTZ2RBchoLol5FRCluAR-AO6u9WnfIcGaZlLu70ZEkBVcKz7tgntRh0zDwe_04Zi-INhj3RZvytWLXmfVjKvYA?width=1301&height=744&cropmode=none)


## Related Links


