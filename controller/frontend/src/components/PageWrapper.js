import React from 'react'

import { Layout, Menu, Icon } from 'antd';
import 'antd/dist/antd.css';

import { BrowserRouter as Router, Route, Link, Switch } from "react-router-dom";

import ClientManagement from './ClientManagement';
import JobManagement from './JobManagement';
import HomePage from './Home'

const { Header, Footer } = Layout;
const { Content } = Layout;

const PageWrapper = () => {
  return (
    <Router>
      <Layout style={{ minHeight:"100vh" }}>
        {/* TODO  display issue when resizing the window becomes (e.g. when the height becomes shorter) */}
        <Header className="header">
          {/* <div className="logo" /> */}
          <div className='logo' style={{ float: 'left', maxHeight: '60px', overflow: 'hidden'}}>
            <img
              src={process.env.PUBLIC_URL + '/title-logo.png'}
              style={{ marginTop: '-42px', width: '150px', marginRight: '20px' }}
              alt="logo"
            />
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
              <span>Database</span>
              <Link to="/database" />
            </Menu.Item>

            <Menu.Item key="5">
              <span>Upload</span>
              <Link to="/uoload" />
            </Menu.Item> */}

          </Menu>
        </Header>

        {/* TODO Layout and Breadcrumb should be in this level, in Page Wrapper level */}

        <Switch>
          <Route exact path='/' component={HomePage} />
          <Route path='/client-management/' component={ClientManagement} />
          <Route path='/job-management/' component={JobManagement} />
          <Route render={() => {
              return <Content style={{ textAlign: 'center', padding: '50px' }}>
                <img
                  src={process.env.PUBLIC_URL + '/title-logo.png'}
                  style={{ width: '200px',
                           backgroundColor: 'black',
                           margin: '20px'}}
                  alt="logo"
                />
                <h1>Page Not Found</h1>
              </Content>
            }}
          />
        </Switch>

        <Footer style={{ textAlign: 'center' }}>
          Autraff ©2019 Created by SUN Mingyang
        </Footer>
      </Layout>


    </Router>

  );
}

export default PageWrapper;
