import React from 'react'

import { Layout, Breadcrumb } from 'antd';

import 'antd/dist/antd.css';

const { Content } = Layout;

const HomePage = () => {
  return (
    <Content style={{ padding: '0 50px' }}>
      <Breadcrumb style={{ margin: '16px 0' }}>
        <Breadcrumb.Item>Home</Breadcrumb.Item>
      </Breadcrumb>
      <Layout style={{ padding: '24px 0', background: '#fff'}}>
        <Content style={{ padding: '0 24px', minHeight: '100px' }}>
          WELCOME TO AUTRAFF !
        </Content>
      </Layout>
    </Content>
  );
}

export default HomePage;
