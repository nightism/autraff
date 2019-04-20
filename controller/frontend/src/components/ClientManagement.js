import React, { Component } from 'react'

import { Layout, Menu, Breadcrumb, Icon } from 'antd';
import MenuItem from 'antd/lib/menu/MenuItem';
import 'antd/dist/antd.css';

import { BrowserRouter as Router, Route, Link, Switch, Redirect } from "react-router-dom";

import ClientDashboard from './client_page_components/ClientDashboard'
import ClientPage from './client_page_components/ClientPage'
import ClientLogPage from './client_page_components/ClientLogPage'
import { DB_CLIENT_API } from '../apis/apiLib';

const { SubMenu } = Menu;
const { Content, Sider } = Layout;

class ClientManagement extends Component {

  state = {
    clients: [],
    clientsLogs: [],
    clientsControl: []
  }

  componentDidMount() {
    fetch(DB_CLIENT_API, {
      method: "GET",
    }).then(results => {
      return results.json()
    }).then(data => {
      var clientMenue = data.map((client) => {
        return (<Menu.Item key={ client.ip }>
          <Link to={"/client-management/" + client.ip + "/detail"}>{client.ip}</Link>
        </Menu.Item>)
      })

      var clientLogs = data.map((client) => {
        return (<Menu.Item key={ client.ip + '.log' }>
          <Link to={"/client-management/" + client.ip + "/log"}>{client.ip}</Link>
        </Menu.Item>)
      })

      var clientControlMenu = data.map((client) => {
        return (<Menu.Item key={ client.ip + ".control"} disabled>
          {/* TODO to be developed */}
          <Link to={"/client-control/" + client.ip}>{client.ip}</Link>
        </Menu.Item>)
      })
      this.setState({clients: clientMenue})
      this.setState({clientsLogs: clientLogs})
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

                <SubMenu key="log" title={<span><Icon type="file-text" />Retrieve Logs</span>}>
                  { this.state.clientsLogs }
                </SubMenu>

                <SubMenu key="control" title={<span><Icon type="robot" />Remote Control</span>}>
                  { this.state.clientsControl }
                  <Menu.Item key="any.control" disabled>any connect</Menu.Item>
                </SubMenu>

                <MenuItem key="addclient" disabled>
                  <Icon type="plus"/>
                  <span>Add New Clients</span>
                </MenuItem>

              </Menu>
            </Sider>
            <Content style={{ padding: '0 24px', minHeight: '100%' }}>
              {/* {this.state.client} */}
              <Switch>
                <Route exact path='/client-management/dashboard' component={ ClientDashboard } />
                <Route exact path='/client-management/:client/detail' component={ ClientPage } />
                <Route exact path='/client-management/:client/log' component={ ClientLogPage } />
                <Redirect path='/client-management' to='/client-management/dashboard' />
              </Switch>
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
//
//   );
// }


export default ClientManagement;
