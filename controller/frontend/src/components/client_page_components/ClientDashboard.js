import React, { Component } from 'react';

import { Table, List, Card, Row, Col } from 'antd';

class ClientDashboard extends Component {
  state = {
    overallStates: [{
      title: 'Number of Clients',
      value: '2'
    }, {
      title: 'Number of Active Clients',
      value: '1'
    }, {
      title: 'Last Modification on',
      value: '21 Feb 2019 21:47'
    }, {
      title: 'Number of Scheduled Tasks',
      value: '0'
    }],
    clientInfo: [],
    numOfClient: 0,
    numOfActiveClient: 'Unknown',
    lastModifiedOn: 'Unknown',
    numOfScheduledTasks: 'Unkown',
  };

  clientInfoColumns = [{
    title: 'IP address',
    dataIndex: 'key',
  }, {
    title: 'Active',
    dataIndex: 'active',
  }, {
    title: 'Tasks scheduled',
    dataIndex: 'tasks',
  }, {
    title: 'Operating System',
    dataIndex: 'os',
  }, {
    title: 'System Version',
    dataIndex: 'version'
  }];

  componentDidMount() {
    fetch('http://localhost:5000/client', {
      method: "GET",
    }).then(results => {
      return results.json()
    }).then(data => {
      var clientList = data.map((client) => {
        var newDict = {}
        newDict['key'] = client.ip
        newDict['active'] = 'unknown'
        newDict['tasks'] = '0'
        newDict['os'] = client.system
        newDict['version'] = client.version
        return newDict
      })
      this.setState({clientInfo: clientList})
      // console.log(this.state.clientInfo)
      // console.log(clientList)
    })
  }

  render() {
    return (
      <div>
        <h1>Dashboard</h1>
        <hr></hr>

        <Row gutter={20}>
          <Col span={6}>
            <Card title='Number of Clients'> {this.state.numOfClient} </Card>
          </Col>
          <Col span={6}>
            <Card title='Number of Active Clients'> {this.state.numOfActiveClient} </Card>
          </Col>
          <Col span={6}>
            <Card title='Last Modification on'> {this.state.lastModifiedOn} </Card>
          </Col>
          <Col span={6}>
            <Card title='Number of Scheduled Tasks'> {this.state.numOfScheduledTasks} </Card>
          </Col>
        </Row>

        <Table
          style={{ marginTop: '40px' }}
          bordered
          columns={this.clientInfoColumns}
          dataSource={this.state.clientInfo}
        />
      </div>
    );
  }
}

export default ClientDashboard;
