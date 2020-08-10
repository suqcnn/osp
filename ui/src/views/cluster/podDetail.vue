<template>
  <div>
    <clusterbar :titleName="titleName" />
    <div class="dashboard-container">
      <!-- <div class="dashboard-text"></div> -->
      <el-table
        ref="table"
        :data="containers"
        class="table-fix"
        tooltip-effect="dark"
        style="width: 100%"
        v-loading="loading"
        :cell-style="cellStyle"
        :default-sort = "{prop: 'name'}"
        >
        <el-table-column type="expand" width="20" style="overflow:hidden">
          <template slot-scope="props">
            <el-form label-position="left" inline class="table-expand">
              <el-form-item label="容器名称">
                <span>{{ props.row.name }}</span>
              </el-form-item>
              <el-form-item label="状态">
                <span>{{ props.row.status }}</span>
              </el-form-item>
              <el-form-item label="镜像">
                <span>{{ props.row.image }}</span>
              </el-form-item>
              <el-form-item label="启动命令" v-if="props.row.command.length">
                <template v-for="a in props.row.command">
                  <span :key="a">{{a}}<br/></span>
                </template>
              </el-form-item>
              <el-form-item label="启动参数" v-if="props.row.args.length">
                <template v-for="a in props.row.args">
                  <span :key="a">{{a}}<br/></span>
                </template>
              </el-form-item>
              <el-form-item label="端口" v-if="props.row.ports.length">
                <template v-for="a in props.row.ports">
                  <span :key="a">{{a.name ? `${a.name}:` : ''}} {{a.containerPort}}/{{a.protocol}}<br/></span>
                </template>
              </el-form-item>
              <el-form-item label="环境变量" v-if="props.row.env.length">
                <!-- <span>{{ props.row.env }}</span> -->
                <template v-for="a in props.row.env">
                  <span :key="a">
                    {{ envStr(a) }}<br/>
                  </span>
                </template>
              </el-form-item>
              <el-form-item label="目录挂载" v-if="props.row.volume_mounts.length">
                <template v-for="a in props.row.volume_mounts">
                  <span :key="a">{{a.name}} -> {{a.mountPath}} ({{a.readOnly ? "ro" : "rw"}})<br/></span>
                </template>
              </el-form-item>
            </el-form>
          </template>
        </el-table-column>
        <el-table-column
          prop="name"
          label="名称"
          show-overflow-tooltip>
          <template slot-scope="scope">
            <span class="name-class" @click="toogleExpand(scope.row)">
              {{ scope.row.name }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="image"
          label="镜像"
          min-width="150"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="restarts"
          label="重启"
          min-width="30"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="start_time"
          label="开始时间"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          min-width="50"
          show-overflow-tooltip>
        </el-table-column>
        <el-table-column
          label=""
          show-overflow-tooltip
          min-width="20">
          <template slot-scope="scope">
            <!-- <el-link :underline="false"
              @click.native.prevent="deleteRow(scope.$index, tableData)">
              <svg-icon style="width: 1.3em; height: 1.3em;" icon-class="operate" />
            </el-link> -->
            <el-dropdown size="medium" >
              <el-link :underline="false"><svg-icon style="width: 1.3em; height: 1.3em;" icon-class="operate" /></el-link>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native.prevent="sContainer = scope.row.name; log = true">
                  <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px" icon-class="log" /> &nbsp; &nbsp;日志
                </el-dropdown-item>
                <el-dropdown-item @click.native.prevent="sContainer = scope.row.name; terminal = true">
                  <svg-icon style="width: 1.3em; height: 1.3em; line-height: 40px" icon-class="terminal" /> &nbsp; &nbsp;终端
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <el-collapse value="detail">
        <el-collapse-item name="detail">
          <template slot="title">
            <span class="title-class">{{pod.name}}</span>
          </template>
          <el-form label-position="left" inline class="pod-item">
            <el-form-item label="状态">
              <span>{{ pod.status }}</span>
            </el-form-item>
            <el-form-item label="创建时间">
              <span>{{ pod.created }}</span>
            </el-form-item>
            <el-form-item label="命名空间">
              <span>{{ pod.namespace }}</span>
            </el-form-item>
            <el-form-item label="节点">
              <span>{{ pod.node_name }}</span>
            </el-form-item>
            <el-form-item label="服务账户">
              <span>{{ pod.service_account }}</span>
            </el-form-item>
            <el-form-item label="Pod IP">
              <span>{{ pod.ip }}</span>
            </el-form-item>
            <el-form-item label="控制器">
              <span>{{ pod.controlled }}/{{ pod.controlled_name}}</span>
            </el-form-item>
            <el-form-item label="QoS Class">
              <span>{{ pod.qos }}</span>
            </el-form-item>
            <el-form-item label="标签">
              <template v-for="(val, key) in pod.labels">
                <span :key="key">{{key}}: {{val}}<br/></span>
              </template>
            </el-form-item>
            <el-form-item label="注解">
              <span v-if="!pod.annonations">——</span>
              
              <template v-else v-for="(val, key) in pod.annonations">
                <span :key="key">{{key}}: {{val}}<br/></span>
              </template>
            </el-form-item>
          </el-form>
        </el-collapse-item>
        <el-collapse-item title="Volumes" name="volumes">
          <template slot="title">
            <span class="title-class">Volumes</span>
          </template>
          <el-collapse class="volume-class">
            <el-collapse-item :title="v.name" :name="v.name" v-for="v in pod.volumes" :key="v.name">
              <template v-for="(val, key) in v">
                <div v-if="key !== 'name'" :key="key">
                  <div>type: {{key}}</div>
                  <div v-for="(val, key) in val" :key="key">{{key}}: {{val}}</div>
                </div>
              </template>
            </el-collapse-item>
          </el-collapse>
        </el-collapse-item>
        <el-collapse-item title="Conditions" name="conditions">
          <template slot="title">
            <span class="title-class">Conditions</span>
          </template>
        </el-collapse-item>
        <el-collapse-item title="Events" name="events">
          <template slot="title">
            <span class="title-class">Events</span>
          </template>
        </el-collapse-item>
      </el-collapse>

      <el-dialog title="终端" :visible.sync="terminal" :close-on-click-modal="false" width="80%" top="55px">
        <terminal v-if="terminal" :cluster="cluster" :namespace="namespace" :pod="podName" :container="sContainer"></terminal>
      </el-dialog>

      <el-dialog title="日志" :visible.sync="log" :close-on-click-modal="false" width="80%" top="55px">
        <log v-if="log" :cluster="cluster" :namespace="namespace" :pod="podName" :container="sContainer"></log>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import { Clusterbar } from '@/views/components'
import { getPod } from '@/api/pods'
import { Message } from 'element-ui'
import { Terminal } from '@/views/components'
import { Log } from '@/views/components'

export default {
  name: 'PodDetail',
  components: {
    Clusterbar,
    Terminal,
    Log
  },
  data() {
    return {
      log: false,
      terminal: false,
      cellStyle: {border: 0},
      loading: true,
      originPod: undefined,
      sContainer: ''
    }
  },
  created() {
    this.fetchData()
  },
  computed: {
    titleName: function() {
      return ['Pods', this.podName]
    },
    podName: function() {
      return this.$route.params ? this.$route.params.podName : ''
    },
    namespace: function() {
      return this.$route.params ? this.$route.params.namespace : ''
    },
    pod: function() {
      let p = this.buildPods(this.originPod)
      return p
    },
    cluster: function() {
      return this.$store.state.cluster
    },
    containers: function() {
      let c = []
      if (this.pod && this.pod.containers) c = this.pod.containers
      if (this.pod && this.pod.init_containers) c = [...this.pod.init_containers, ...c]
      return c
    }
  },
  methods: {
    fetchData: function() {
      this.originPods = []
      this.loading = true
      const cluster = this.$store.state.cluster
      if (!cluster) {
        Message.error("获取集群参数异常，请刷新重试")
        this.loading = false
        return
      }
      if (!this.namespace) {
        Message.error("获取命名空间参数异常，请刷新重试")
        this.loading = false
        return
      }
      if (!this.podName) {
        Message.error("获取Pod名称参数异常，请刷新重试")
        this.loading = false
        return
      }
      getPod(cluster, this.namespace, this.podName).then(response => {
        this.loading = false
        this.originPod = response.data
      }).catch(() => {
        this.loading = false
      })
    },
    buildPods: function(pod) {
      if (!pod) return {}
      let containers = []
      for (let c of pod.spec.containers) {
        let bc = this.buildContainer(c, pod.status.containerStatuses)
        console.log(bc)
        containers.push(bc)
      }
      let init_containers = []
      if (pod.spec.initContainers) {
        for (let c of pod.spec.initContainers) {
          init_containers.push(this.buildContainer(c, pod.status.initContainerStatuses))
        }
      }
      let controlled
      if (pod.metadata.ownerReferences.length > 0) {
        controlled = pod.metadata.ownerReferences[0]
      }
      let p = {
        uid: pod.metadata.uid,
        name: pod.metadata.name,
        namespace: pod.metadata.namespace,
        containers: containers,
        init_containers: init_containers,
        controlled: controlled ? controlled.kind : '',
        controlled_name: controlled ? controlled.name : '',
        qos: pod.status.qosClass,
        status: pod.status.phase,
        ip: pod.status.podIP,
        created: pod.metadata.creationTimestamp,
        node_name: pod.spec.nodeName,
        resource_version: pod.metadata.resourceVersion,
        labels: pod.metadata.labels,
        annonations: pod.metadata.annotations,
        service_account: pod.spec.serviceAccountName || pod.spec.serviceAccount,
        node_selector: pod.spec.nodeSelector,
        volumes: pod.spec.volumes,
        conditions: pod.status.conditions,
      }
      console.log(p)
      return p
    },
    buildContainer: function(container, statuses) {
      if (!container) return {}
      if (!statuses) return {}
      let c = {
        name: container.name,
        status: 'unknown',
        image: container.image,
        restarts: 0,
        command: container.command ? container.command : [],
        args: container.args ? container.args : [],
        ports: container.ports ? container.ports : [],
        env: container.env ? container.env : [],
        volume_mounts: container.volumeMounts ? container.volumeMounts : [],
        image_pull_policy: container.imagePullPolicy ? container.imagePullPolicy : '',
        resources: container.resources ? container.resources : {},
        start_time: '',
      }
      for (let s of statuses) {
        if (s.name == container.name) {
          c.restarts = s.restartCount
          if (s.state.running) {
            c.status = 'running'
            c.start_time = s.state.running.startedAt
          }
          else if (s.state.terminated) {
            c.status = 'terminated'
            c.start_time = s.state.terminated.startedAt
          }
          else if (s.state.waiting) {
            c.status = 'waiting'
          }
          c.ready = s.ready
          break
        }
      }
      return c
    },
    toogleExpand: function(row) {
      let $table = this.$refs.table;
      $table.toggleRowExpansion(row)
    },
    envStr: function(env) {
      let s = env.name + ': '
      if (env.value) {
        s += env.value
      } else if (env.valueFrom) {
        if (env.valueFrom.configMapKeyRef) {
          s += `configmap(${env.valueFrom.configMapKeyRef.key}:${env.valueFrom.configMapKeyRef.name})`
        } else if (env.valueFrom.fieldRef) {
          s += `fieldRef(${env.valueFrom.fieldRef.apiVersion}:${env.valueFrom.fieldRef.fieldPath})`
        } else if (env.valueFrom.secretKeyRef) {
          s += `secret(${env.valueFrom.secretKeyRef.key}:${env.valueFrom.secretKeyRef.name})`
        } else {
          s += String(env.valueFrom)
        }
      }
      return s
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 10px 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }

  .table-fix {
    height: calc(100% - 100px);
  }
}
.name-class {
  cursor: pointer;
}
.name-class:hover {
  color: #409EFF;
}
</style>

<style>
/* .el-table__expand-icon {
  display: none;
} */
.el-table__expanded-cell[class*=cell] {
  padding-top: 5px;
}
.table-expand {
  font-size: 0;
}
.table-expand label {
  width: 90px;
  color: #99a9bf;
  font-weight: 400;
}
.table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 100%;
}

.pod-item {
  margin: 0px 20px 0px 25px;
  font-size: 0;
}
.pod-item label {
  width: 120px;
  color: #99a9bf;
  font-weight: 400;
}
.pod-item .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
.pod-item span {
  color: #606266;
}
.el-collapse {
  border-top: 0px;
}
.title-class {
  margin-left: 5px;
  color: #606266;
  font-size: 13px;
}
.volume-class {
  margin: 0px 25px;
}
.volume-class .el-collapse-item__arrow {
  display: none;
}
.volume-class .el-collapse-item__header {
  border-bottom: 0px;
}
.volume-class .el-collapse-item__content {
  padding: 0px 10px 15px;
  font-size: 13px;
}
.el-dialog__body {
  padding-top: 5px;
}
</style>
