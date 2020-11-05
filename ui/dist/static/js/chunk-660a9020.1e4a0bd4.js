(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-660a9020"],{"147d":function(e,t,n){"use strict";var a=n("f6bf"),s=n.n(a);s.a},"1b0e":function(e,t,n){"use strict";var a=n("b76c"),s=n.n(a);s.a},"43df":function(e,t,n){},"4b16":function(e,t,n){},"589b":function(e,t,n){"use strict";var a=n("714a"),s=n.n(a);s.a},"61b2":function(e,t,n){"use strict";n.d(t,"a",(function(){return m})),n.d(t,"c",(function(){return k})),n.d(t,"b",(function(){return F})),n.d(t,"d",(function(){return T}));var a,s=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"cluster-bar"},[n("el-breadcrumb",{staticClass:"app-breadcrumb",attrs:{"separator-class":"el-icon-arrow-right"}},e._l(e.titleName,(function(t){return n("el-breadcrumb-item",{key:t,staticClass:"no-redirect"},[e._v(" "+e._s(t)+" ")])})),1),"undefined"!==typeof e.editFunc?n("el-link",{staticClass:"icon-create",on:{click:function(t){return e.editFunc()}}},[n("svg-icon",{attrs:{"icon-class":"edit"}})],1):e._e(),"undefined"!==typeof e.delFunc?n("el-link",{staticClass:"icon-create",on:{click:function(t){return e.delFunc()}}},[n("svg-icon",{attrs:{"icon-class":"delete"}})],1):e._e(),n("div",{staticClass:"right"},["undefined"!==typeof e.nsFunc?n("el-select",{attrs:{multiple:"",placeholder:"命名空间",size:"small"},on:{change:e.nsChange},model:{value:e.nsInput,callback:function(t){e.nsInput=t},expression:"nsInput"}},e._l(e.namespaces,(function(e){return n("el-option",{key:e.name,attrs:{label:e.name,value:e.name}})})),1):e._e(),"undefined"!==typeof e.nameFunc?n("el-input",{attrs:{size:"small",placeholder:"搜索","suffix-icon":"el-icon-search"},on:{input:e.nameDebounce},model:{value:e.nameInput,callback:function(t){e.nameInput=t},expression:"nameInput"}}):e._e()],1)],1)},i=[],r=(n("b0c0"),n("aad4")),o=n("5c96"),c={name:"Clusterbar",props:{titleName:{type:Array,required:!0,default:function(){return[]}},nsFunc:{type:Function,required:!1,default:void 0},nameFunc:{type:Function,required:!1,default:void 0},delFunc:{type:Function,required:!1,default:void 0},editFunc:{type:Function,required:!1,default:void 0}},data:function(){return{nameInput:"",nsInput:[],namespaces:[]}},created:function(){"undefined"!==typeof this.nsFunc&&this.fetchNamespace()},methods:{nsChange:function(e){this.nsFunc&&this.nsFunc(e)},nameDebounce:function(){var e=this;this.nameFunc&&(a&&clearTimeout(a),a=setTimeout((function(){e.nameFunc(e.nameInput),a=void 0}),500))},fetchNamespace:function(){var e=this;this.namespaces=[];var t=this.$store.state.cluster;t?Object(r["b"])(t).then((function(t){e.namespaces=t.data,e.namespaces.sort((function(e,t){return e.name>t.name?1:-1}))})).catch((function(){})):o["Message"].error("获取集群异常，请刷新重试")}}},l=c,u=(n("589b"),n("dda3"),n("2877")),d=Object(u["a"])(l,s,i,!1,null,"3d7b3a75",null),m=d.exports,f=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"xterm",attrs:{id:"xterm"}})},h=[],g=(n("99af"),n("abb2"),n("fcf3")),p=n("47d0"),v=n("173c"),b={name:"Xterm",data:function(){return{socket:null,term:null}},props:{cluster:{type:String,required:!0,default:""},namespace:{type:String,required:!0,default:""},pod:{type:String,required:!0,default:""},container:{type:String,required:!1,default:""}},mounted:function(){this.initTerm()},beforeDestroy:function(){this.socket&&(this.socket.send("\r\nexit\r"),this.socket.close()),this.term&&this.term.dispose()},methods:{initTerm:function(){var e=Math.floor((window.innerHeight-100)/20);console.log(e);var t=new g["Terminal"]({fontSize:14,cursorBlink:!0,rows:e}),n=new p["FitAddon"];t.loadAddon(n),t.open(document.getElementById("xterm")),n.fit(),t.focus(),this.term=t,this.initSocket()},initSocket:function(){var e=this.term.cols,t=this.term.rows;if(this.cluster)if(this.namespace)if(this.pod){var n="ws://".concat(window.location.host,"/api/v1/exec/").concat(this.cluster,"/").concat(this.namespace,"/").concat(this.pod);this.socket=new WebSocket(n+"?container=".concat(this.container,"&cols=").concat(e,"&rows=").concat(t)),this.socketOnClose(),this.socketOnOpen(),this.socketOnError()}else o["Message"].error("获取POD参数异常，请刷新重试");else o["Message"].error("获取命名空间参数异常，请刷新重试");else o["Message"].error("获取集群参数异常，请刷新重试")},socketOnOpen:function(){var e=this;this.socket.onopen=function(){var t=new v["AttachAddon"](e.socket);e.term.loadAddon(t)}},socketOnClose:function(){this.socket.onclose=function(){}},socketOnError:function(){this.socket.onerror=function(){}}}},y=b,w=Object(u["a"])(y,f,h,!1,null,null,null),k=w.exports,O=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"log-class",style:{height:e.logHeight+"px"},attrs:{id:"logDiv"}},[n("p",{staticStyle:{"white-space":"pre-line"}},[e._v(e._s(e.logs))])])},I=[],_=n("5f87"),x={name:"Logs",data:function(){return{logs:"",socket:null,scrollToBottom:!0}},props:{cluster:{type:String,required:!0,default:""},namespace:{type:String,required:!0,default:""},pod:{type:String,required:!0,default:""},container:{type:String,required:!1,default:""}},computed:{logHeight:function(){return window.innerHeight-200}},mounted:function(){var e=document.getElementById("logDiv"),t=this;e.addEventListener("scroll",(function(){t.scrollToBottom=!1,e.scrollTop+e.clientHeight===e.scrollHeight&&(t.scrollToBottom=!0)}),!0),this.initSocket()},beforeDestroy:function(){this.socket&&this.socket.close()},methods:{initSocket:function(){var e=Object(_["a"])();if(console.log(e),this.cluster)if(this.namespace)if(this.pod){var t="ws://".concat(window.location.host,"/osp/api/log/").concat(this.cluster,"/").concat(this.namespace,"/").concat(this.pod);this.socket=new WebSocket(t+"?container=".concat(this.container,"&token=").concat(e)),this.socketOnClose(),this.socketOnOpen(),this.socketOnError(),this.socketOnMessage()}else o["Message"].error("获取POD参数异常，请刷新重试");else o["Message"].error("获取命名空间参数异常，请刷新重试");else o["Message"].error("获取集群参数异常，请刷新重试")},socketOnOpen:function(){this.socket.onopen=function(){}},socketOnClose:function(){this.socket.onclose=function(){}},socketOnError:function(){this.socket.onerror=function(){}},socketOnMessage:function(){var e=this;this.socket.onmessage=function(t){e.logs+=t.data;var n=e;e.$nextTick((function(){if(n.scrollToBottom){var e=document.getElementById("logDiv");e.scrollTop=e.scrollHeight}}))}}}},S=x,j=(n("147d"),Object(u["a"])(S,O,I,!1,null,"72e53532",null)),F=j.exports,C=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],staticClass:"yaml-editor",style:"--yamlHeight: "+e.yamlHeight+"px"},[n("textarea",{ref:"textarea"})])},D=[],E=n("56b3"),M=n.n(E);n("0dd0"),n("a7be"),n("cc10"),n("ced0"),n("8822"),n("b8d1");window.jsyaml=n("651e");var N={name:"YamlEditor",props:["value","loading","updateValue"],data:function(){return{yamlEditor:!1}},computed:{yamlHeight:function(){return window.innerHeight-250}},watch:{value:function(e){var t=this.yamlEditor.getValue();e!==t&&this.yamlEditor.setValue(this.value)}},mounted:function(){var e=this;this.yamlEditor=M.a.fromTextArea(this.$refs.textarea,{lineNumbers:!0,mode:"text/x-yaml",gutters:["CodeMirror-lint-markers"],theme:"base16-light",lint:!0,lineWrapping:!0}),this.yamlEditor.setValue(this.value),this.yamlEditor.on("change",(function(t){e.$emit("input",t.getValue())}))},methods:{getValue:function(){return this.yamlEditor.getValue()}}},H=N,V=(n("db62"),Object(u["a"])(H,C,D,!1,null,"5bb854da",null)),T=V.exports},6414:function(e,t,n){"use strict";var a=n("4b16"),s=n.n(a);s.a},"714a":function(e,t,n){},"9f46":function(e,t,n){"use strict";n.d(t,"c",(function(){return s})),n.d(t,"b",(function(){return i})),n.d(t,"a",(function(){return r})),n.d(t,"d",(function(){return o}));n("99af");var a=n("b775");function s(e){return Object(a["a"])({url:"ingress/".concat(e),method:"get"})}function i(e,t,n){var s=arguments.length>3&&void 0!==arguments[3]?arguments[3]:"";return Object(a["a"])({url:"ingress/".concat(e,"/").concat(t,"/").concat(n),method:"get",params:{output:s}})}function r(e,t){return Object(a["a"])({url:"ingress/".concat(e,"/delete"),method:"post",data:t})}function o(e,t,n,s){return Object(a["a"])({url:"ingress/".concat(e,"/").concat(t,"/").concat(n),method:"post",data:{yaml:s}})}},a15b:function(e,t,n){"use strict";var a=n("23e7"),s=n("44ad"),i=n("fc6a"),r=n("a640"),o=[].join,c=s!=Object,l=r("join",",");a({target:"Array",proto:!0,forced:c||!l},{join:function(e){return o.call(i(this),void 0===e?",":e)}})},aad4:function(e,t,n){"use strict";n.d(t,"b",(function(){return s})),n.d(t,"a",(function(){return i}));n("99af");var a=n("b775");function s(e){return Object(a["a"])({url:"namespace/".concat(e),method:"get"})}function i(e,t,n){return Object(a["a"])({url:"namespace/".concat(e,"/").concat(t),method:"get",params:{output:n}})}},b76c:function(e,t,n){},b85c:function(e,t,n){"use strict";n.d(t,"a",(function(){return s}));n("a4d3"),n("e01a"),n("d28b"),n("d3b7"),n("3ca3"),n("ddb0");var a=n("06c5");function s(e,t){var n;if("undefined"===typeof Symbol||null==e[Symbol.iterator]){if(Array.isArray(e)||(n=Object(a["a"])(e))||t&&e&&"number"===typeof e.length){n&&(e=n);var s=0,i=function(){};return{s:i,n:function(){return s>=e.length?{done:!0}:{done:!1,value:e[s++]}},e:function(e){throw e},f:i}}throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}var r,o=!0,c=!1;return{s:function(){n=e[Symbol.iterator]()},n:function(){var e=n.next();return o=e.done,e},e:function(e){c=!0,r=e},f:function(){try{o||null==n["return"]||n["return"]()}finally{if(c)throw r}}}}},b92f:function(e,t,n){},d7ff:function(e,t,n){"use strict";n.r(t);var a=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[n("clusterbar",{attrs:{titleName:e.titleName,nsFunc:e.nsSearch,nameFunc:e.nameSearch,delFunc:e.delFunc}}),n("div",{staticClass:"dashboard-container"},[n("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.loading,expression:"loading"}],ref:"multipleTable",staticClass:"table-fix",staticStyle:{width:"100%"},attrs:{data:e.ingresses,"tooltip-effect":"dark","max-height":e.maxHeight,"cell-style":e.cellStyle,"default-sort":{prop:"name"},"row-key":"uid"},on:{"selection-change":e.handleSelectionChange}},[n("el-table-column",{attrs:{type:"selection",width:"45"}}),n("el-table-column",{attrs:{prop:"name",label:"名称","min-width":"50","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(t){return[n("span",{staticClass:"name-class",on:{click:function(n){return e.nameClick(t.row.namespace,t.row.name)}}},[e._v(" "+e._s(t.row.name)+" ")])]}}])}),n("el-table-column",{attrs:{prop:"namespace",label:"命名空间","min-width":"40","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{prop:"rules",label:"访问域名","min-width":"75","show-overflow-tooltip":""},scopedSlots:e._u([{key:"default",fn:function(t){return[n("span",[e._v(" "+e._s(e.getIngressHosts(t.row.rules))+" ")])]}}])}),n("el-table-column",{attrs:{prop:"created",label:"创建时间","min-width":"40","show-overflow-tooltip":""}}),n("el-table-column",{attrs:{label:"","show-overflow-tooltip":"",width:"45"},scopedSlots:e._u([{key:"default",fn:function(t){return[n("el-dropdown",{attrs:{size:"medium"}},[n("el-link",{attrs:{underline:!1}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em"},attrs:{"icon-class":"operate"}})],1),n("el-dropdown-menu",{attrs:{slot:"dropdown"},slot:"dropdown"},[n("el-dropdown-item",{nativeOn:{click:function(n){return n.preventDefault(),e.nameClick(t.row.namespace,t.row.name)}}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em","line-height":"40px","vertical-align":"-0.25em"},attrs:{"icon-class":"detail"}}),n("span",{staticStyle:{"margin-left":"5px"}},[e._v("详情")])],1),n("el-dropdown-item",{nativeOn:{click:function(n){return n.preventDefault(),e.getIngressYaml(t.row.namespace,t.row.name)}}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em","line-height":"40px","vertical-align":"-0.25em"},attrs:{"icon-class":"edit"}}),n("span",{staticStyle:{"margin-left":"5px"}},[e._v("修改")])],1),n("el-dropdown-item",{nativeOn:{click:function(n){return n.preventDefault(),e.deleteIngresses([{namespace:t.row.namespace,name:t.row.name}])}}},[n("svg-icon",{staticStyle:{width:"1.3em",height:"1.3em","line-height":"40px","vertical-align":"-0.25em"},attrs:{"icon-class":"delete"}}),n("span",{staticStyle:{"margin-left":"5px"}},[e._v("删除")])],1)],1)],1)]}}])})],1)],1),n("el-dialog",{attrs:{title:"编辑",visible:e.yamlDialog,"close-on-click-modal":!1,width:"60%",top:"55px"},on:{"update:visible":function(t){e.yamlDialog=t}}},[e.yamlDialog?n("yaml",{attrs:{loading:e.yamlLoading},model:{value:e.yamlValue,callback:function(t){e.yamlValue=t},expression:"yamlValue"}}):e._e(),n("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[n("el-button",{attrs:{plain:"",size:"small"},on:{click:function(t){e.yamlDialog=!1}}},[e._v("取 消")]),n("el-button",{attrs:{plain:"",size:"small"},on:{click:function(t){return e.updateIngress()}}},[e._v("确 定")])],1)],1)],1)},s=[],i=(n("4de4"),n("caad"),n("c975"),n("a15b"),n("b0c0"),n("2532"),n("b85c")),r=n("61b2"),o=n("9f46"),c=n("5c96"),l={name:"Ingress",components:{Clusterbar:r["a"],Yaml:r["d"]},data:function(){return{yamlDialog:!1,yamlNamespace:"",yamlName:"",yamlValue:"",yamlLoading:!0,cellStyle:{border:0},titleName:["Ingresses"],maxHeight:window.innerHeight-150,loading:!0,originIngresses:[],search_ns:[],search_name:"",delFunc:void 0,delIngresses:[]}},created:function(){this.fetchData()},mounted:function(){var e=this;window.onresize=function(){return function(){var t=window.innerHeight-150;e.maxHeight=t}()}},watch:{ingressesWatch:function(e){if(e){var t=e.resource.metadata.uid,n=e.resource.metadata.resourceVersion;if("add"===e.event)this.originIngresses.push(this.buildIngresses(e.resource));else if("update"===e.event)for(var a in this.originIngresses){var s=this.originIngresses[a];if(s.uid===t){if(s.resource_version<n){var i=this.buildIngresses(e.resource);this.$set(this.originIngresses,a,i)}break}}else"delete"===e.event&&(this.originIngresses=this.originIngresses.filter((function(e){var n=e.uid;return n!==t})))}}},computed:{ingresses:function(){var e,t=[],n=Object(i["a"])(this.originIngresses);try{for(n.s();!(e=n.n()).done;){var a=e.value;this.search_ns.length>0&&this.search_ns.indexOf(a.namespace)<0||(this.search_name&&!a.name.includes(this.search_name)||(a.conditions&&a.conditions.length>0?a.conditions.sort():a.conditions=[],t.push(a)))}}catch(s){n.e(s)}finally{n.f()}return t},ingressesWatch:function(){return this.$store.getters["ws/ingressesWatch"]}},methods:{fetchData:function(){var e=this;this.loading=!0,this.originIngresses=[];var t=this.$store.state.cluster;t?Object(o["c"])(t).then((function(t){e.loading=!1,e.originIngresses=t.data})).catch((function(){e.loading=!1})):(this.loading=!1,c["Message"].error("获取集群异常，请刷新重试"))},nsSearch:function(e){this.search_ns=[];var t,n=Object(i["a"])(e);try{for(n.s();!(t=n.n()).done;){var a=t.value;this.search_ns.push(a)}}catch(s){n.e(s)}finally{n.f()}},nameSearch:function(e){this.search_name=e},buildIngresses:function(e){if(e){var t={uid:e.metadata.uid,namespace:e.metadata.namespace,name:e.metadata.name,backend:e.spec.backend,tls:e.spec.tls,rules:e.spec.rules,resource_version:e.metadata.resourceVersion,created:e.metadata.creationTimestamp};return t}},nameClick:function(e,t){this.$router.push({name:"ingressDetail",params:{namespace:e,ingressName:t}})},getIngressYaml:function(e,t){var n=this;this.yamlNamespace="",this.yamlName="";var a=this.$store.state.cluster;a?e?t?(this.yamlValue="",this.yamlDialog=!0,this.yamlLoading=!0,Object(o["b"])(a,e,t,"yaml").then((function(a){n.yamlLoading=!1,n.yamlValue=a.data,n.yamlNamespace=e,n.yamlName=t})).catch((function(){n.yamlLoading=!1}))):c["Message"].error("获取Deployment名称参数异常，请刷新重试"):c["Message"].error("获取命名空间参数异常，请刷新重试"):c["Message"].error("获取集群参数异常，请刷新重试")},deleteIngresses:function(e){var t=this.$store.state.cluster;if(t)if(e.length<=0)c["Message"].error("请选择要删除的Ingresses");else{var n={resources:e};Object(o["a"])(t,n).then((function(){c["Message"].success("删除成功")})).catch((function(){}))}else c["Message"].error("获取集群参数异常，请刷新重试")},updateIngress:function(){var e=this.$store.state.cluster;e?this.yamlNamespace?this.yamlName?(console.log(this.yamlValue),Object(o["d"])(e,this.yamlNamespace,this.yamlName,this.yamlValue).then((function(){c["Message"].success("更新成功")})).catch((function(){}))):c["Message"].error("获取Ingress参数异常，请刷新重试"):c["Message"].error("获取命名空间参数异常，请刷新重试"):c["Message"].error("获取集群参数异常，请刷新重试")},_delIngressesFunc:function(){if(this.delIngresses.length>0){var e,t=[],n=Object(i["a"])(this.delIngresses);try{for(n.s();!(e=n.n()).done;){var a=e.value;t.push({namespace:a.namespace,name:a.name})}}catch(s){n.e(s)}finally{n.f()}this.deleteIngresses(t)}},handleSelectionChange:function(e){this.delIngresses=e,e.length>0?this.delFunc=this._delIngressesFunc:this.delFunc=void 0},getIngressHosts:function(e){if(!e)return"";var t,n=[],a=Object(i["a"])(e);try{for(a.s();!(t=a.n()).done;){var s=t.value;n.push(s.host)}}catch(r){a.e(r)}finally{a.f()}return n.join(",")}}},u=l,d=(n("1b0e"),n("6414"),n("2877")),m=Object(d["a"])(u,a,s,!1,null,"27b88a68",null);t["default"]=m.exports},db62:function(e,t,n){"use strict";var a=n("43df"),s=n.n(a);s.a},dda3:function(e,t,n){"use strict";var a=n("b92f"),s=n.n(a);s.a},f6bf:function(e,t,n){}}]);