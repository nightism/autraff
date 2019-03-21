import React, { Component } from 'react';

import { Table, List, Card } from 'antd';

class JobListPage extends Component {
  state = {
    jobInfo: []
  };

  jobInfoColumns = [{
    title: 'Task ID',
    dataIndex: 'schedule_id',
  }, {
    title: 'Task Name',
    dataIndex: 'name',
  }, {
    title: 'Module',
    dataIndex: 'module',
  }, {
    title: 'Deployed machine',
    dataIndex: 'client',
  }, {
    title: 'Persona',
    dataIndex: 'persona',
  }, {
    title: 'Period',
    dataIndex: 'interval',
  }, {
    title: 'Start time',
    dataIndex: 'start',
  }, {
    title: 'Sequence',
    dataIndex: 'seq'
  }];

  componentDidMount() {
    fetch('http://localhost:5000/job', {
      method: "GET",
    }).then(results => {
      return results.json()
    }).then(data => {
      var jobs = data.map((job) => {
        var newDict = {}
        newDict['seq'] = job.seq
        newDict['name'] = job.name
        newDict['client'] = job.client
        newDict['persona'] = job.persona
        newDict['module'] = job.module
        newDict['interval'] = job.interval
        newDict['arguments'] = job.arguments
        newDict['start'] = job.start
        newDict['schedule_id'] = job.schedule_id
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
        <h1>Task list</h1>
        <hr></hr>

        <Table
          bordered
          columns={this.jobInfoColumns}
          dataSource={this.state.jobInfo}
          rowKey="seq"
        />
      </div>
    );
  }
}

export default JobListPage;
