import React from 'react'

import { Layout, Menu, Icon } from 'antd';
import 'antd/dist/antd.css';

import { BrowserRouter as Router, Route, Link } from "react-router-dom";

import ClientManagement from './ClientManagement';
import JobManagement from './JobManagement';
import HomePage from './Home'

const { Header, Footer } = Layout;

const PageWrapper = () => {
  return (
    <Router>
      <Layout style={{height:"100vh"}}>
        <Header className="header">
          {/* <div className="logo" /> */}
          <div className='logo' style={{ float: 'left', maxHeight: '60px', overflow: 'hidden'}}>
            <img src={process.env.PUBLIC_URL + '/title-logo.png'} style={{ marginTop: '-42px', width: '150px', marginRight: '20px' }}/>
          </div>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['1']}
            style={{ lineHeight: '64px' }}
          >
            <Menu.Item key="1">
              <Icon type='home' />
              <span>Home</span>
              <Link to="/" />
            </Menu.Item>

            <Menu.Item key="2">
              <Icon type='laptop' />
              <span>Client Management</span>
              <Link to="/client-management/dashboard" />
            </Menu.Item>

            <Menu.Item key="3">
              <Icon type='book' />
              <span>Job Management</span>
              <Link to="/job-management/dashboard" />
            </Menu.Item>

            {/* <Menu.Item key="4">
              <span>Persona Management</span>
              <Link to="/persona-management/dashboard" />
            </Menu.Item> */}

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
        {/* <Route exact path='/persona-management/dashboard' component={PersonaManagement} /> */}


        <Footer style={{ textAlign: 'center' }}>
          Autraff ©2019 Created by SUN Mingyang
        </Footer>
      </Layout>
    
    
    </Router>
    
  );
}

export default PageWrapper;
