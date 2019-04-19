
import React, { Component } from 'react';

import { Table, List, Card } from 'antd';

class JobDashboard extends Component {
  state = {
    jobInfo: [],
    overallStates: [{
      title: 'Number of Clients',
      value: '2' // TODO dummy data now
    }, {
      title: 'Number of Active Clients',
      value: '2' // TODO dummy data now
    }, {
      title: 'Last Modification on',
      value: 'Wthin 1 hour' // TODO dummy data now
    }, {
      title: 'Number of Scheduled Tasks',
      value: 'NA' // TODO dummy data now
    }],
  };

  jobInfoColumns = [{
    title: 'Alias',
    dataIndex: 'name',
  }, {
    title: 'Client',
    dataIndex: 'client',
  }, {
    title: 'Scheduled',
    dataIndex: 'active'
  }, {
    title: 'Arguments',
    dataIndex: 'arguments',
  },];

  componentDidMount() {
    let countScheduled = 0
    fetch('http://localhost:5000/job', {
      method: "GET",
    }).then(results => {
      return results.json()
    }).then(data => {
      var jobs = data.map((job) => {
        var newDict = {}
        newDict['name'] = job.name
        newDict['client'] = job.client
        newDict['module'] = job.module
        newDict['interval'] = job.interval
        newDict['arguments'] = job.arguments
        newDict['start'] = job.start
        newDict['schedule_id'] = job.schedule_id

        // console.log(job)

        if (newDict['schedule_id'] === null || newDict['schedule_id'] === "") {
          newDict['active'] = 'inactive'
        } else {
          countScheduled ++
          newDict['active'] = 'active'
        }
        return newDict
      })
      this.setState({
        jobInfo: jobs,
        overallStates: [{
          title: 'Number of Clients',
          value: '2' // TODO dummy data now
        }, {
          title: 'Number of Active Clients',
          value: '2' // TODO dummy data now
        }, {
          title: 'Last Modification on',
          value: 'Wthin 1 hour' // TODO dummy data now
        }, {
          title: 'Number of Scheduled Tasks',
          value: countScheduled
        }]
      })
    })
  }

  render() {
    return (
      <div>
        <h1>Dashboard</h1>
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
          columns={this.jobInfoColumns}
          dataSource={this.state.jobInfo}
          rowKey="id"
        />
      </div>
    );
  }
}

export default JobDashboard;
