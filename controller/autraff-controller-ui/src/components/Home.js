import React, { Component } from 'react'

import { Button, Layout, Breadcrumb } from 'antd';

import 'antd/dist/antd.css';

const { Content } = Layout;

class HomePage extends Component {

  constructor(props) {
    super(props);
    this.state = {
      status: 'initialze'
    };

    // This binding is necessary to make `this` work in the callback
    this.openConnection = this.openConnection.bind(this);
  }

  openConnection() {
    fetch('http://localhost:5000/open-connection', {
      method: 'POST',
      body: JSON.stringify({
        status: 'initialize',
      })
    }).then((response) => {
      return response.json()
    }).then((data) => {
      alert(data.result)
    })
  }

  checkConnection() {
    fetch('http://localhost:5000/check-connection', {
      method: 'POST',
    }).then((response) => {
      return response.json()
    }).then((data) => {
      alert(data.result)
    })
  }

  render() {
    return (
      <Content style={{ padding: '0 50px' }}>
        <Breadcrumb style={{ margin: '16px 0' }}>
          <Breadcrumb.Item>Home</Breadcrumb.Item>
        </Breadcrumb>
        <Layout style={{ padding: '24px 0', background: '#fff'}}>
          <Content style={{ padding: '0 24px', minHeight: '100px' }}>
            <h1>WELCOME TO AUTRAFF !</h1>
            <div>
              <Button type="primary" onClick={ this.openConnection }>Open Connection</Button>
            </div>
            <div>
              <Button onClick={ this.checkConnection } >Check Client Connectivity</Button>
            </div>
            <div>
              <Button type="dashed">Shutdown Connected Clients</Button>
            </div>
            <div>
              <Button type="danger">Shutdown Connection</Button>
            </div>
          </Content>
        </Layout>
      </Content>
    );
  }
}

export default HomePage;
