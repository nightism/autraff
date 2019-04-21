import React, { Component } from 'react'

import {
  Collapse,
  Button,
  message,
  Tooltip
} from 'antd';
import 'antd/dist/antd.css';

import { GET_REQUEST_HEADER, POST_REQUEST_HEADER } from '../../utils/requestHeaders'
import { LOG_USAGE_LOG, CONNECT_TO_CLIENT, LOG_DRIVER_LOG } from '../../apis/apiLib';

class ClientLogPage extends Component{
  state = {
    client: "",
    usageLog: [],
    usageLogDisplay: "",
    driverLog: [],
    driverLogDisplay: "",

    usageLoading: false,
    driverLoading: false,
  }

  constructor(props) {
    super(props)
    this.connectToClient = this.connectToClient.bind(this)
    this.downloadUsageLog = this.downloadUsageLog.bind(this)
    this.downloadDriverLog = this.downloadDriverLog.bind(this)
    this.fetchUsageLog = this.fetchUsageLog.bind(this)
    this.fetchDriverLog = this.fetchDriverLog.bind(this)
  }

  connectToClient() {
    return fetch(CONNECT_TO_CLIENT, {
      ...POST_REQUEST_HEADER,
      body: JSON.stringify({
        client: this.props.match.params.client
      })
    }).then((response) => {
      return response.json()
    }).then((data) => {
      if (data.result === 'success') {
        return 0
      } else {
        return 1
      }
    })
  }

  downloadUsageLog = () => {
    const element = document.createElement("a");
    const file = new Blob([this.state.usageLog], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = this.props.match.params.client + ".usage.log";
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  }

  downloadDriverLog = () => {
    const element = document.createElement("a");
    const file = new Blob([this.state.driverLog], {type: 'text/plain'});
    element.href = URL.createObjectURL(file);
    element.download = this.props.match.params.client + ".driver.log";
    document.body.appendChild(element); // Required for this to work in FireFox
    element.click();
  }

  fetchUsageLog(e) {
    this.setState({ usageLoading: true })
    this.connectToClient().then((rc) => {
      if (rc === 0) {
        message.success('Connected to client.')
        fetch(LOG_USAGE_LOG + this.props.match.params.client, {
          ...GET_REQUEST_HEADER
        }).then((response) => {
          return response.json()
        }).then((data) => {
          let usageLog = data['usage_log']
          this.setState({
            usageLog: usageLog.join('\n'),
            usageLogDisplay: usageLog.slice(-20).map((line, index) => {
              return <p key={index}>{line}</p>
            })
          })
        })
        message.success('Usage Log retrieved.')
      } else {
        message.error('Cannot connect to client, log fetching failed.')
      }
    }).then(() => {
      this.setState({ usageLoading: false })
    })
  }

  fetchDriverLog(e) {
    this.setState({ driverLoading: true })
    this.connectToClient().then((rc) => {
      if (rc === 0) {
        message.success('Connected to client.')
        fetch(LOG_DRIVER_LOG + this.props.match.params.client, {
          ...GET_REQUEST_HEADER
        }).then((response) => {
          return response.json()
        }).then((data) => {
          let driverLog = data['driver_log']
          this.setState({
            driverLog: driverLog.join('\n'),
            driverLogDisplay: driverLog.slice(-20).map((line, index) => {
              return <p key={index}>{line}</p>
            })
          })
        })
        message.success('Driver Log retrieved.')
      } else {
        message.error('Cannot connect to client, log fetching failed.')
      }
    }).then(() => {
      this.setState({ driverLoading: false })
    })
  }

  componentDidMount() {
    this.setState({
      client: this.props.match.params.client,
      usageLog: [],
      usageLogDisplay: "",
      driverLog: [],
      driverLogDisplay: "",

      usageLoading: false,
      driverLoading: false,
    })
  }

  componentDidUpdate() {
    if (this.state.client !== this.props.match.params.client) {
      this.setState({
        client: this.props.match.params.client,
        usageLog: [],
        usageLogDisplay: "",
        driverLog: [],
        driverLogDisplay: "",

        usageLoading: false,
        driverLoading: false,
      })
    }
  }

  render() {
    return(
      <div>
        <h1>Log - {this.props.match.params.client}</h1>
        <hr></hr>
        <Collapse activeKey={['usage', 'driver']} onChange={() => ({})}>
          <Collapse.Panel header={
            <span>
              Client Usage Log
              <span style={{ margin: "20px" }}/>
              <Button
                type="normal"
                loading={this.state.usageLoading}
                onClick={this.fetchUsageLog}
              >
                Retrieve From Client
              </Button>
              <span style={{ margin: "10px" }}/>
              <Tooltip title="download full log">
                <Button
                  type="normal"
                  shape="circle"
                  icon="download"
                  onClick={this.downloadUsageLog}
                />
              </Tooltip>
            </span>
            }
            key="usage"
            showArrow={false}
          >
              {this.state.usageLogDisplay}
          </Collapse.Panel>
          <Collapse.Panel header={
            <span>
              Web Driver Log
              <span style={{ margin: "20px" }}/>
              <Button
                type="normal"
                loading={this.driverLoading}
                onClick={this.fetchDriverLog}
              >
                Retrieve From Client
              </Button>
              <span style={{ margin: "10px" }}/>
              <Tooltip title="download full log">
                <Button
                  type="normal"
                  shape="circle"
                  icon="download"
                  onClick={this.downloadDriverLog}
                />
              </Tooltip>
            </span>
            } key="driver"
            showArrow={false}
          >
              {this.state.driverLogDisplay}
          </Collapse.Panel>
        </Collapse>
      </div>
    )
  }
}

export default ClientLogPage
