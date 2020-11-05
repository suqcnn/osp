(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-b32af870"],{"147d":function(e,t,n){"use strict";var o=n("f6bf"),a=n.n(o);a.a},"43df":function(e,t,n){},"4a49":function(e,t,n){},"589b":function(e,t,n){"use strict";var o=n("714a"),a=n.n(o);a.a},"61b2":function(e,t,n){"use strict";n.d(t,"a",(function(){return m})),n.d(t,"c",(function(){return k})),n.d(t,"b",(function(){return J})),n.d(t,"d",(function(){return H}));var o,a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"cluster-bar"},[n("el-breadcrumb",{staticClass:"app-breadcrumb",attrs:{"separator-class":"el-icon-arrow-right"}},e._l(e.titleName,(function(t){return n("el-breadcrumb-item",{key:t,staticClass:"no-redirect"},[e._v(" "+e._s(t)+" ")])})),1),"undefined"!==typeof e.editFunc?n("el-link",{staticClass:"icon-create",on:{click:function(t){return e.editFunc()}}},[n("svg-icon",{attrs:{"icon-class":"edit"}})],1):e._e(),"undefined"!==typeof e.delFunc?n("el-link",{staticClass:"icon-create",on:{click:function(t){return e.delFunc()}}},[n("svg-icon",{attrs:{"icon-class":"delete"}})],1):e._e(),n("div",{staticClass:"right"},["undefined"!==typeof e.nsFunc?n("el-select",{attrs:{multiple:"",placeholder:"命名空间",size:"small"},on:{change:e.nsChange},model:{value:e.nsInput,callback:function(t){e.nsInput=t},expression:"nsInput"}},e._l(e.namespaces,(function(e){return n("el-option",{key:e.name,attrs:{label:e.name,value:e.name}})})),1):e._e(),"undefined"!==typeof e.nameFunc?n("el-input",{attrs:{size:"small",placeholder:"搜索","suffix-icon":"el-icon-search"},on:{input:e.nameDebounce},model:{value:e.nameInput,callback:function(t){e.nameInput=t},expression:"nameInput"}}):e._e()],1)],1)},i=[],s=(n("b0c0"),n("aad4")),r=n("5c96"),c={name:"Clusterbar",props:{titleName:{type:Array,required:!0,default:function(){return[]}},nsFunc:{type:Function,required:!1,default:void 0},nameFunc:{type:Function,required:!1,default:void 0},delFunc:{type:Function,required:!1,default:void 0},editFunc:{type:Function,required:!1,default:void 0}},data:function(){return{nameInput:"",nsInput:[],namespaces:[]}},created:function(){"undefined"!==typeof this.nsFunc&&this.fetchNamespace()},methods:{nsChange:function(e){this.nsFunc&&this.nsFunc(e)},nameDebounce:function(){var e=this;this.nameFunc&&(o&&clearTimeout(o),o=setTimeout((function(){e.nameFunc(e.nameInput),o=void 0}),500))},fetchNamespace:function(){var e=this;this.namespaces=[];var t=this.$store.state.cluster;t?Object(s["b"])(t).then((function(t){e.namespaces=t.data,e.namespaces.sort((function(e,t){return e.name>t.name?1:-1}))})).catch((function(){})):r["Message"].error("获取集群异常，请刷新重试")}}},l=c,u=(n("589b"),n("dda3"),n("2877")),d=Object(u["a"])(l,a,i,!1,null,"3d7b3a75",null),m=d.exports,h=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"xterm",attrs:{id:"xterm"}})},f=[],p=(n("99af"),n("abb2"),n("fcf3")),b=n("47d0"),g=n("173c"),v={name:"Xterm",data:function(){return{socket:null,term:null}},props:{cluster:{type:String,required:!0,default:""},namespace:{type:String,required:!0,default:""},pod:{type:String,required:!0,default:""},container:{type:String,required:!1,default:""}},mounted:function(){this.initTerm()},beforeDestroy:function(){this.socket&&(this.socket.send("\r\nexit\r"),this.socket.close()),this.term&&this.term.dispose()},methods:{initTerm:function(){var e=Math.floor((window.innerHeight-100)/20);console.log(e);var t=new p["Terminal"]({fontSize:14,cursorBlink:!0,rows:e}),n=new b["FitAddon"];t.loadAddon(n),t.open(document.getElementById("xterm")),n.fit(),t.focus(),this.term=t,this.initSocket()},initSocket:function(){var e=this.term.cols,t=this.term.rows;if(this.cluster)if(this.namespace)if(this.pod){var n="ws://".concat(window.location.host,"/api/v1/exec/").concat(this.cluster,"/").concat(this.namespace,"/").concat(this.pod);this.socket=new WebSocket(n+"?container=".concat(this.container,"&cols=").concat(e,"&rows=").concat(t)),this.socketOnClose(),this.socketOnOpen(),this.socketOnError()}else r["Message"].error("获取POD参数异常，请刷新重试");else r["Message"].error("获取命名空间参数异常，请刷新重试");else r["Message"].error("获取集群参数异常，请刷新重试")},socketOnOpen:function(){var e=this;this.socket.onopen=function(){var t=new g["AttachAddon"](e.socket);e.term.loadAddon(t)}},socketOnClose:function(){this.socket.onclose=function(){}},socketOnError:function(){this.socket.onerror=function(){}}}},y=v,w=Object(u["a"])(y,h,f,!1,null,null,null),k=w.exports,C=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"log-class",style:{height:e.logHeight+"px"},attrs:{id:"logDiv"}},[n("p",{staticStyle:{"white-space":"pre-line"}},[e._v(e._s(e.logs))])])},_=[],O=n("5f87"),S={name:"Logs",data:function(){return{logs:"",socket:null,scrollToBottom:!0}},props:{cluster:{type:String,required:!0,default:""},namespace:{type:String,required:!0,default:""},pod:{type:String,required:!0,default:""},container:{type:String,required:!1,default:""}},computed:{logHeight:function(){return window.innerHeight-200}},mounted:function(){var e=document.getElementById("logDiv"),t=this;e.addEventListener("scroll",(function(){t.scrollToBottom=!1,e.scrollTop+e.clientHeight===e.scrollHeight&&(t.scrollToBottom=!0)}),!0),this.initSocket()},beforeDestroy:function(){this.socket&&this.socket.close()},methods:{initSocket:function(){var e=Object(O["a"])();if(console.log(e),this.cluster)if(this.namespace)if(this.pod){var t="ws://".concat(window.location.host,"/osp/api/log/").concat(this.cluster,"/").concat(this.namespace,"/").concat(this.pod);this.socket=new WebSocket(t+"?container=".concat(this.container,"&token=").concat(e)),this.socketOnClose(),this.socketOnOpen(),this.socketOnError(),this.socketOnMessage()}else r["Message"].error("获取POD参数异常，请刷新重试");else r["Message"].error("获取命名空间参数异常，请刷新重试");else r["Message"].error("获取集群参数异常，请刷新重试")},socketOnOpen:function(){this.socket.onopen=function(){}},socketOnClose:function(){this.socket.onclose=function(){}},socketOnError:function(){this.socket.onerror=function(){}},socketOnMessage:function(){var e=this;this.socket.onmessage=function(t){e.logs+=t.data;var n=e;e.$nextTick((function(){if(n.scrollToBottom){var e=document.getElementById("logDiv");e.scrollTop=e.scrollHeight}}))}}}},x=S,j=(n("147d"),Object(u["a"])(x,C,_,!1,null,"72e53532",null)),J=j.exports,F=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],staticClass:"yaml-editor",style:"--yamlHeight: "+e.yamlHeight+"px"},[n("textarea",{ref:"textarea"})])},D=[],E=n("56b3"),M=n.n(E);n("0dd0"),n("a7be"),n("cc10"),n("ced0"),n("8822"),n("b8d1");window.jsyaml=n("651e");var N={name:"YamlEditor",props:["value","loading","updateValue"],data:function(){return{yamlEditor:!1}},computed:{yamlHeight:function(){return window.innerHeight-250}},watch:{value:function(e){var t=this.yamlEditor.getValue();e!==t&&this.yamlEditor.setValue(this.value)}},mounted:function(){var e=this;this.yamlEditor=M.a.fromTextArea(this.$refs.textarea,{lineNumbers:!0,mode:"text/x-yaml",gutters:["CodeMirror-lint-markers"],theme:"base16-light",lint:!0,lineWrapping:!0}),this.yamlEditor.setValue(this.value),this.yamlEditor.on("change",(function(t){e.$emit("input",t.getValue())}))},methods:{getValue:function(){return this.yamlEditor.getValue()}}},T=N,V=(n("db62"),Object(u["a"])(T,F,D,!1,null,"5bb854da",null)),H=V.exports},"714a":function(e,t,n){},8215:function(e,t,n){"use strict";var o=n("df86"),a=n.n(o);a.a},8372:function(e,t,n){"use strict";n.r(t);var o=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("clusterbar",{attrs:{titleName:e.titleName,nsFunc:e.nsSearch,nameFunc:e.nameSearch,delFunc:e.delFunc}}),n("div",{staticClass:"dashboard-container"},[n("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],ref:"multipleTable",staticClass:"table-fix",staticStyle:{width:"100%"},attrs:{data:e.cronjobs,"tooltip-effect":"dark","max-height":e.maxHeight,"cell-style":e.cellStyle,"default-sort":{prop:"name"},"row-key":"uid"},on:{"selection-change":e.handleSelectionChange}},[n("el-table-column",{attrs:{type:"selection",width:"45"}}),n("el-table-column",{attrs:{prop:"name",label:"名称","min-width":"45","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(t){return[n("span",{staticClass:"name-class",on:{click:function(n){return e.nameClick(t.row.namespace,t.row.name)}}},[e._v(" "+e._s(t.row.name)+" ")])]}}])}),n("el-table-column",{attrs:{prop:"namespace",label:"命名空间","min-width":"40","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{prop:"schedule",label:"定时","min-width":"40","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{prop:"suspend",label:"挂起","min-width":"40","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{prop:"concurrency_policy",label:"并发策略","min-width":"35","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{prop:"last_schedule_time",label:"上一次执行","min-width":"50","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{prop:"created",label:"创建时间","min-width":"50","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{label:"","show-overflow-tooltip":"",width:"45"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("el-dropdown",{attrs:{size:"medium"}},[n("el-link",{attrs:{underline:!1}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em"},attrs:{"icon-class":"operate"}})],1),n("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[n("el-dropdown-item",{nativeOn:{click:function(n){return n.preventDefault(),e.nameClick(t.row.namespace,t.row.name)}}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em","line-height":"40px","vertical-align":"-0.25em"},attrs:{"icon-class":"detail"}}),n("span",{staticStyle:{"margin-left":"5px"}},[e._v("详情")])],1),n("el-dropdown-item",{nativeOn:{click:function(n){return n.preventDefault(),e.getCronJobYaml(t.row.namespace,t.row.name)}}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em","line-height":"40px","vertical-align":"-0.25em"},attrs:{"icon-class":"edit"}}),n("span",{staticStyle:{"margin-left":"5px"}},[e._v("修改")])],1),n("el-dropdown-item",{nativeOn:{click:function(n){return n.preventDefault(),e.deleteCronJobs([{namespace:t.row.namespace,name:t.row.name}])}}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em","line-height":"40px","vertical-align":"-0.25em"},attrs:{"icon-class":"delete"}}),n("span",{staticStyle:{"margin-left":"5px"}},[e._v("删除")])],1)],1)],1)]}}])})],1)],1),n("el-dialog",{attrs:{title:"编辑",visible:e.yamlDialog,"close-on-click-modal":!1,width:"60%",top:"55px"},on:{"update:visible":function(t){e.yamlDialog=t}}},[e.yamlDialog?n("yaml",{attrs:{loading:e.yamlLoading},model:{value:e.yamlValue,callback:function(t){e.yamlValue=t},expression:"yamlValue"}}):e._e(),n("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[n("el-button",{attrs:{plain:"",size:"small"},on:{click:function(t){e.yamlDialog=!1}}},[e._v("取 消")]),n("el-button",{attrs:{plain:"",size:"small"},on:{click:function(t){return e.updateCronJob()}}},[e._v("确 定")])],1)],1)],1)},a=[],i=(n("4de4"),n("caad"),n("c975"),n("b0c0"),n("2532"),n("b85c")),s=n("61b2"),r=n("994f"),c=n("5c96"),l={name:"CronJob",components:{Clusterbar:s["a"],Yaml:s["d"]},data:function(){return{yamlDialog:!1,yamlNamespace:"",yamlName:"",yamlValue:"",yamlLoading:!0,cellStyle:{border:0},titleName:["CronJobs"],maxHeight:window.innerHeight-150,loading:!0,originCronJobs:[],search_ns:[],search_name:"",delFunc:void 0,delCronJobs:[]}},created:function(){this.fetchData()},mounted:function(){var e=this;window.onresize=function(){return function(){var t=window.innerHeight-150;e.maxHeight=t}()}},watch:{cronjobsWatch:function(e){if(e){var t=e.resource.metadata.uid,n=e.resource.metadata.resourceVersion;if("add"===e.event)this.originCronJobs.push(this.buildCronJobs(e.resource));else if("update"===e.event)for(var o in this.originCronJobs){var a=this.originCronJobs[o];if(a.uid===t){if(a.resource_version<n){var i=this.buildCronJobs(e.resource);this.$set(this.originCronJobs,o,i)}break}}else"delete"===e.event&&(this.originCronJobs=this.originCronJobs.filter((function(e){var n=e.uid;return n!==t})))}}},computed:{cronjobs:function(){var e,t=[],n=Object(i["a"])(this.originCronJobs);try{for(n.s();!(e=n.n()).done;){var o=e.value;this.search_ns.length>0&&this.search_ns.indexOf(o.namespace)<0||(this.search_name&&!o.name.includes(this.search_name)||(o.conditions&&o.conditions.length>0?o.conditions.sort():o.conditions=[],t.push(o)))}}catch(a){n.e(a)}finally{n.f()}return t},cronjobsWatch:function(){return this.$store.getters["ws/cronjobsWatch"]}},methods:{fetchData:function(){var e=this;this.loading=!0,this.originCronJobs=[];var t=this.$store.state.cluster;t?Object(r["c"])(t).then((function(t){e.loading=!1,e.originCronJobs=t.data})).catch((function(){e.loading=!1})):(this.loading=!1,c["Message"].error("获取集群异常，请刷新重试"))},nsSearch:function(e){this.search_ns=[];var t,n=Object(i["a"])(e);try{for(n.s();!(t=n.n()).done;){var o=t.value;this.search_ns.push(o)}}catch(a){n.e(a)}finally{n.f()}},nameSearch:function(e){this.search_name=e},buildCronJobs:function(e){if(e){var t=[];if(e.status.conditions){var n,o=Object(i["a"])(e.status.conditions);try{for(o.s();!(n=o.n()).done;){var a=n.value;"True"===a.status&&t.push(a.type)}}catch(r){o.e(r)}finally{o.f()}}var s={uid:e.metadata.uid,namespace:e.metadata.namespace,name:e.metadata.name,active:e.status.active,last_schedule_time:e.status.lastScheduleTime,schedule:e.spec.schedule,resource_version:e.metadata.resourceVersion,concurrency_policy:e.Spec.concurrencyPolicy,suspend:e.spec.suspend,created:e.metadata.creationTimestamp};return s}},nameClick:function(e,t){this.$router.push({name:"cronjobDetail",params:{namespace:e,cronjobName:t}})},getCronJobYaml:function(e,t){var n=this;this.yamlNamespace="",this.yamlName="";var o=this.$store.state.cluster;o?e?t?(this.yamlValue="",this.yamlDialog=!0,this.yamlLoading=!0,Object(r["b"])(o,e,t,"yaml").then((function(o){n.yamlLoading=!1,n.yamlValue=o.data,n.yamlNamespace=e,n.yamlName=t})).catch((function(){n.yamlLoading=!1}))):c["Message"].error("获取Deployment名称参数异常，请刷新重试"):c["Message"].error("获取命名空间参数异常，请刷新重试"):c["Message"].error("获取集群参数异常，请刷新重试")},deleteCronJobs:function(e){var t=this.$store.state.cluster;if(t)if(e.length<=0)c["Message"].error("请选择要删除的CronJobs");else{var n={resources:e};Object(r["a"])(t,n).then((function(){c["Message"].success("删除成功")})).catch((function(){}))}else c["Message"].error("获取集群参数异常，请刷新重试")},updateCronJob:function(){var e=this.$store.state.cluster;e?this.yamlNamespace?this.yamlName?(console.log(this.yamlValue),Object(r["d"])(e,this.yamlNamespace,this.yamlName,this.yamlValue).then((function(){c["Message"].success("更新成功")})).catch((function(){}))):c["Message"].error("获取CronJob参数异常，请刷新重试"):c["Message"].error("获取命名空间参数异常，请刷新重试"):c["Message"].error("获取集群参数异常，请刷新重试")},_delCronJobsFunc:function(){if(this.delCronJobs.length>0){var e,t=[],n=Object(i["a"])(this.delCronJobs);try{for(n.s();!(e=n.n()).done;){var o=e.value;t.push({namespace:o.namespace,name:o.name})}}catch(a){n.e(a)}finally{n.f()}this.deleteCronJobs(t)}},handleSelectionChange:function(e){this.delCronJobs=e,e.length>0?this.delFunc=this._delCronJobsFunc:this.delFunc=void 0}}},u=l,d=(n("cd10"),n("8215"),n("2877")),m=Object(d["a"])(u,o,a,!1,null,"792a0ff5",null);t["default"]=m.exports},"994f":function(e,t,n){"use strict";n.d(t,"c",(function(){return a})),n.d(t,"b",(function(){return i})),n.d(t,"a",(function(){return s})),n.d(t,"d",(function(){return r}));n("99af");var o=n("b775");function a(e){return Object(o["a"])({url:"cronjob/".concat(e),method:"get"})}function i(e,t,n){var a=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"";return Object(o["a"])({url:"cronjob/".concat(e,"/").concat(t,"/").concat(n),method:"get",params:{output:a}})}function s(e,t){return Object(o["a"])({url:"cronjob/".concat(e,"/delete"),method:"post",data:t})}function r(e,t,n,a){return Object(o["a"])({url:"cronjob/".concat(e,"/").concat(t,"/").concat(n),method:"post",data:{yaml:a}})}},aad4:function(e,t,n){"use strict";n.d(t,"b",(function(){return a})),n.d(t,"a",(function(){return i}));n("99af");var o=n("b775");function a(e){return Object(o["a"])({url:"namespace/".concat(e),method:"get"})}function i(e,t,n){return Object(o["a"])({url:"namespace/".concat(e,"/").concat(t),method:"get",params:{output:n}})}},b85c:function(e,t,n){"use strict";n.d(t,"a",(function(){return a}));n("a4d3"),n("e01a"),n("d28b"),n("d3b7"),n("3ca3"),n("ddb0");var o=n("06c5");function a(e,t){var n;if("undefined"===typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(n=Object(o["a"])(e))||t&&e&&"number"===typeof e.length){n&&(e=n);var a=0,i=function(){};return{s:i,n:function(){return a>=e.length?{done:!0}:{done:!1,value:e[a++]}},e:function(e){throw e},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var s,r=!0,c=!1;return{s:function(){n=e[Symbol.iterator]()},n:function(){var e=n.next();return r=e.done,e},e:function(e){c=!0,s=e},f:function(){try{r||null==n["return"]||n["return"]()}finally{if(c)throw s}}}}},b92f:function(e,t,n){},cd10:function(e,t,n){"use strict";var o=n("4a49"),a=n.n(o);a.a},db62:function(e,t,n){"use strict";var o=n("43df"),a=n.n(o);a.a},dda3:function(e,t,n){"use strict";var o=n("b92f"),a=n.n(o);a.a},df86:function(e,t,n){},f6bf:function(e,t,n){}}]);