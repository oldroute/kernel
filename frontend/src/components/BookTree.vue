
<template>
    <b-row>
      <b-col md="3" lg="3" xl="5">
        <tree :data="treeData" :options="treeOptions" ref="tree" @node:expanded="nodeExpanded" @node:selected="nodeSelected">
          <div slot-scope="{ node }" class="node-container" >
            <div class="node-text">{{ node.text }}</div>
          </div>
        </tree>
      </b-col>
      <b-col md="9" lg="9" xl="7">
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
      </b-col>
    </b-row>
</template>
  
<script>
import LiquorTree from 'liquor-tree';

export default {
  name: "BookTree",
  components: {
    [LiquorTree.name]: LiquorTree
  },
  data : function(){
    return {
      treeData: this.getRootNodes(),
      currentNode: null,
      testsFields: ['input', 'output'],
      treeOptions: {
        dnd: true
      }
    }
  },
  methods: {
    
    getRootNodes(){
      return this.$backend.$getRoot().then((pages) => {
        let treeRoot = [];
        for (let page of Object.values(pages)){
          page.text = page.data.title
          page.data.loaded = false;
          if (page.data.tasks_or_children_exists) page.children =[{}]
          treeRoot.push(page)
        }
        return treeRoot
      })
    },
    updatePageNode(node, page){
      node.data = page.data;
      node.data.text = node.data.title
      node.data.loaded = true;
      node.children = [];
      if (node.data.tasks_exists){
        let treeTasks = {
          text: 'Задачи',
          data: {class: 'tasks'},
          children: [],
        }
        for (let task of Object.values(page.tasks)){
          task.text = task.data.title;
          task.data.loaded = false;
          treeTasks.children.push(task)
        }
        node.append(treeTasks)
      }

      if (page.data.children_exists){
        for(let child of Object.values(page.children)){
          child.text = child.data.title;
          child.data.loaded = false;
          if (child.data.tasks_or_children_exists) child.children =[{}];
          node.append(child)
        }
      }
    },
    updateTaskNode(node, task){
      node.data = task.data;
      node.data.text = task.data.title
      node.data.loaded = true;
    },
    updateNode(node){
      switch(node.data.class){
        case 'page': this.$backend.$getPage(node.id).then((page) => this.updatePageNode(node, page)); break;
        case 'task': this.$backend.$getTask(node.id).then((task) => this.updateTaskNode(node, task)); break;
        }
    },
    nodeExpanded(node){
      //node.selected(false);
      //console.log(node.data.children_exists, !node.data.loaded, !node.selected());
      if(node.data.tasks_or_children_exists && !node.data.loaded && !node.selected()){
        this.updateNode(node);
      }
    },
    nodeSelected(node){      
      //console.log(node.id, !node.data.loaded, !node.expanded());
      if(!node.data.loaded && !node.expanded()){
        this.updateNode(node);
      }
      this.currentNode = node;
    },
  }
}
</script>


