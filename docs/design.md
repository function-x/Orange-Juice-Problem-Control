# A design for Problem Hub System of Project: Orange-Juice

## TODO list
### basic
* ~~design interactions API.~~
* ~~design problem structure.~~
* ~~design file system structure.(core job to do)~~
* suport file layout.
    + ~~json~~
    + html
    + markdown
* git submodule support.
* httpListner provide APIserver API.
* payload poster.
* manage methods or class.
* test module.

### enhance
* consider performance.
    + multi-thread situation.
        - pasers
        - ~~walker~~
        - git manager
        - main manager
    + optimize.

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

## API

| 名称   | URL     | 方法   | 备注         |
| ---- | ------- | ---- | ---------- |
| 创建仓库 | /create | POST    | 需要API服务器认证 |
| 更新仓库 | /update | PUT     | 需要API服务器认证 |
| 删除仓库 | /delete | DELETE  | 需要API服务器认证 |

### 更新仓库

请求：

| 路径       | 说明   | 备注      |
| -------- | ---- | ------- |
| reponame | 仓库名称 | 应与用户名一致 |

响应：

| 路径   | 说明   | 备注   |
| ---- | ---- | ---- |
| code | 错误码  |      |

### 创建仓库

请求：

| 路径       | 说明   | 备注      |
| -------- | ---- | ------- |
| reponame | 仓库名称 | 应与用户名一致 |
| url      | 仓库地址 |         |

响应：

| 路径   | 说明   | 备注   |
| ---- | ---- | ---- |
| code | 错误码  |      |

### 删除仓库

请求：

| 路径       | 说明   | 备注      |
| -------- | ---- | ------- |
| reponame | 仓库名称 | 应与用户名一致 |

响应：

| 路径   | 说明   | 备注   |
| ---- | ---- | ---- |
| code | 错误码  |      |