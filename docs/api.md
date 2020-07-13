### User

#### 1. Create a user

Create a user

##### HTTP request

```
POST /osp/api/users HTTP/1.1
Authorization: Bearer $TOKEN
Accept: applicaton/json
```

##### Body

| Parameter | Required | Type   | Description                   |
| --------- | -------- | ------ | ----------------------------- |
| name      | true     | string | name of the user to login     |
| email     | true     | string | email of the user             |
| password  | true     | string | password of the user to login |

##### Responses

| Field | Type   | Description   |
| ----- | ------ | ------------- |
| code  | string | error code    |
| msg   | string | error message |



#### 2. List all users

List all users

##### HTTP request

```
GET /osp/api/users HTTP/1.1
Authorization: Bearer $TOKEN
Accept: applicaton/json
```

##### Query parameters

| Parameter | Required | Type   | Description      |
| --------- | -------- | ------ | ---------------- |
| name      | false    | string | name of the user |

##### Responses

| Field       | Type       | Description       |
| ----------- | ---------- | ----------------- |
| code        | string     | error code        |
| msg         | string     | error message     |
| data        | list[dict] | list users        |
| name        | string     | name of the user  |
| email       | string     | email of the user |
| create_time | datetime   | create time       |
| update_time | datetime   | update time       |

example:

```json
{
  "code": "Success",
  "msg": "Success",
  "data": [{
    "name": "test",
    "email": "test@abc.com",
    "create_time": "2020-07-12 08:24:10",
    "update_time": "2020-07-12 08:24:10"
  }]
}
```



#### 3. Update a user

Update a user

##### HTTP request

```
PUT /osp/api/users/$NAME HTTP/1.1
Authorization: Bearer $TOKEN
Accept: applicaton/json
```

##### Body

| Parameter | Required | Type   | Description                   |
| --------- | -------- | ------ | ----------------------------- |
| email     | false    | string | email of the user             |
| password  | false    | string | password of the user to login |

##### Responses

| Field | Type   | Description   |
| ----- | ------ | ------------- |
| code  | string | error code    |
| msg   | string | error message |



#### 4. Login

Login with a user

##### HTTP request

```
POST /osp/api/login HTTP/1.1
Accept: applicaton/json
```

##### Body

| Parameter | Required | Type   | Description                   |
| --------- | -------- | ------ | ----------------------------- |
| name      | true     | string | name of the user to login     |
| password  | true     | string | password of the user to login |

##### Responses

| Field | Type   | Description                                         |
| ----- | ------ | --------------------------------------------------- |
| code  | string | error code                                          |
| msg   | string | error message                                       |
| data  | dict   | response data                                       |
| token | string | authenticate token of the user, expired after 30min |

example:

```json
{
  "code": "Success",
  "msg": "Success",
  "data": {
    "token": ""
  }
}
```



### Pods

#### 1. List all pods

List all pods with simple information

##### HTTP request

```
GET /osp/api/pods/$CLUSTER HTTP/1.1
Authorization: Bearer $TOKEN
Accept: applicaton/json
```

##### Path parameters

| Parameter | Type   | Description         |
| --------- | ------ | ------------------- |
| cluster   | string | name of the cluster |

##### Query parameters

| Parameter | Required | Type   | Description               |
| --------- | -------- | ------ | ------------------------- |
| namespace | false    | string | name of the pod namespace |
| name      | false    | string | name of the pod           |

##### Responses

| Field              | Type       | Description                 |
| ------------------ | ---------- | --------------------------- |
| code               | string     | error code                  |
| msg                | string     | error message               |
| data               | list[dict] | list pods                   |
| name               | string     | name of the pod             |
| namespace          | string     | namespace of the pod        |
| containers         | list[dict] | containers of the pod       |
| init_conatiners    | list[dict] | init containers of the pod  |
| containers[name]   | string     | name of the container       |
| containers[status] | string     | status of the container     |
| restarts           | int        | restart numbers of the pod  |
| controlled         | string     | pod controlled by           |
| qos                | string     | qos of the pod              |
| created            | string     | created datetime of the pod |
| status             | string     | status of the pod           |

example:

```json
{
  "code": "Success",
  "msg": "Success",
  "data": [{
    "name": "test",
    "namespace": "default",
    "containers": [{
      "name": "test",
      "status": "running",
    	"restarts": 0
    }],
    "init_containers": [],
    "controlled": "ReplicaSet",
    "qos": "BestEffort",
    "created": "2020-07-09T10:10:53Z",
    "status": "Running",
    "node_name": "woker001"
  }]
}
```



#### 2. Get a pod

Get a pod with detail information

##### HTTP request

```
GET /osp/api/pods/$CLUSTER/$NAMESPACE/$NAME HTTP/1.1
Authorization: Bearer $TOKEN
Accept: applicaton/json
```

##### Path parameters

| Parameter | Type   | Description               |
| --------- | ------ | ------------------------- |
| cluster   | string | name of the cluster       |
| namespace | string | name of the pod namespace |
| name      | string | name of the pod           |

##### Query parameters

| Parameter | Required | Type   | Description                                   |
| --------- | -------- | ------ | --------------------------------------------- |
| output    | false    | string | output type of the pod, default json, or yaml |

##### Responses

| Field  | Type   | Description                                                  |
| ------ | ------ | ------------------------------------------------------------ |
| code   | string | error code                                                   |
| msg    | string | error message                                                |
| data   | dict   | list pods                                                    |
| v1.Pod | object | object of the pod<br />https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#pod-v1-core |

example:

```json
{
  "code": "Success",
  "msg": "Success",
  "data": {
  }
}
```



