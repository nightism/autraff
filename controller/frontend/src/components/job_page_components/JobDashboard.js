
import React, { Component } from 'react';

import { Table, List, Card } from 'antd';

class JobDashboard extends Component {
  state = {
    overallStates: [{
      title: 'Number of Clients',
      value: 'NA'
    }, {
      title: 'Number of Active Clients',
      value: 'NA'
    }, {
      title: 'Last Modification on',
      value: 'NA'
    }, {
      title: 'Number of Scheduled Tasks',
      value: 'NA'
    }],
  };

  jobInfoColumns = [{
    title: 'Alias',
    dataIndex: 'name',
  }, {
    title: 'Client',
    dataIndex: 'client',
  }, {
    title: 'Active',
    dataIndex: 'active'
  }, {
    title: 'Interval',
    dataIndex: 'arguments',
  }, {
    title: 'Start Time',
    dataIndex: 'start',
  }, {
    title: 'Sequence Number',
    dataIndex: 'id',
    className: 'hide',
  }];

  componentDidMount() {
    fetch('http://localhost:5000/job', {
      method: "GET",
    }).then(results => {
      return results.json()
    }).then(data => {
      var jobs = data.map((job) => {
        var newDict = {}
        newDict['name'] = job.name
        newDict['client'] = job.client
        newDict['persona'] = job.persona
        newDict['module'] = job.module
        newDict['interval'] = job.interval
        newDict['arguments'] = job.arguments
        newDict['start'] = job.start
        newDict['schedule_id'] = job.schedule_id
        newDict['id'] = job.seq

        // console.log(job)

        if (newDict['schedule_id'] === null || newDict['schedule_id'] === "") {
          newDict['active'] = 'inactive'
        } else {
          newDict['active'] = 'active'
        }
        return newDict
      })
      this.setState({jobInfo: jobs})
      // console.log(this.state.jobInfo)
      // console.log(jobs)
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
