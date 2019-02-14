
<template>
    <b-row>
      <b-col md="3" lg="3" xl="5">
          <v-jstree ref="tree" textFieldName="title"
             :data="treeData"
             @item-toggle="nodeToggle"
             >
          </v-jstree>
      </b-col>
      <b-col md="9" lg="9" xl="7">

      </b-col>
    </b-row>
</template>
  
<script>
import VJstree from 'vue-jstree'

export default {
  name: "BookTree",
  components: {
    VJstree
  },
  mounted : function(){
      this.$backend.$getRoot().then((rootNodes) => this.treeData = rootNodes)
  },
  data : function(){
    return {
      treeData: [],
      editingNode: null, 
      editingItem: {},
    }
  },
  methods: {
    nodeToggle(node, item, e){
     if (!item.loaded && item.opened){
       this.updateNode(node, item)
     } else {

     }
    },
    updateNode(node, item){
      console.log(item.opened);
      switch(node.data.meta.class){
        case 'page': this.$backend.$getPage(node.data.id).then((pageNode) => {
          node.model.children = pageNode.children;
          node.data.loaded = true;
        }); break;    
        case 'task': this.$backend.$getTask(node.data.id).then((task) => this.updateTaskNode(node, task)); break;
      }
    
    }
  }
}

/*       loadData: function (node, resolve) {
        if (node.data.meta == undefined){
          this.$backend.$getRoot().then((pages) => resolve(pages));
        } else {
          switch(node.data.meta.class){
            case 'page': {
              if(!node.data.isLeaf && node.data.loaded == undefined){
                this.$backend.$getPage(node.data.id).then((page) => {
                  resolve(page);
                  node.data.loaded = true;
                  for(let child of Object.values(page.children)){
                    node.data.addChild(child);
                  }
                })
              } 
              break;
            }
            case 'task': this.$backend.$getTask(node.id).then((task) => resolve(task)); break;
          }
        }
      },  */     
</script>

          <!-- <b-tabs v-if="currentNode" small card v-model="tabIndex">
            <b-tab title="Просмотр">
                <small>{{ currentNode.data.author.name }}</small>
                <h2>{{ currentNode.data.title }}</h2>
                <div v-for="item in currentNode.data.body" :key="item.type" >{{ item.content }}</div>
            </b-tab>
            <b-tab  v-if="currentNode.data.tests" title="Тесты">
              <b-table striped hover :items="currentNode.data.tests" :fields="testsFields"></b-table>
            </b-tab>
          </b-tabs> -->

