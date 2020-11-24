(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-0c6b7d9d"],{"43df":function(t,e,n){},"61b2":function(t,e,n){"use strict";n.d(e,"a",(function(){return f})),n.d(e,"c",(function(){return k})),n.d(e,"b",(function(){return D})),n.d(e,"d",(function(){return V}));var o,i=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"cluster-bar"},[n("el-breadcrumb",{staticClass:"app-breadcrumb",attrs:{"separator-class":"el-icon-arrow-right"}},t._l(t.titleName,(function(e){return n("el-breadcrumb-item",{key:e,staticClass:"no-redirect"},[t._v(" "+t._s(e)+" ")])})),1),"undefined"!==typeof t.editFunc?n("el-link",{staticClass:"icon-create",on:{click:function(e){return t.editFunc()}}},[n("svg-icon",{attrs:{"icon-class":"edit"}})],1):t._e(),"undefined"!==typeof t.delFunc?n("el-link",{staticClass:"icon-create",on:{click:function(e){return t.delFunc()}}},[n("svg-icon",{attrs:{"icon-class":"delete"}})],1):t._e(),n("div",{staticClass:"right"},["undefined"!==typeof t.createFunc?n("el-button",{attrs:{size:"small",plain:""},on:{click:function(e){return t.createFunc()}}},[t._v(t._s(t.createDisplay))]):t._e(),"undefined"!==typeof t.nsFunc?n("el-select",{attrs:{multiple:"",placeholder:"命名空间",size:"small"},on:{change:t.nsChange},model:{value:t.nsInput,callback:function(e){t.nsInput=e},expression:"nsInput"}},t._l(t.namespaces,(function(t){return n("el-option",{key:t.name,attrs:{label:t.name,value:t.name}})})),1):t._e(),"undefined"!==typeof t.nameFunc?n("el-input",{attrs:{size:"small",placeholder:"搜索","suffix-icon":"el-icon-search"},on:{input:t.nameDebounce},model:{value:t.nameInput,callback:function(e){t.nameInput=e},expression:"nameInput"}}):t._e()],1)],1)},a=[],s=(n("b0c0"),n("aad4")),r=n("5c96"),c={name:"Clusterbar",props:{titleName:{type:Array,required:!0,default:function(){return[]}},nsFunc:{type:Function,required:!1,default:void 0},nameFunc:{type:Function,required:!1,default:void 0},delFunc:{type:Function,required:!1,default:void 0},editFunc:{type:Function,required:!1,default:void 0},createDisplay:{type:String,required:!1,default:"创建"},createFunc:{type:Function,required:!1,default:void 0}},data:function(){return{nameInput:"",nsInput:[],namespaces:[]}},created:function(){"undefined"!==typeof this.nsFunc&&this.fetchNamespace()},methods:{nsChange:function(t){this.nsFunc&&this.nsFunc(t)},nameDebounce:function(){var t=this;this.nameFunc&&(o&&clearTimeout(o),o=setTimeout((function(){t.nameFunc(t.nameInput),o=void 0}),500))},fetchNamespace:function(){var t=this;this.namespaces=[];var e=this.$store.state.cluster;e?Object(s["b"])(e).then((function(e){t.namespaces=e.data,t.namespaces.sort((function(t,e){return t.name>e.name?1:-1}))})).catch((function(){})):r["Message"].error("获取集群异常，请刷新重试")}}},l=c,u=(n("a6e1"),n("dda3"),n("2877")),d=Object(u["a"])(l,i,a,!1,null,"3a53f646",null),f=d.exports,p=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"xterm",attrs:{id:"xterm"}})},m=[],h=(n("99af"),n("abb2"),n("fcf3")),g=n("47d0"),v=n("173c"),b={name:"Xterm",data:function(){return{socket:null,term:null}},props:{cluster:{type:String,required:!0,default:""},namespace:{type:String,required:!0,default:""},pod:{type:String,required:!0,default:""},container:{type:String,required:!1,default:""}},mounted:function(){this.initTerm()},beforeDestroy:function(){this.socket&&(this.socket.send("\r\nexit\r"),this.socket.close()),this.term&&this.term.dispose()},methods:{initTerm:function(){var t=Math.floor((window.innerHeight-100)/20);console.log(t);var e=new h["Terminal"]({fontSize:14,cursorBlink:!0,rows:t}),n=new g["FitAddon"];e.loadAddon(n),e.open(document.getElementById("xterm")),n.fit(),e.focus(),this.term=e,this.initSocket()},initSocket:function(){var t=this.term.cols,e=this.term.rows;if(this.cluster)if(this.namespace)if(this.pod){var n="http:"==window.location.protocol?"ws":"wss",o="".concat(n,"://").concat(window.location.host,"/ws/exec/").concat(this.cluster,"/").concat(this.namespace,"/").concat(this.pod);this.socket=new WebSocket(o+"?container=".concat(this.container,"&cols=").concat(t,"&rows=").concat(e)),this.socketOnClose(),this.socketOnOpen(),this.socketOnError()}else r["Message"].error("获取POD参数异常，请刷新重试");else r["Message"].error("获取命名空间参数异常，请刷新重试");else r["Message"].error("获取集群参数异常，请刷新重试")},socketOnOpen:function(){var t=this;this.socket.onopen=function(){var e=new v["AttachAddon"](t.socket);t.term.loadAddon(e)}},socketOnClose:function(){this.socket.onclose=function(){}},socketOnError:function(){this.socket.onerror=function(){}}}},y=b,w=Object(u["a"])(y,p,m,!1,null,null,null),k=w.exports,C=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{staticClass:"log-class",style:{height:t.logHeight+"px"},attrs:{id:"logDiv"}},[n("p",{staticStyle:{"white-space":"pre-line"}},[t._v(t._s(t.logs))])])},x=[],_=n("5f87"),O={name:"Logs",data:function(){return{logs:"",socket:null,scrollToBottom:!0}},props:{cluster:{type:String,required:!0,default:""},namespace:{type:String,required:!0,default:""},pod:{type:String,required:!0,default:""},container:{type:String,required:!1,default:""}},computed:{logHeight:function(){return window.innerHeight-200}},mounted:function(){var t=document.getElementById("logDiv"),e=this;t.addEventListener("scroll",(function(){e.scrollToBottom=!1,t.scrollTop+t.clientHeight===t.scrollHeight&&(e.scrollToBottom=!0)}),!0),this.initSocket()},beforeDestroy:function(){this.socket&&this.socket.close()},methods:{initSocket:function(){var t=Object(_["a"])();if(console.log(t),this.cluster)if(this.namespace)if(this.pod){var e="http:"==window.location.protocol?"ws":"wss",n="".concat(e,"://").concat(window.location.host,"/ws/log/").concat(this.cluster,"/").concat(this.namespace,"/").concat(this.pod);this.socket=new WebSocket(n+"?container=".concat(this.container,"&token=").concat(t)),this.socketOnClose(),this.socketOnOpen(),this.socketOnError(),this.socketOnMessage()}else r["Message"].error("获取POD参数异常，请刷新重试");else r["Message"].error("获取命名空间参数异常，请刷新重试");else r["Message"].error("获取集群参数异常，请刷新重试")},socketOnOpen:function(){this.socket.onopen=function(){}},socketOnClose:function(){this.socket.onclose=function(){}},socketOnError:function(){this.socket.onerror=function(){}},socketOnMessage:function(){var t=this;this.socket.onmessage=function(e){t.logs+=e.data;var n=t;t.$nextTick((function(){if(n.scrollToBottom){var t=document.getElementById("logDiv");t.scrollTop=t.scrollHeight}}))}}}},S=O,F=(n("ca6d"),Object(u["a"])(S,C,x,!1,null,"19556679",null)),D=F.exports,E=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],staticClass:"yaml-editor",style:"--yamlHeight: "+t.yamlHeight+"px"},[n("textarea",{ref:"textarea"})])},T=[],H=n("56b3"),q=n.n(H);n("0dd0"),n("a7be"),n("cc10"),n("ced0"),n("8822"),n("b8d1");window.jsyaml=n("651e");var M={name:"YamlEditor",props:["value","loading","updateValue"],data:function(){return{yamlEditor:!1}},computed:{yamlHeight:function(){return window.innerHeight-250}},watch:{value:function(t){var e=this.yamlEditor.getValue();t!==e&&this.yamlEditor.setValue(this.value)}},mounted:function(){var t=this;this.yamlEditor=q.a.fromTextArea(this.$refs.textarea,{lineNumbers:!0,mode:"text/x-yaml",gutters:["CodeMirror-lint-markers"],theme:"base16-light",lint:!0,lineWrapping:!0}),this.yamlEditor.setValue(this.value),this.yamlEditor.on("change",(function(e){t.$emit("input",e.getValue())}))},methods:{getValue:function(){return this.yamlEditor.getValue()}}},j=M,N=(n("db62"),Object(u["a"])(j,E,T,!1,null,"5bb854da",null)),V=N.exports},"64d3":function(t,e,n){},"753c":function(t,e,n){"use strict";n.r(e);var o=function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",[n("clusterbar",{attrs:{titleName:t.titleName,nameFunc:t.nameSearch,createFunc:t.createClusterDialog,createDisplay:"创建集群"}}),n("div",{ref:"tableCot",staticClass:"dashboard-container"},[n("el-table",{directives:[{name:"loading",rawName:"v-loading",value:t.loading,expression:"loading"}],staticClass:"table-fix",staticStyle:{width:"100%"},attrs:{data:t.clusters,"tooltip-effect":"dark","max-height":t.maxHeight,"cell-style":t.cellStyle,"default-sort":{prop:"name"},"row-key":"name"}},[n("el-table-column",{attrs:{prop:"name",label:"名称","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{prop:"create_time",label:"创建时间","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{prop:"status",label:"状态","min-width":"34%","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{label:"",width:"80"},scopedSlots:t._u([{key:"default",fn:function(e){return[n("el-dropdown",{attrs:{size:"medium"}},[n("el-link",{attrs:{underline:!1}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em"},attrs:{"icon-class":"operate"}})],1),n("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},["Pending"===e.row.status?n("el-dropdown-item",{nativeOn:{click:function(n){n.preventDefault(),t.clusterConnectToken=e.row.token,t.clusterConnectDialog=!0}}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em","line-height":"40px","vertical-align":"-0.25em"},attrs:{"icon-class":"link"}}),n("span",{staticStyle:{"margin-left":"5px"}},[t._v("连接")])],1):t._e(),n("el-dropdown-item",{nativeOn:{click:function(n){return n.preventDefault(),t.deleteClusters([{name:e.row.name}])}}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em","line-height":"40px","vertical-align":"-0.25em"},attrs:{"icon-class":"delete"}}),n("span",{staticStyle:{"margin-left":"5px"}},[t._v("删除")])],1)],1)],1)]}}])})],1)],1),n("div",[n("el-dialog",{attrs:{title:"创建集群",visible:t.createClusterFormVisible,"close-on-click-modal":!1},on:{"update:visible":function(e){t.createClusterFormVisible=e}}},[n("el-form",{attrs:{model:t.form}},[n("el-form-item",{attrs:{label:"集群名称"}},[n("el-input",{attrs:{autocomplete:"off"},model:{value:t.form.name,callback:function(e){t.$set(t.form,"name",e)},expression:"form.name"}})],1)],1),n("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[n("el-button",{on:{click:function(e){t.createClusterFormVisible=!1}}},[t._v("取 消")]),n("el-button",{attrs:{type:"primary"},on:{click:t.handleCreateCluster}},[t._v("确 定")])],1)],1)],1),n("div",[n("el-dialog",{attrs:{title:"集群导入",visible:t.clusterConnectDialog,"close-on-click-modal":!1},on:{"update:visible":function(e){t.clusterConnectDialog=e}}},[n("div",{staticStyle:{"font-size":"15px"}},[t._v("请在现有Kubernetes集群上运行下面的kubeclt命令，以连接OpenSpace平台：")]),n("div",{staticStyle:{"margin-top":"15px"}},[n("el-tag",{staticStyle:{"font-size":"14px","border-radius":"4px 0px 0px 4px","border-right-width":"0px"},attrs:{type:"info"}},[t._v(" "+t._s(t.copyCluster)+" ")]),n("el-button",{directives:[{name:"clipboard",rawName:"v-clipboard:copy",value:t.copyCluster,expression:"copyCluster",arg:"copy"},{name:"clipboard",rawName:"v-clipboard:success",value:t.onCopy,expression:"onCopy",arg:"success"},{name:"clipboard",rawName:"v-clipboard:error",value:t.onError,expression:"onError",arg:"error"}],staticStyle:{height:"32px","border-radius":"0px 4px 4px 0px",padding:"10px 15px"},attrs:{slot:"append",plain:"",size:"small"},slot:"append"},[t._v(" 复制 ")])],1),n("div",{staticStyle:{"font-size":"13px","margin-top":"8px",color:"#e6a23c"}},[t._v(" *注意：请将上述访问地址"+t._s(this.locationAddr)+"换为Kubernetes集群可以访问的地址。 ")]),n("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[n("el-button",{attrs:{type:"primary"},on:{click:function(e){t.clusterConnectDialog=!1}}},[t._v("确 定")])],1)])],1)],1)},i=[],a=(n("99af"),n("b0c0"),n("61b2")),s=n("7ea2"),r=n("5c96"),c={name:"SettingsCluster",components:{Clusterbar:a["a"]},created:function(){this.fetchData()},mounted:function(){var t=this;window.onresize=function(){return function(){var e=window.innerHeight-150;console.log(e),t.maxHeight=e}()}},data:function(){return{titleName:["Cluster"],search_name:"",cellStyle:{border:0},maxHeight:window.innerHeight-150,loading:!0,clusters:[],createClusterFormVisible:!1,clusterConnectDialog:!1,clusterConnectToken:"",form:{name:""},locationAddr:window.location.origin}},computed:{copyCluster:function(){return"kubectl apply -f ".concat(this.locationAddr,"/v1/import/").concat(this.clusterConnectToken)}},methods:{fetchData:function(){var t=this;this.loading=!0,Object(s["d"])().then((function(e){t.loading=!1,t.clusters=e.data})).catch((function(){t.loading=!1}))},nameSearch:function(t){this.search_name=t},createClusterDialog:function(){this.createClusterFormVisible=!0},handleCreateCluster:function(){var t=this;console.log(this.form.name),this.form.name?Object(s["b"])(this.form).then((function(e){r["Message"].success("集群添加成功"),t.createClusterFormVisible=!1,t.loading=!1,t.fetchData(),t.clusterConnectToken=e.data.token,t.clusterConnectDialog=!0})).catch((function(){t.loading=!1})):r["Message"].error("集群名称不能为空！")},deleteClusters:function(t){var e=this;t.length<=0?r["Message"].error("请选择要删除的集群"):Object(s["c"])(t).then((function(t){e.fetchData()})).catch((function(t){console.log(t)}))},onCopy:function(t){r["Message"].success("复制成功")},onError:function(t){}}},l=c,u=(n("77f3"),n("2877")),d=Object(u["a"])(l,o,i,!1,null,"213aa09e",null);e["default"]=d.exports},"77f3":function(t,e,n){"use strict";var o=n("b1e0"),i=n.n(o);i.a},a6e1:function(t,e,n){"use strict";var o=n("ab7f"),i=n.n(o);i.a},aad4:function(t,e,n){"use strict";n.d(e,"b",(function(){return i})),n.d(e,"a",(function(){return a}));n("99af");var o=n("b775");function i(t){return Object(o["a"])({url:"namespace/".concat(t),method:"get"})}function a(t,e,n){return Object(o["a"])({url:"namespace/".concat(t,"/").concat(e),method:"get",params:{output:n}})}},ab7f:function(t,e,n){},b1e0:function(t,e,n){},b92f:function(t,e,n){},ca6d:function(t,e,n){"use strict";var o=n("64d3"),i=n.n(o);i.a},db62:function(t,e,n){"use strict";var o=n("43df"),i=n.n(o);i.a},dda3:function(t,e,n){"use strict";var o=n("b92f"),i=n.n(o);i.a}}]);