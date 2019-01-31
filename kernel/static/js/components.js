
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
    getPage(node){
      if(node.children.length && node.data["loaded"] == false){
          $backend.$getPage(node.id).then((data) => {
            node.data = data["data"];
            node.data["loaded"] = true
            node.children = [];
            for (let child_node of Object.values(data["children"])) {
                node.append(child_node)
            }
          });
      }
    }

  },


      template: '<div><tree :data="treeData" @node:expanded="getPage" /></div>'
})

