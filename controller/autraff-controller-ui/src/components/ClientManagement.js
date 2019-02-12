import React, { Component } from 'react'

import { Layout, Menu, Breadcrumb, Icon } from 'antd';
import MenuItem from 'antd/lib/menu/MenuItem';
import 'antd/dist/antd.css';

import { BrowserRouter as Router, Route, Link } from "react-router-dom";

import ClientDashboard from './client_page_components/ClientDashboard'
import ClientPage from './client_page_components/ClientPage'

const { SubMenu } = Menu;
const { Content, Sider } = Layout;

class ClientManagement extends Component {

  state = {
    clients: [],
    clientsControl: []
  }

  componentDidMount() {
    fetch('http://localhost:5000/client', {
      method: "GET",
    }).then(results => {
      return results.json()
    }).then(data => {
      var clientMenue = data.map((client) => {
        return (<Menu.Item key={ client.ip }>
          <Link to="/client-management/127.0.0.1">{ client.ip }</Link>
        </Menu.Item>)
      })
      var clientControlMenu = data.map((client) => {
        return (<Menu.Item key={ client.ip + ".control"}>
          <Link to="/client-management/127.0.0.1">{ client.ip }</Link>
        </Menu.Item>)
      })
      this.setState({clients: clientMenue})
      this.setState({clientsControl: clientControlMenu})
    })
  }

  render() {

    return (
      <Content style={{ padding: '0 50px' }}>
        <Breadcrumb style={{ margin: '16px 0' }}>
          <Breadcrumb.Item>Home</Breadcrumb.Item>
          <Breadcrumb.Item>Client Management</Breadcrumb.Item>
        </Breadcrumb>
        <Router>
          <Layout style={{ padding: '24px 0', background: '#fff'}}>
            <Sider width={200} style={{ background: '#fff'}}>
              <Menu
                mode="inline"
                defaultSelectedKeys={['dashboard']}
                defaultOpenKeys={['sub1']}
                style={{ height: '100%'}}
              >

                <MenuItem key="dashboard">
                  <Icon type="pie-chart"/>
                  <span>Dashboard</span>
                  <Link to="/client-management/dashboard"/>
                </MenuItem>

                <SubMenu key="clients" title={<span><Icon type="laptop"/>All Clients</span>}>
                  { this.state.clients }
                </SubMenu>

                <SubMenu key="control" title={<span><Icon type="laptop" />Remote Control</span>}>
                  { this.state.clientsControl }
                  <Menu.Item key="any.control">customised</Menu.Item>
                </SubMenu>

                <MenuItem key="addclient">
                  <Icon type="plus"/>
                  <span>Add New Clients</span>
                </MenuItem>

              </Menu>
            </Sider>
            <Content style={{ padding: '0 24px', minHeight: '100%' }}>
              {/* {this.state.client} */}
              <Route exact path='/client-management/dashboard' component={ ClientDashboard } />
              <Route exact path='/client-management/127.0.0.1' component={ ClientPage } />
            </Content>
          </Layout>
        </Router>
      </Content>
    );
  }
}

// const ClientSubMenu = () => {
//   // const { name } = props;
//   return (

//     <SubMenu key="123.123.456.456" title={<span><Icon type="user" theme="twoTone" /> haha </span>}>
//       <Menu.Item key=".info">information</Menu.Item>
//       <Menu.Item key=".task">task list</Menu.Item>
//       <Menu.Item key=".report">report</Menu.Item>
//       <Menu.Item key=".control">control</Menu.Item>
//     </SubMenu>
  
//   );
// }


export default ClientManagement;
