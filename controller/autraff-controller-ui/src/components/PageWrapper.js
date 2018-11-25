import React from 'react'

import { Layout, Menu } from 'antd';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

import 'antd/dist/antd.css';
import ClientManagement from './ClientMangement';

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
              <Link to="/client-management" />
            </Menu.Item>

            <Menu.Item key="3">
              <span>Task Management</span>
              <Link to="/task-management" />
            </Menu.Item>

            <Menu.Item key="4">
              <span>Database Management</span>
              <Link to="/database-management" />
            </Menu.Item>

            <Menu.Item key="5">
              <span>Upload</span>
              <Link to="/uoload" />
            </Menu.Item>

          </Menu>
        </Header>


        <Route exact path='/client-management' component={ClientManagement} />

        <Footer style={{ textAlign: 'center' }}>
          {/* Ant Design ©2018 Created by Ant UED */}
          Autraff ©2018
        </Footer>
      </Layout>
    
    
    </Router>
    
  );
}

export default PageWrapper;
