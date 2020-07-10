agent_yaml = """
---

apiVersion: v1
kind: Namespace
metadata:
  name: osp

---

apiVersion: v1
kind: ServiceAccount
metadata:
  name: osp-admin
  namespace: osp

---

kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: osp-clusterrole-bind
  namespace: osp
subjects:
- kind: ServiceAccount
  name: osp-admin
  namespace: osp
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: ospagent
  namespace: osp
  labels:
    app: ospagent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ospagent
  template:
    metadata:
      labels:
        app: ospagent
    spec:
      containers:
      - name: ospagent
        image: alyf/ospagent:latest
        ports:
        - containerPort: 80
        command:
        - "/ospagent"
        args:
        - --token=${token}
        - --server-url=101.251.205.250
      serviceAccountName: osp-admin
      imagePullSecrets:
      - name: regcred
"""