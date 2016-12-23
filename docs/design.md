# A design for Problem Hub System of Project: Orange-Juice

## TODO list
* ~~design interactionsinteractions API.~~(abandoned)
* ~~design problem structure.~~
* ~~design file system structure.(core job to do)~~
* suport file layout
    * ~~json~~
    * html
    * markdown
* git submodule support

## modeling of the problem:
> with any other object we keep the job for API server.

### repo structure(file system struvture)
```
.
├── package1
│   ├── problem1
│   ├── problem2
├── package2
│   ├── problem1
│   ├── problem2
```
### problem structure
#### problem:

* id
* title.
* description.
* package.
* owner.
* type.
* lable.

```python
problem_sturcture = {
    "id": ObjectId,
    "title": str,
    "description": str,
    "package": str,
    "owner": str,
    "type": str,
    "lable": list
}
```

#### problem file
##### json

```python
problem_sturcture = {
    "title": str,
    "description": str,
    "type": str,
    "lable": list
}
```