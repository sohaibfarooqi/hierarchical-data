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
 
 - ### [Adjcency List](https://en.wikipedia.org/wiki/Adjacency_list)

 In the adjacency list model, each item in the table contains a pointer to its parent. The topmost element, in this case electronics, has a NULL value for its parent. The adjacency list model has the advantage of being quite simple
 While the adjacency list model can be dealt with fairly easily in client-side code, working with the model can be more problematic in pure SQL.

 **Example Data:**

 					|  id         | parent_id   |
					|-------------|-------------|
					|           1 |   NULL      |
					|           2 |      1      |
					|           3 |      2      |
					|           4 |      2      |
					|           5 |      2      |
					|           6 |      1      |
					|           7 |      6      |
					|           8 |      7      |
					|           9 |      6      |
					|          10 |      6      |


 - ### [Lineage Column (Materialized Path Views)](https://medium.com/notes-from-a-messy-desk/representing-trees-in-postgresql-cbcdae419022#.6666ewmcl)

 Lineage Column defines a `path` column which contains path of that node till root node. Path can be seperated with any character. Example `None.1.2.3`. This trick is really handy when searching for child and ansestor nodes. SQL `WITH` and `ANY` are really useful with this approach. 
 With Postgres one can define [GIN](https://www.postgresql.org/docs/9.5/static/gin.html) or [GIST](https://www.postgresql.org/docs/9.5/static/gist.html) indexes on [LTREE](https://www.postgresql.org/docs/9.5/static/ltree.html) dtype to perform really fast filtering of data.This trick can be used in creating related searches and creating hashtags.
 Drawbacks of this approach are, inserts, update and moving a node is really expensive operation since every time you have to recalculate path and update it.

 **Example data:**   


				| id          | parent_id   |  Path            |
				|-------------|-------------|------------------|
				|           1 |   NULL      | None             | 
				|           2 |      1      | None.1.2         |
				|           3 |      2      | None.1.2.3       |
				|           4 |      2      | None.1.2.4       |
				|           5 |      2      | None.1.2.5       |
				|           6 |      1      | None.1.6         |
				|           7 |      6      | None.1.6.7       |
				|           8 |      7      | None.1.6.7.8     |
				|           9 |      6      | None.1.6.9       |
				|          10 |      6      | None.1.6.10      |


 - ### [Nested Set](https://en.wikipedia.org/wiki/Nested_set_model)

 The nested set model is to number the nodes according to a tree traversal, which visits each node twice, assigning numbers in the order of visiting, and at both visits. This leaves two numbers for each node, which are stored as two attributes. Querying becomes inexpensive: hierarchy membership can be tested by comparing these numbers. Updating requires renumbering and is therefore expensive. Refinements that use rational numbers instead of integers can avoid renumbering, and so are faster to update, although much more complicated

 Nested sets are very slow for inserts because it requires updating left and right domain values for all records in the table after the insert. This can cause a lot of database thrash as many rows are rewritten and indexes rebuilt

 **Example Data:**


				| category    | lft | rgt |
				|-------------|-----|-----|
				|           1 |   1 |  20 |
				|           2 |   2 |   9 |
				|           3 |   3 |   4 |
				|           4 |   5 |   6 |
				|           5 |   7 |   8 |
				|           6 |  10 |  19 |
				|           7 |  11 |  14 |
				|           8 |  12 |  13 |
				|           9 |  15 |  16 |
				|          10 |  17 |  18 |


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
HTTP request time benchmarking is performed using [wrk](https://github.com/wg/wrk). Test is done on 
`getSubTree()` with 100 tree nodes. 

**Nested set:**
![Nested Set Model Results](https://unsgdg.bl3301.livefilestore.com/y3mNFl8niH8yIeZFFQztmsvsgj9cUErVGo-YUmrAsocR108JUPgxLxc_wEzNs3AaMLJkKgPdTS6jLtAbkvonnYoiLTZ2RBchoLol5FRCluAR-AO6u9WnfIcGaZlLu70ZEkBVcKz7tgntRh0zDwe_04Zi-INhj3RZvytWLXmfVjKvYA?width=1301&height=744&cropmode=none)

**Adjcency List:**
![Adjcency List Model Results](https://unsqdg.bl3301.livefilestore.com/y3mAD_BrOqi6iWyHEauLt-Kp_DnnmkHoXp2XsgMaslm2-u1DiwwOL5PrBBAbGokae3kXqoSmb_CSf2zwfzAMwEQFPRkYHYJs1BN3_nOtAmna6fPCyt3EmUASw3B7Qwmxgvu4HNoO-WUgNlZCebUKKzd9PB1KcGhoOXhGGEH_gZ-uEU?width=1301&height=744&cropmode=none)

**Materialized Path:**
![Materialized Path Model Results](https://unspdg.bl3301.livefilestore.com/y3mgV3Az3twJEXHKhTL8ybymtR0NJY-CwbGfh5vnfZgV497-GvhsnE6jlDFnrR5gGv9VBwFrg3vGU8FceGEH45FNPBJmQ2jcE26-bgdyVo0wbUnDoG8Z7ca8zNHorD2e7R4GKzeJdeTsRJmvb7R9QgjANTBJKffPk6qfWrPbzV3HiI?width=1301&height=744&cropmode=none)

## Helpful Links

 - [Joe Celko wrote the book on SQL Trees & Hiearichies](https://www.amazon.com/dp/1558609202/?tag=stackoverfl08-20)
 - [What are the Options for Storing Hierarchical Data in a Relational Database?](http://stackoverflow.com/questions/4048151/what-are-the-options-for-storing-hierarchical-data-in-a-relational-database)
- [Notes From a Messy desk](https://medium.com/notes-from-a-messy-desk/representing-trees-in-postgresql-cbcdae419022#.6666ewmcl)
- [Mike Hillyer guides to Hierarchical-Data](http://mikehillyer.com/articles/managing-hierarchical-data-in-mysql/)
