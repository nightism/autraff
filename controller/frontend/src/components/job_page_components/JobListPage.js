import React, { Component } from 'react';

import { Table, List, Card } from 'antd';


class JobListPage extends Component {
  state = {
    jobInfo: []
  };

  jobInfoColumns = [{
    title: 'Deployed machine',
    dataIndex: 'client',
  }, {
    title: 'Task Name',
    dataIndex: 'name',
  }, {
    title: 'Module',
    dataIndex: 'module',
  }, {
    title: 'Interval',
    dataIndex: 'interval',
  }, {
    title: 'Start time',
    dataIndex: 'start',
  }];


  nestedTableRendering(job) {
    let jobExpandedColumns = [{
      title: 'Arguments',
      dataIndex: 'arguments',
    }, {
      title: 'Scheduling ID',
      dataIndex: 'schedule_id',
    }, {
      title: 'On Success',
      dataIndex: 'success',
    }, {
      title: 'On Failure',
      dataIndex: 'failure',
    }]

    // console.log(job)

    let jobExpandedData = [{
      schedule_id: job.schedule_id,
      module: job.module,
      arguments: job.arguments,
      success: job.success,
      failure: job.failure,
    }]

    // console.log(job.seq.toString() + '-detail')

    return <Table
      columns={jobExpandedColumns}
      dataSource={jobExpandedData}
      pagination={false}
      rowKey={job.name + '-detail'}
    />
  }

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
        newDict['module'] = job.module
        newDict['interval'] = job.interval
        newDict['arguments'] = job.arguments
        newDict['start'] = job.start
        newDict['schedule_id'] = job.schedule_id
        newDict['success'] = job.success
        newDict['failure'] = job.failure
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
          expandedRowRender={this.nestedTableRendering}
          rowKey="name"
        />
      </div>
    );
  }
}

export default JobListPage;
