import React, { Component } from 'react'

import { Collapse, Row, Col, Button } from 'antd';
import 'antd/dist/antd.css';

class ClientLogPage extends Component{
  state = {
    usageLog: "testtest",
    driverLog: "",
  }
  render() {
    return(
      <div>
        <h1>Log - {this.props.match.params.client}</h1>
        <hr></hr>
        <Collapse defaultActiveKey={['usage', 'driver']} onChange={() => ({})}>
          <Collapse.Panel header={
            <span>
              Client Usage Log
              <span style={{ margin: "20px" }}/>
              <Button type="normal"> Retrieve From Client </Button>
              <span style={{ margin: "10px" }}/>
              <Button type="normal"shape="circle" icon="download"></Button>
            </span>
            } key="usage">
            <p>{this.state.usageLog}</p>
            <p>{this.state.usageLog}</p>
          </Collapse.Panel>
          <Collapse.Panel header={
            <span>
              Web Driver Log
              <span style={{ margin: "20px" }}/>
              <Button type="normal"> Retrieve From Client </Button>
              <span style={{ margin: "10px" }}/>
              <Button type="normal"shape="circle" icon="download"></Button>
            </span>
            } key="driver">
            <p>{this.state.driverLog}</p>
          </Collapse.Panel>
        </Collapse>
      </div>
    )
  }
}

export default ClientLogPage
