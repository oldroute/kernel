
Vue.component('book-tree', {
  data : function(){
    return {
      treeData: this.getBookRoot(),
      node: {text: "", data: {text:""}}
    }
  },
  methods: {
    getBookRoot(){
      return $backend.$getBookRoot().then((response) => {return response});
    },
    getNodeData(node){
      switch(node.data.type){
        case 'page':
          $backend.$getPage(node.id).then((data) => {
            node.data = data["data"];
            node.data["loaded"] = true
            node.children = [];
            for (let child_node of Object.values(data["children"])) {
                node.append(child_node)
            }
          });
          break;
        case 'tasks':
          $backend.$getTasks(node.id).then((data) => {
            node.data["loaded"] = true
            node.children = [];
            for (let child_node of Object.values(data)) {
              node.append(child_node)
            }
          });
          break;
        case 'task':
          $backend.$getTask(node.id).then((data) => {
            node.data = data["data"];
            node.data["loaded"] = true
          });
          break;
        }
    },
    nodeExpanded(node){
      if(node.children.length > 0 && node.data["loaded"] == false && node.selected() == false ){
        this.getNodeData(node);
      }
    },
    nodeSelected(node){
      if(node.data["loaded"] == false && node.expanded() == false){
        this.getNodeData(node);
      }
    },
  },
  template: '\
    <b-row>\
      <b-col md="3" lg="3" xl="5">\
          <tree :data="treeData" ref="tree"  @node:expanded="nodeExpanded" >\
             <div slot-scope="{ node }"class="node-container" >\
                <div class="node-text">{{ node.text }}</div>\
             </div>\
          </tree>\
      </b-col>\
      <b-col md="9" lg="9" xl="7"></b-col>\
    </b-row>'
})

