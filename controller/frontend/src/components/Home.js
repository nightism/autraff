import React, { Component } from 'react'

import { Button, Layout, Breadcrumb, Row, Col, Card } from 'antd';

import 'antd/dist/antd.css';

const { Content } = Layout;

class HomePage extends Component {

  constructor(props) {
    super(props);
    this.state = {
      status: 'initialze',
      nameserverAddr: 'test addr',
      controllerAlias: 'backend',
      serviceUpTime: '1 hour',
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
        <Layout style={{ padding: '24px 0', background: '#fff', textAlign: 'center'}}>
          
          <Content style={{ padding: '0 24px', minHeight: '100px' }}>
            <h1>WELCOME TO AUTRAFF !</h1>
            <hr style={{ margin: '20px' }}></hr>
            <Row span={12} gutter={30} style={{ margin: '10px' }}>
              <Col span={1} />
              <Col span={7}>
                <Card
                  style={{ margin: '20px' }}
                  title="Nameserver Address"
                >
                  {this.state.nameserverAddr}
                </Card>
                <Card
                  style={{ margin: '20px' }}
                  title="Controller Alias"
                >
                  {this.state.controllerAlias}
                </Card>
                <Card
                  style={{ margin: '20px' }}
                  title="Service Uptime"
                >
                  {this.state.serviceUpTime}
                </Card>
              </Col>
              <Col span={15} style={{ textAlign: 'left', paddingTop: '40px' }}>
                <h2>To run and connect to the nameserver:</h2>
                <Button type="primary" onClick={ this.openConnection }>Connect to Nameserver</Button>
                <div style={{ margin: '20px' }}></div>
                <h2>To check the status of nameserver:</h2>
                <Button onClick={ this.checkConnection } >Check Nameserver Status</Button>
                <div style={{ margin: '20px' }}></div>
                <h2>To shutdown all clients running on nameserver remotely:</h2>
                <Button type="dashed">Shutdown Connected Clients</Button>
                <div style={{ margin: '20px' }}></div>
                <h2>To shutdown the nameserver:</h2>
                <Button type="danger">Shutdown Connection</Button>
              </Col>
              <Col span={1} />
            </Row>
          </Content>
        </Layout>
      </Content>
    );
  }
}

export default HomePage;
