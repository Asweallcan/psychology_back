(window.webpackJsonp=window.webpackJsonp||[]).push([[16],{203:function(e,t){},523:function(e,t,n){"use strict";n.r(t);var a,r=n(0),o=n(66),l=(n(196),n(525)),c=n(524),i=n(47),u=n.n(i),s=n(16),p=n(512),m=n(19),f=n(513),d=n(39),h=(n(408),n(7)),y=(n(60),n(12)),g=(n(34),n(14)),b=(n(203),a=function(e,t){return(a=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(e,t){e.__proto__=t}||function(e,t){for(var n in t)t.hasOwnProperty(n)&&(e[n]=t[n])})(e,t)},function(e,t){function n(){this.constructor=e}a(e,t),e.prototype=null===t?Object.create(t):(n.prototype=t.prototype,new n)}),E=function(e,t,n,a){var r,o=arguments.length,l=o<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,n):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)l=Reflect.decorate(e,t,n,a);else for(var c=e.length-1;0<=c;c--)(r=e[c])&&(l=(o<3?r(l):3<o?r(t,n,l):r(t,n))||l);return 3<o&&l&&Object.defineProperty(t,n,l),l},v=function(o,l,c,i){return new(c||(c=Promise))(function(e,t){function n(e){try{r(i.next(e))}catch(e){t(e)}}function a(e){try{r(i.throw(e))}catch(e){t(e)}}function r(t){t.done?e(t.value):new c(function(e){e(t.value)}).then(n,a)}r((i=i.apply(o,l||[])).next())})},w=function(n,a){var r,o,l,e,c={label:0,sent:function(){if(1&l[0])throw l[1];return l[1]},trys:[],ops:[]};return e={next:t(0),throw:t(1),return:t(2)},"function"==typeof Symbol&&(e[Symbol.iterator]=function(){return this}),e;function t(t){return function(e){return function(t){if(r)throw new TypeError("Generator is already executing.");for(;c;)try{if(r=1,o&&(l=2&t[0]?o.return:t[0]?o.throw||((l=o.return)&&l.call(o),0):o.next)&&!(l=l.call(o,t[1])).done)return l;switch(o=0,l&&(t=[2&t[0],l.value]),t[0]){case 0:case 1:l=t;break;case 4:return c.label++,{value:t[1],done:!1};case 5:c.label++,o=t[1],t=[0];continue;case 7:t=c.ops.pop(),c.trys.pop();continue;default:if(!(l=0<(l=c.trys).length&&l[l.length-1])&&(6===t[0]||2===t[0])){c=0;continue}if(3===t[0]&&(!l||t[1]>l[0]&&t[1]<l[3])){c.label=t[1];break}if(6===t[0]&&c.label<l[1]){c.label=l[1],l=t;break}if(l&&c.label<l[2]){c.label=l[2],c.ops.push(t);break}l[2]&&c.ops.pop(),c.trys.pop();continue}t=a.call(n,c)}catch(e){t=[6,e],o=0}finally{r=l=0}if(5&t[0])throw t[1];return{value:t[0]?t[1]:void 0,done:!0}}([t,e])}}},_=function(e){return{userInfo:e.httpResponse.getUserInfo}},x=["/","/papers","/admin/paper","/admin/user","/admin/grade"],O=function(t){function e(){var e=null!==t&&t.apply(this,arguments)||this;return e.logout=function(){return v(e,void 0,void 0,function(){var t,n;return w(this,function(e){switch(e.label){case 0:t=this.props.history,n=y.a.loading("",0),e.label=1;case 1:return e.trys.push([1,,3,4]),[4,g.actionsMap.logout({url:"/api/logout",method:"post"})];case 2:return e.sent(),t.push("/login"),[3,4];case 3:return n(),[7];case 4:return[2]}})})},e.getSelectKey=function(){var e=location.pathname;return x.indexOf(e).toString()},e}return b(e,t),e.prototype.componentDidMount=function(){return v(this,void 0,void 0,function(){return w(this,function(e){switch(e.label){case 0:return[4,g.actionsMap.getUserInfo({url:"/api/user",method:"get"})];case 1:return e.sent(),[2]}})})},e.prototype.render=function(){var e=this.props.userInfo,t=this.getSelectKey();return r.createElement(d.a,{mode:"inline",defaultSelectedKeys:[t],defaultOpenKeys:["paper","user","admin"],className:"main-page-menu"},r.createElement(d.a.SubMenu,{key:"user",title:r.createElement("span",null,r.createElement(h.a,{type:"user"}),"用户中心")},r.createElement(d.a.Item,null,r.createElement("span",{className:"main-page-menu-logout",onClick:this.logout},"退出登录")),r.createElement(d.a.Item,{key:"0"},r.createElement(p.a,{to:"/"},"个人信息"))),r.createElement(d.a.SubMenu,{key:"paper",title:r.createElement("span",null,r.createElement(h.a,{type:"laptop"}),"评测中心")},r.createElement(d.a.Item,{key:"1"},r.createElement(p.a,{to:"/papers"},"参加评测"))),e&&e.data.is_admin?r.createElement(d.a.SubMenu,{key:"admin",title:r.createElement("span",null,r.createElement(h.a,{type:"setting"}),"管理中心")},r.createElement(d.a.Item,{key:"2"},r.createElement(p.a,{to:"/admin/paper"},"试卷管理")),r.createElement(d.a.Item,{key:"3"},r.createElement(p.a,{to:"/admin/user"},"用户管理")),r.createElement(d.a.Item,{key:"4"},r.createElement(p.a,{to:"/admin/grade"},"成绩查询"))):null)},e=E([f.a,Object(s.connect)(_)],e)}(r.Component);n.d(t,"default",function(){return F});var k,N=(k=function(e,t){return(k=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(e,t){e.__proto__=t}||function(e,t){for(var n in t)t.hasOwnProperty(n)&&(e[n]=t[n])})(e,t)},function(e,t){function n(){this.constructor=e}k(e,t),e.prototype=null===t?Object.create(t):(n.prototype=t.prototype,new n)}),j=function(e,t,n,a){var r,o=arguments.length,l=o<3?t:null===a?a=Object.getOwnPropertyDescriptor(t,n):a;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)l=Reflect.decorate(e,t,n,a);else for(var c=e.length-1;0<=c;c--)(r=e[c])&&(l=(o<3?r(l):3<o?r(t,n,l):r(t,n))||l);return 3<o&&l&&Object.defineProperty(t,n,l),l},I=u()({loader:function(){return Promise.all([n.e(0),n.e(1),n.e(3),n.e(4),n.e(8)]).then(n.bind(null,519))},loading:m.b}),P=u()({loader:function(){return Promise.all([n.e(0),n.e(1),n.e(3),n.e(4),n.e(7)]).then(n.bind(null,521))},loading:m.b}),S=u()({loader:function(){return Promise.all([n.e(0),n.e(4),n.e(14),n.e(17)]).then(n.bind(null,516))},loading:m.b}),R=u()({loader:function(){return Promise.all([n.e(0),n.e(1),n.e(3),n.e(4),n.e(9)]).then(n.bind(null,520))},loading:m.b});function F(){return r.createElement(o.a,{className:"main-page"},r.createElement(o.a.Sider,{className:"main-page-sider"},r.createElement(O,null)),r.createElement(o.a.Content,{className:"main-page-content"},r.createElement(l.a,null,r.createElement(c.a,{exact:!0,path:"/",component:z}),r.createElement(c.a,{exact:!0,path:"/papers",component:S}),r.createElement(c.a,{exact:!0,path:"/admin/paper",component:I}),r.createElement(c.a,{exact:!0,path:"/admin/user",component:P}),r.createElement(c.a,{exact:!0,path:"/admin/grade",component:R}))))}var M=function(e){return{userInfo:e.httpResponse.getUserInfo}},z=function(e){function t(){return null!==e&&e.apply(this,arguments)||this}return N(t,e),t.prototype.render=function(){var e=this.props.userInfo;return r.createElement("div",{className:"index-page"},e?r.createElement(m.a,null,r.createElement("div",null,r.createElement("p",{className:"index-page-title"},e&&e.data.username),r.createElement("img",{className:"index-page-image",src:"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1551977395709&di=a531be11d5e6ff736b13de6b2b163bac&imgtype=0&src=http%3A%2F%2Fherbert.openrice.com%2Fimages%2Fv4%2Fmyopenrice%2Fmyor_img_welcome.jpg",alt:""}),r.createElement("p",null,"上次登录 ",e&&e.data.last_seen),r.createElement("dl",{className:"index-page-list"},e&&0<e.data.finished.length?r.createElement("dt",{className:"index-page-list-title"},"已完成的测评："):null,e&&e.data.finished.map(function(e){return r.createElement("dd",{className:"index-page-list-content"},e.paper_name," ",e.analyzed?r.createElement(p.a,{to:"/analyze/"+e.id},"去看报告"):"报告还在分析中哦")}),e&&0<e.data.unfinished.length?r.createElement("dt",{className:"index-page-list-title"},"参加但还没完成的测评："):null,e&&e.data.unfinished.map(function(e){return r.createElement("dd",{className:"index-page-list-content"},e.paper_name," ",e.analyzed?r.createElement(p.a,{to:"/test/"+e.id},"去继续评测"):"报告还在分析中哦")})))):r.createElement("p",{className:"index-page-error-text"},"身份验证失败，请重新登陆"))},t=j([Object(s.connect)(M)],t)}(r.Component)}}]);