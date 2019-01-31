
Vue.component('book-tree', {
  data : function(){
    return {
      treeData: this.getBookRoot(),
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
    }

  },
  template: '<div><tree :data="treeData" @node:expanded="nodeExpanded" @node:selected="nodeSelected" /></div>'
})

