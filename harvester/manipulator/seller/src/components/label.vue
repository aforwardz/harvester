<template>
  <Manipulator name="Manipulator">
    <div class="label-container">
      <div class="label-input-container">
        <h1>标注</h1>
        <div class="label-create-container" v-if="label_pros.length === 0">
          <el-button icon="el-icon-plus" @click="newLabelProVisble=true">新增</el-button>
          <el-dialog title="新增标注" :visible.sync="newLabelProVisble">
            <el-form :model="newForm" ref="newForm" label-width="25%">
              <el-form-item label="标注项目名称" prop="project"
                            :rules="{ required: true, message: '请输入标注项目名称(英文)', trigger: 'blur' }">
                <el-input v-model="newForm.project" auto-complete="off" style="width:60%;"></el-input>
              </el-form-item>
              <el-form-item v-for="(lab, index) in newForm.labels" :label="'标注' + index"
                            :rules = "[{ required: true, message: '请输入标注名称(英文)', trigger: 'blur'},
                            {max: 10, message: '不超过10个字符', trigger: 'blur'}]" :prop="'labels.' + index + '.name'">
                <el-input v-model="lab.name" auto-complete="off" style="width:30%;margin-right: 10px"></el-input>
                <el-color-picker v-model="lab.color" style="margin-right: 10px"></el-color-picker>
                <el-button @click.prevent="removeLabel(index)">删除</el-button>
              </el-form-item>
              <el-form-item>
                <el-button @click="addLabel">新增标注</el-button>
              </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
              <el-button type="primary" @click="addLabelPro">保 存</el-button>
              <el-button @click="resetLabelPro">取 消</el-button>
            </div>
          </el-dialog>
        </div>
        <div class="label-detail-container" v-else>
          <div class="label-item" v-for="lab in label_pros">
            <span v-bind:style="{backgroundColor: lab.color}">{{lab.name}}</span>
          </div>
        </div>
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
      label_pros: [{'name': 'Player', 'color': '#FCA90E'}, {'name': 'Coach', 'color': '#FCA90E'},
      {'name': 'Club', 'color': '#FCA90E'}, {'name': 'Nation', 'color': '#FCA90E'}],
      label_list: [],
      newLabelProVisble: false,
      newForm: {
        'action': 'add',
        'project': '',
        'labels': [{name: '', color:''}]
      },
    }
  },
  methods: {
    addLabel() {
      this.newForm.labels.push({
        name: '',
        color: ''
      });
    },
    removeLabel(index) {
      this.newForm.labels.splice(index, 1);
    },
    addLabelPro: function() {
      console.log(this.newForm)
      this.$http.post(this.NLP_BASE + 'label_pro/', this.newForm).then(
        (response) => {
          this.newLabelProVisble = false;
          console.log(response.body);
          this.label_pros = this.newForm.labels;
          if (response.status === 200 && response.body.status === 'OK') {
            this.label_pros = this.newForm.labels;
            this.$message('创建成功')
          }
        }
      )
    },
    resetLabelPro: function() {
      this.newLabelProVisble = false;
      this.newForm = {
        'project': '',
        'labels': []
      };
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
      console.log(this.label_pros);
      this.$http.get(this.NLP_BASE + 'label_pro/').then(
        (response) => {
          console.log(response.body);
          this.label_pros = this.newForm.labels;
          if (response.status === 200 && response.body.status === 'OK') {
            this.label_pros = response.body.data;
          }
        }
      )
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
  .label-create-container {
    margin: auto;
  }
  .label-create-container .el-form-item__content {
    display: flex;
  }
  .el-checkbox.el-transfer-panel__item {
    z-index: 0;
  }
  .label-detail-container {
    width: 20%;
    height: 80%;
    margin: auto;
    display: flex;
    flex-wrap: wrap;
  }
  .label-item {
    margin: 0 2px;
  }
  .label-item span {
    padding: 0 2px;
  }
  .input-container {
    margin: auto;
    height: auto;
    width: auto;
    border-radius: 10px;
  }
  .label-input-container .el-textarea {
    width: 50%;
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
