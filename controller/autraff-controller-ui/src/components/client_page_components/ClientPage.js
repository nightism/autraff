import React, { Component } from 'react';

import { Table, List, Card } from 'antd';

class ClientPage extends Component {
  state = {
    taskInfo: [
      {
        key: '1',
        active: 'No',
        name: 'search NUS',
        module: 'module_search_keyword',
        interval: '10',
        duration: '5'
      }
    ]
  };

  taskInfoColumns = [{
    title: 'Name',
    dataIndex: 'name',
  }, {
    title: 'Active',
    dataIndex: 'active',
  }, {
    title: 'Module',
    dataIndex: 'module',
  }, {
    title: 'Interval',
    dataIndex: 'interval',
  }, {
    title: 'Duration',
    dataIndex: 'duration'
  }];


  render() {
    return (
      <div>
        <h1>127.0.0.1</h1>
        <hr></hr>

        <Table
          bordered
          columns={this.taskInfoColumns}
          dataSource={this.state.taskInfo}
        />
      </div>
    );
  }
}

export default ClientPage;
