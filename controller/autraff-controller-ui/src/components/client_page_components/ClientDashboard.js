import React, { Component } from 'react';

import { Table, List, Card } from 'antd';

class ClientDashboard extends Component {
  state = {
    overallStates: [{
      title: 'Number of Clients',
      value: '4'
    }, {
      title: 'Number of Active Clients',
      value: '3'
    }, {
      title: 'Last Modification on',
      value: '25 Nov 2018 18:59'
    }, {
      title: 'Number of Scheduled Tasks',
      value: '13'
    }],
    clientInfo: [{
      key: '10.0.0.4',
      name: '10.0.0.4',
      active: 'true',
      tasks: 4,
      os: 'Linux',
    }, {
      key: '10.0.0.5',
      name: '10.0.0.5',
      active: 'false',
      tasks: 0,
      os: 'Linux',
    }, {
      key: '10.0.0.6',
      name: '10.0.0.6',
      active: 'true',
      tasks: 6,
      os: 'Windows',
    }, {
      key: '10.0.0.7',
      name: '10.0.0.7',
      active: 'true',
      tasks: 4,
      os: 'MacOS',
    }]
  };

  clientInfoColumns = [{
    title: 'IP address',
    dataIndex: 'name',
  }, {
    title: 'Active',
    dataIndex: 'active',
  }, {
    title: 'Tasks scheduled',
    dataIndex: 'tasks',
  }, {
    title: 'Operating System',
    dataIndex: 'os',
  },];

  render() {
    return (
      <div>
        <h1>Dashboardd</h1>
        <hr></hr>

        <List
          grid={ {gutter: 20, column: 4} }
          dataSource={this.state.overallStates}
          renderItem={item  => (
            <List.Item>
              <Card title={item.title}> {item.value} </Card>
            </List.Item>
          )}
        />

        <Table
          bordered
          columns={this.clientInfoColumns}
          dataSource={this.state.clientInfo}
        />
      </div>
    );
  }
}

export default ClientDashboard;
