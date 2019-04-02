import React, { Component } from 'react';

import { Table, List, Card, Button, Icon } from 'antd';

class ClientPage extends Component {
  state = {
    client: '',
    jobInfo: [
    ],
    status: 'unknown'
  };

  constructor(props) {
    super(props)
    this.connectToClient = this.connectToClient.bind(this)
    this.scheduleJob = this.scheduleJob.bind(this)
    this.stopJob = this.stopJob.bind(this)
    this.updateTable = this.updateTable.bind(this)
  }

  jobInfoColumns = [{
    title: 'Name',
    dataIndex: 'name',
  }, {
    title: 'Schedule ID',
    dataIndex: 'schedule_id',
  }, {
    title: 'Module',
    dataIndex: 'module',
  }, {
    title: 'Interval (seconds)',
    dataIndex: 'interval',
  }, {
    title: 'Start Time',
    dataIndex: 'start'
  }, {
    title: 'Actions',
    render: (text, record) => <div style={{ textAlign: 'center' }}>
      <Button type="primary" value={record.key} onClick={this.scheduleJob}>schedule</Button>
      <span style={{ padding: 10 }}></span>
      <Button type="danger" value={record.key} onClick={this.stopJob}>stop</Button>
    </div>
  }];

  generateStatusIcon(status) {
    if (status === 'connecting')
      return (<Icon type="sync" spin/>)
    else if (status === 'connected')
      return (<Icon type="check-circle" theme='twoTone' twoToneColor="#52c41a"/>)
    else
      return (<Icon type="close-circle" theme='twoTone' twoToneColor="#ff0000"/>)
  }

  scheduleJob(e){
    console.log('scheduling')
    fetch("http://localhost:5000/job/" + e.target.value + "/detail", {
      method: "GET",
    }).then((response) => {
      return response.json()
    }).then((targetJob) => {
      if (targetJob.schedule_id !== null && targetJob.schedule_id !== "") {
        alert("This job is already running.")
        alert(targetJob.schedule_id)
        console.log(targetJob.schedule_id)
        return
      }
      var schedule_request = {
        "connection_name": targetJob.client + "_tcp_channel",
        "module": targetJob.module,
        "interval": targetJob.interval,
        "para": targetJob.arguments,
        "command": 'schedule_task',
      }
      fetch("http://localhost:5000/schedule-job", {
        method: "POST",
        body: JSON.stringify(schedule_request)
      }).then((response) => {
        return response.json()
      }).then((scheduling) => {
        console.log(scheduling.schedule_id)
        fetch("http://localhost:5000/job/schedule/" + targetJob.seq, {
          method: "POST",
          body: JSON.stringify({
            schedule_id: scheduling.schedule_id
          }),
        }).then((response) => {
          return response.json()
        }).then((data) => {
          alert("Job scheduled!")
          this.updateTable()
        })
      })
    })
  }

  stopJob(e) {
    console.log('stopping')
    fetch("http://localhost:5000/job/" + e.target.value + "/detail", {
      method: "GET",
    }).then((response) => {
      return response.json()
    }).then((targetJob) => {
      if (targetJob.schedule_id === null || targetJob.schedule_id === "") {
        alert("This job is not running.")
        return
      }
      var schedule_request = {
        "connection_name": targetJob.client + "_tcp_channel",
        "command": 'delete_task',
        "job_schedule_id": targetJob.schedule_id,
      }
      fetch("http://localhost:5000/stop-job", {
        method: "POST",
        body: JSON.stringify(schedule_request)
      }).then((response) => {
        return response.json()
      }).then((data) => {
        // if (data.result !== "DEL") {
        //   alert('fail!')
        // } else {
        fetch("http://localhost:5000/job/schedule/" + targetJob.seq, {
          method: "POST",
          body: JSON.stringify({
            schedule_id: ""
          }),
        }).then((response) => {
          return response.json()
        }).then((data) => {
          alert("Job stopped.")
          this.updateTable()
        })
        // }
      })
    })
  }

  updateTable() {
    fetch("http://localhost:5000/job/" + this.props.match.params.client, {
      method: "GET"
    }).then((response) => {
      return response.json()
    }).then((data) => {
      var jobList = data.map((job) => {
        var jobDict = {
          key: job.seq,
          schedule_id: job.schedule_id,
          name: job.name,
          module: job.module,
          interval: job.interval,
          start: job.start,
        }
        return jobDict
      })
      this.setState({'jobInfo': jobList})
    })
  }

  connectToClient() {
    // console.log(this.state.client)
    this.setState({status: 'connecting'})

    fetch("http://localhost:5000/connect-to-client", {
      method: "POST",
      body: JSON.stringify({
        client: this.state.client
      })
    }).then((response) => {
      return response.json()
    }).then((data) => {
      alert(data.result)
      if (data.result === 'success') {
        this.setState({status: 'connected'})
      } else {
        this.setState({status: 'disconnected'})
      }
    })
  }

  componentDidMount() {
    this.setState({'client': this.props.match.params.client})
    this.setState({status: 'connecting'})

    fetch("http://localhost:5000/job/" + this.props.match.params.client, {
      method: "GET"
    }).then((response) => {
      return response.json()
    }).then((data) => {
      var jobList = data.map((job) => {
        var jobDict = {
          key: job.seq,
          schedule_id: job.schedule_id,
          name: job.name,
          module: job.module,
          interval: job.interval,
          start: job.start,
        }
        return jobDict
      })
      this.setState({'jobInfo': jobList})

      fetch("http://localhost:5000/connect-to-client", {
        method: "POST",
        body: JSON.stringify({
          client: this.props.match.params.client
        })
      }).then((response) => {
        return response.json()
      }).then((data) => {
        // alert(data.result)
        if (data.result === 'success') {
          this.setState({status: 'connected'})
        } else {
          this.setState({status: 'disconnected'})
        }
      })
    })
  }

  // TODO too many repeated code here
  componentDidUpdate() {
    if (this.state.client !== this.props.match.params.client) {
      this.setState({'client': this.props.match.params.client})
      this.setState({status: 'connecting'})

      fetch("http://localhost:5000/job/" + this.props.match.params.client, {
        method: "GET"
      }).then((response) => {
        return response.json()
      }).then((data) => {
        var jobList = data.map((job) => {
          var jobDict = {
            key: job.seq,
            schedule_id: job.schedule_id,
            name: job.name,
            module: job.module,
            interval: job.interval,
            start: job.start,
          }
          return jobDict
        })
        this.setState({'jobInfo': jobList})

        fetch("http://localhost:5000/connect-to-client", {
          method: "POST",
          body: JSON.stringify({
            client: this.props.match.params.client
          })
        }).then((response) => {
          return response.json()
        }).then((data) => {
          // alert(data.result)
          if (data.result === 'success') {
            this.setState({status: 'connected'})
          } else {
            this.setState({status: 'disconnected'})
          }
        })
      })
    }

  }

  render() {
    return (
      <div>
        <h1>{this.props.match.params.client}</h1>
        <hr></hr>

        <div style={{ fontSize: 20, marginBottom: 20, marginTop: 20}}>
          Status: {this.state.status}
          <span style={{ margin: 5 }}></span>
          <span>
            {this.generateStatusIcon(this.state.status)}
          </span>
          <span style={{ margin: 10 }}></span>
          <Button onClick={this.connectToClient} ghost type="primary">Refresh Client Connection Status</Button>
          <span style={{ margin: 10 }}></span>
          <Button onClick={(e) => { alert('Coming soon!') }} ghost type="primary">Refresh Client Schedule Status</Button>
        </div>
        <div style={{ margin: 10 }}></div>
        <Table
          bordered
          columns={this.jobInfoColumns}
          dataSource={this.state.jobInfo}
          rowKey="key"
        />
      </div>
    );
  }
}

export default ClientPage;
