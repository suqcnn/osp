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
    "status": "Running"
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



