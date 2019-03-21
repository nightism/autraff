import React from 'react'

import { Layout, Menu, Breadcrumb, Icon } from 'antd';

import 'antd/dist/antd.css';
import MenuItem from 'antd/lib/menu/MenuItem';

const { Content, Sider } = Layout;

const PersonaManagement = () => {
  return (
    <Content style={{ padding: '0 50px' }}>
      <Breadcrumb style={{ margin: '16px 0' }}>
        <Breadcrumb.Item>Home</Breadcrumb.Item>
        <Breadcrumb.Item>Persona Management</Breadcrumb.Item>
      </Breadcrumb>
      <Layout style={{ padding: '24px 0', background: '#fff'}}>
        <Sider width={200} style={{ background: '#fff'}}>
          <Menu
            mode="inline"
            defaultSelectedKeys={['dashboard']}
            style={{ height: '100%'}}
          >

            <MenuItem key="dashboard">
              <Icon type="pie-chart"/>
              <span>Dashboard</span>
            </MenuItem>

            <MenuItem key="tasklist">
              <Icon type="align-left"/>
              <span>Persona List</span>
            </MenuItem>

            <MenuItem key="addtask">
              <Icon type="plus"/>
              <span>Add Personas</span>
            </MenuItem>

          </Menu>
        </Sider>
        <Content style={{ padding: '0 24px', minHeight: '100px' }}>
          Content
        </Content>
      </Layout>
    </Content>
  );
}

export default PersonaManagement;
