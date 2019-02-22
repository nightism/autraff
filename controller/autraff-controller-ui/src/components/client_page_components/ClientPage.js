import React, { Component } from 'react';

import { Table, List, Card, Button } from 'antd';

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
    render: (text, record) => <div>
      <Button value={record.key} onClick={this.scheduleJob}>schedule</Button> 
      <Button value={record.key} onClick={this.stopJob}>stop</Button>
    </div>
  }];

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
    fetch("http://localhost:5000/connect_to_client", {
      method: "POST",
      body: JSON.stringify({
        client: this.state.client
      })
    }).then((response) => {
      return response.json()
    }).then((data) => {
      // alert(data.result)
      if (data.result === 'success') {
        this.setState({status: 'connected'})
      } else {
        this.setState({status: 'unknown'})
      }
    })
  }

  componentDidMount() {
    this.setState({'client': this.props.match.params.client})

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

      fetch("http://localhost:5000/connect_to_client", {
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
          this.setState({status: 'unknown'})
        }
      })
    })
  }

  componentDidUpdate() {
    if (this.state.client !== this.props.match.params.client) {
      this.setState({'client': this.props.match.params.client})
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

        fetch("http://localhost:5000/connect_to_client", {
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
            this.setState({status: 'unknown'})
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

        <div>
          Status: {this.state.status}
          <span style={{ padding: 10 }}></span>
          <Button onClick={this.connectToClient}>connect to this client</Button>
        </div>
        <div style={{ padding: 10 }}></div>
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
