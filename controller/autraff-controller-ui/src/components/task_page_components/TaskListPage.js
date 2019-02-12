import React, { Component } from 'react';

import { Table, List, Card } from 'antd';

class TaskListPage extends Component {
  state = {
    TaskInfo: [{
      key: '1',
      name: 'news_browsing',
      active: 'true',
      deployment: '10.0.0.4',
      persona: 'Alice',
      period: '10 hours',
      start: '2018-12-20 20:05:58'
    }, {
      key: '2',
      name: 'news_browsing',
      active: 'true',
      deployment: '10.0.0.6',
      persona: 'Bob',
      period: '2 hours',
      start: '2018-12-20 21:08:41'
    }, {
      key: '3',
      name: 'work_routine',
      active: 'true',
      deployment: '10.0.0.7',
      persona: 'Eve',
      period: '24 hours',
      start: '2018-12-25 20:17:52'
    }, {
      key: '4',
      name: 'news_browsing',
      active: 'true',
      deployment: '10.0.0.4',
      persona: 'Alice',
      period: '1 hours',
      start: '2019-01-12 10:36:43'
    }, {
      key: '5',
      name: 'work_routine',
      active: 'true',
      deployment: '10.0.0.7',
      persona: 'Eve',
      period: '24 hours',
      start: '2019-1-13 18:12:11'
    }, {
      key: '6',
      name: 'work_routine',
      active: 'true',
      deployment: '10.0.0.7',
      persona: 'Eve',
      period: '24 hours',
      start: '2019-01-14 09:11:49'
    }, ]
  };

  taskInfoColumns = [{
    title: 'Task ID',
    dataIndex: 'key',
  }, {
    title: 'Task Name',
    dataIndex: 'name',
  }, {
    title: 'is Alive',
    dataIndex: 'active',
  }, {
    title: 'Deployed machine',
    dataIndex: 'deployment',
  }, {
    title: 'Persona',
    dataIndex: 'persona',
  }, {
    title: 'Period',
    dataIndex: 'period',
  }, {
    title: 'Start time',
    dataIndex: 'start',
  },];

  render() {
    return (
      <div>
        <h1>Task list</h1>
        <hr></hr>

        <Table
          bordered
          columns={this.taskInfoColumns}
          dataSource={this.state.TaskInfo}
        />
      </div>
    );
  }
}

export default TaskListPage;
