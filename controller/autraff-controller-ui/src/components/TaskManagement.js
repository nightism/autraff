import React from 'react'

import { Layout, Menu, Breadcrumb, Icon } from 'antd';
import MenuItem from 'antd/lib/menu/MenuItem';
import 'antd/dist/antd.css';

import { BrowserRouter as Router, Route, Link } from "react-router-dom";

const { Content, Sider } = Layout;

const TaskManagement = () => {
  return (
    <Content style={{ padding: '0 50px' }}>
      <Breadcrumb style={{ margin: '16px 0' }}>
        <Breadcrumb.Item>Home</Breadcrumb.Item>
        <Breadcrumb.Item>Task Management</Breadcrumb.Item>
      </Breadcrumb>
      <Router>
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
                <span>Task List</span>
              </MenuItem>

              <MenuItem key="addtask">
                <Icon type="plus"/>
                <span>Add Tasks</span>
              </MenuItem>

            </Menu>
          </Sider>

          <Content style={{ padding: '0 24px', minHeight: '100px' }}>
            Content
          </Content>
        </Layout>
      </Router>
    </Content>
  );
}

export default TaskManagement;
