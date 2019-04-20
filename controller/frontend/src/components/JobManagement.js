import React from 'react'

import { Layout, Menu, Breadcrumb, Icon } from 'antd';
import MenuItem from 'antd/lib/menu/MenuItem';
import 'antd/dist/antd.css';

import { BrowserRouter as Router, Route, Link, Switch, Redirect } from "react-router-dom";

import JobDashboard from './job_page_components/JobDashboard'
import JobListPage from './job_page_components/JobListPage'

const { Content, Sider } = Layout;

const JobManagement = () => {
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
                <Link to="/job-management/dashboard"/>
              </MenuItem>

              <MenuItem key="joblist">
                <Icon type="align-left"/>
                <span>Job List</span>
                <Link to="/job-management/task-list-page"/>
              </MenuItem>

              <MenuItem key="addjob" disabled>
                <Icon type="plus"/>
                <span>Add Jobs</span>
              </MenuItem>

            </Menu>
          </Sider>

          <Content style={{ padding: '0 24px', minHeight: '100px' }}>
            <Switch>
              <Route exact path='/job-management/dashboard' component={JobDashboard} />
              <Route exact path='/job-management/task-list-page' component={JobListPage} />
              <Redirect path='/job-management' to='/job-management/dashboard' />
            </Switch>
          </Content>
        </Layout>
      </Router>
    </Content>
  );
}

export default JobManagement;
