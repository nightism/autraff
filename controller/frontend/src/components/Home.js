import React, { Component } from 'react'

import { Button, Layout, Breadcrumb, Row, Col, Card, Alert } from 'antd';

import 'antd/dist/antd.css';
import { getNameserverAndControllerInfo, connectToNameserverAndController } from '../apis/controllerApis';
import { CHECK_NAMESERVER_STATUS, CONNECT_TO_ALL_CLIENTS } from '../apis/apiLib';

const { Content } = Layout;

class HomePage extends Component {

  constructor(props) {
    super(props);
    this.state = {
      status: 'initialze', // TODO useless state
      nameserverAddr: '',
      controllerAlias: '',
      serviceUpTime: 'UNKOWN',
      alertDisplay: {
        style: { display: 'None' }
      },
      loading: {
        connectAllClients: false,
      }
    };

    // This binding is necessary to make `this` work in the callback
    this.openConnection = this.openConnection.bind(this)
    this.connectToAllClients = this.connectToAllClients.bind(this)
  }

  openConnection() {
    connectToNameserverAndController().then(data => {
      let alertDisplay = { display: 'None' }
      if (data.controller === '' && data.nameserverAddr === '') {
        alertDisplay = {}
      }
      this.setState({
        controllerAlias: data.controller,
        nameserverAddr: data.nameserver,
        serviceUpTime: 'UNKOWN',
        alertDisplay: alertDisplay,
      })
    })
  }

  checkConnection() {
    fetch(CHECK_NAMESERVER_STATUS, {
      method: 'POST',
    }).then((response) => {
      return response.json()
    }).then((data) => {
      alert(data.result)
    })
  }

  connectToAllClients() {
    this.setState({
      loading: Object.assign({}, this.state.loading, {
        connectAllClients: true
      })
    })
    fetch(CONNECT_TO_ALL_CLIENTS, {
      method: 'POST',
    }).then((response) => {
      return response.json()
    }).then((data) => {
      alert(data.result)
      this.setState({
        loading: Object.assign({}, this.state.loading, {
          connectAllClients: false
        })
      })
    })
  }

  shutdownAllClients() {
    alert('Coming soon!')
  }

  shutdownNameserver() {
    alert('Coming soon!')
  }

  componentDidMount() {
    getNameserverAndControllerInfo().then(data => {
      let alertDisplay = { display: 'None' }
      if (data.controller === '' && data.nameserverAddr === '') {
        alertDisplay = {}
      }
      this.setState({
        controllerAlias: data.controller,
        nameserverAddr: data.nameserver,
        serviceUpTime: 'UNKOWN',
        alertDisplay: alertDisplay,
      })
    })
  }

  render() {
    return (
      <Content style={{ padding: '0 50px' }}>
        <Breadcrumb style={{ margin: '16px 0' }}>
          <Breadcrumb.Item>Home</Breadcrumb.Item>
        </Breadcrumb>
        <Layout style={{ padding: '24px 0', background: '#fff', textAlign: 'center' }}>

          <Content style={{ padding: '0 24px', minHeight: '100px' }}>
            <h1>WELCOME TO AUTRAFF !</h1>
            <hr style={{ margin: '20px' }}></hr>
            <Alert
              message="Nameserver or Controller backend is not connected/running."
              description="Please see the instructions below to start Autraff service."
              type="warning"
              showIcon
              style={{ margin: '0 100px', textAlign: 'left', ...this.state.alertDisplay }}
            />
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
                <Col span={12}>
                  <h2>To run and connect to the nameserver:</h2>
                  <Button type="primary" onClick={ this.openConnection }>Connect to Nameserver</Button>
                  <div style={{ margin: '20px' }}></div>
                </Col>

                <Col span={12}>
                  <h2>To check the status of nameserver:</h2>
                  <Button onClick={ this.checkConnection } >Refresh Nameserver Status</Button>
                  <div style={{ margin: '20px' }}></div>
                </Col>

                <Col span={24}>
                  <h2>To establish communication channels for all clients:</h2>
                  <Button
                    type="primary"
                    onClick={ this.connectToAllClients }
                    loading={this.state.loading.connectAllClients}
                  >
                    Connect to All Clients
                  </Button>
                  <div style={{ margin: '20px' }}></div>
                </Col>

                <Col span={24}>
                  <h2>To shutdown all clients running on nameserver remotely:</h2>
                  <Button type="danger" onClick={ this.shutdownAllClients }>Shutdown Connected Clients</Button>
                  <div style={{ margin: '20px' }}></div>
                </Col>

                <Col span={24}>
                  <h2>To shutdown the nameserver and all connected clients:</h2>
                  <Button type="danger" onClick={ this.shutdownNameserver }>Shutdown Connection</Button>
                </Col>
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
