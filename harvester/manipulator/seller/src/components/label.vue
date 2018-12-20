<template>
  <Manipulator name="Manipulator">
    <div class="label-container">
      <div class="label-input-container">
        <h1>标注</h1>
        <div class="label-create-container">
          <el-button icon="el-icon-plus" @click="newLabelProVisble=true">新增</el-button>
        </div>
        <el-dialog title="新增标注" v-model="newLabelProVisble">
            <el-form :model="newForm" ref="newForm" label-width="50px">
              <el-form-item label="标注项目名称" prop="project">
                <el-input v-model="newForm.project" auto-complete="off" style="width:70%;"></el-input>
              </el-form-item>
              <el-form-item v-for="(lab, index) in newForm.labels" :label="'标注' + index"
                            :prop="'labels.' + index + '.name'">
                <el-input v-model="lab.name" auto-complete="off" style="width:70%;"></el-input>
                <el-input v-model="lab.color" auto-complete="off" style="width:70%;"></el-input>
                <el-button @click.prevent="removeLabel(lab)">删除</el-button>
              </el-form-item>
              <el-form-item>
                <el-button @click="addLabel">新增标注</el-button>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button type="primary" @click="addLabelPro('newForm')">保 存</el-button>
              <el-button @click="resetLabelPro('newForm')">取 消</el-button>
            </div>
          </el-dialog>
        <el-input v-model="content" class="input-container" type="textarea" placeholder="请输入内容"></el-input>
        <div class="label-button-container">
          <el-button class="submit" type="primary" @click="labelContent">走你</el-button>
        </div>
      </div>
    </div>
    <div class="result-container" v-show="label_list.length > 0" v-loading="loading">
      <!--<div class="raw-item" v-for="word_list in label_list">-->
        <!--<div class="raw-word-item" v-for="word in word_list">-->
          <!--<span class="raw-word">{{word.word}}</span>-->
          <!--<span class="pos">{{word.pos_n}}</span>-->
        <!--</div>-->
      <!--</div>-->
      <div class="label-item" onselect="labelSelect()" @mouseup="selected()" v-for="word_list in label_list">
        <div class="label-word-item" v-for="(word, index) in word_list">
          <span :class="'ner-word ' + word.ner">{{word.word}}</span>
          <span class="ner">{{word.ner_n}}</span>
        </div>
      </div>
    </div>
  </Manipulator>
</template>

<script>
import Manipulator from './menu';

export default {
  name: 'Label',
  components: {
    Manipulator,
  },
  data() {
    return {
      loading: false,
      content: '',
      label_list: [],
      newLabelProVisble: false,
      newForm: {
        'project': '',
        'labels': []
      }
    }
  },
  methods: {
    addLabel() {
      this.newForm.labels.push({
        name: '',
        color: ''
      });
    },
    removeLabel(lab) {
      this.newForm.labels.push({
        name: '',
        color: ''
      });
    },
    addLabelPro: function(form) {

    },
    resetLabelPro: function(form) {
      this.newLabelProVisble = false;
    },
    labelContent: function() {
      this.loading = true;
      var data = {'content': this.content};
      this.$http.post(this.NLP_BASE + 'label/', data).then(
        (response) => {
          this.label_list = response.body.data;
          this.loading = false;
        }
      )
    },
    labelSelect: function() {
      console.log(document.selection)
    },
    selected: function() {
      console.log('selected')
      console.log(document.selection)
    },
    loadLabels: function() {

    }
  },
  created: function() {
    var lastLogined = this.$session.get('lastLogined');
    if (!lastLogined) {
      this.$router.push({
        path: '/login'
      })
    }
    this.loadLabels()
  }
};
</script>

<style>
  h1 {
    margin: 16px 0 0 10px;
  }
  .label-container {
    width: 90%;
    margin: 6rem auto 0 auto;
    height: 100%;
    background-color: rgba(255, 255, 255, .8);
    border-radius: 20px;
  }
  .label-input-container {
    height: 80px;
    display: flex;
  }
  .input-container {
    height: auto;
    width: auto;
    border-radius: 10px;
  }
  .label-input-container .el-textarea {
    width: 60%;
    height: auto;
  }
  .label-input-container .label-button-container {
    width: 10%;
    height: auto;
    margin: auto;
  }
  .label-button-container .submit {
    width: 100%;
    background-color: lightblue;
    color: hotpink;
  }
  .result-container {
    margin: 3rem auto;
    width: 90%;
    height: auto;
    display: flex;
    flex-direction: column;
    background-color: rgba(255, 255, 255, .8);
    border-radius: 15px;
  }
  .result-container .label-item {
    width: 95%;
    display: flex;
    margin: 10px auto;
    flex-wrap: wrap;
  }
  .label-item .label-word-item {
    height: 38px;
    display: flex;
    margin: 5px 1px;
    flex-direction: column;
    border: solid #aeaeae 0.5px;
  }
  .ner-word {
    height: 22px;
    text-align: center;
    font-weight: 500;
  }
  .ner {
    height: 16px;
    padding: 0 1px;
    font-size: 12px;
    color: #f7faf5;
    text-align: center;
    background-color: #959595;
    -webkit-user-select: none; /* Safari */
    -moz-user-select: none; /* Firefox */
    -ms-user-select: none; /* IE10+/Edge */
    user-select: none; /* Standard */
  }
</style>
