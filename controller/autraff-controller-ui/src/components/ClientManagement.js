import React from 'react'

import { Layout, Menu, Breadcrumb, Icon } from 'antd';

import 'antd/dist/antd.css';
import MenuItem from 'antd/lib/menu/MenuItem';

const { SubMenu } = Menu;
const { Content, Sider } = Layout;

const ClientManagement = () => {
  return (
    <Content style={{ padding: '0 50px' }}>
      <Breadcrumb style={{ margin: '16px 0' }}>
        <Breadcrumb.Item>Home</Breadcrumb.Item>
        <Breadcrumb.Item>Client Management</Breadcrumb.Item>
      </Breadcrumb>
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
            </MenuItem>
            
            <SubMenu key="clients" title={<span><Icon type="laptop"/> All Clients </span>}>
              <Menu.Item key="10.0.0.4">10.0.0.4</Menu.Item>
              <Menu.Item key="10.0.0.5">10.0.0.5</Menu.Item>
              <Menu.Item key="10.0.0.6">10.0.0.6</Menu.Item>
              <Menu.Item key="10.0.0.7">10.0.0.7</Menu.Item>
            </SubMenu>

            <SubMenu key="control" title={<span><Icon type="laptop" />Remote Control</span>}>
              <Menu.Item key="10.0.0.4.control">10.0.0.4</Menu.Item>
              <Menu.Item key="10.0.0.5.control">10.0.0.5</Menu.Item>
              <Menu.Item key="10.0.0.6.control">10.0.0.6</Menu.Item>
              <Menu.Item key="10.0.0.7.control">10.0.0.7</Menu.Item>
              <Menu.Item key="any.control">customised</Menu.Item>
            </SubMenu>

          </Menu>
        </Sider>
        <Content style={{ padding: '0 24px', minHeight: '100%' }}>
          Content
        </Content>
      </Layout>
    </Content>
  );
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