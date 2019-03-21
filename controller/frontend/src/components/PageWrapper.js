import React from 'react'

import { Layout, Menu } from 'antd';
import 'antd/dist/antd.css';

import { BrowserRouter as Router, Route, Link } from "react-router-dom";

import ClientManagement from './ClientManagement';
import JobManagement from './JobManagement';
import PersonaManagement from './PersonaManagement'
import HomePage from './Home'

const { Header, Footer } = Layout;

const PageWrapper = () => {
  return (
    <Router>
      <Layout style={{height:"100vh"}}>
        <Header className="header">
          {/* <div className="logo" /> */}
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['1']}
            style={{ lineHeight: '64px' }}
          >
            <Menu.Item key="1">
              <span>Home</span>
              <Link to="/" />
            </Menu.Item>

            <Menu.Item key="2">
              <span>Client Management</span>
              <Link to="/client-management/dashboard" />
            </Menu.Item>

            <Menu.Item key="3">
              <span>Job Management</span>
              <Link to="/job-management/dashboard" />
            </Menu.Item>

            <Menu.Item key="4">
              <span>Persona Management</span>
              <Link to="/persona-management/dashboard" />
            </Menu.Item>

            {/* <Menu.Item key="5">
              <span>Database</span>
              <Link to="/database" />
            </Menu.Item>

            <Menu.Item key="6">
              <span>Upload</span>
              <Link to="/uoload" />
            </Menu.Item> */}

          </Menu>
        </Header>

        <Route exact path='/' component={HomePage} />
        <Route exact path='/client-management/dashboard' component={ClientManagement} />
        <Route exact path='/job-management/dashboard' component={JobManagement} />
        <Route exact path='/persona-management/dashboard' component={PersonaManagement} />


        {/* <Footer style={{ textAlign: 'center' }}>
          {/* Ant Design ©2018 Created by Ant UED */}
          {/* Autraff ©2018
        </Footer> */}
      </Layout>
    
    
    </Router>
    
  );
}

export default PageWrapper;
