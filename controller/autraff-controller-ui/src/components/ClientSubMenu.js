import React from 'react'

import { Menu, Icon } from 'antd';

import 'antd/dist/antd.css';

const { SubMenu } = Menu;

const ClientSubMenu = () => {
  // const { name } = props;
  return (

    <SubMenu key="123.123.456.456" title={<span><Icon type="user" theme="twoTone" /> haha </span>}>
      <Menu.Item key=".info">information</Menu.Item>
      <Menu.Item key=".task">task list</Menu.Item>
      <Menu.Item key=".report">report</Menu.Item>
      <Menu.Item key=".control">control</Menu.Item>
    </SubMenu>
  
  );
}
    {/* <SubMenu key={ name } title={<span><Icon type="user" theme="twoTone" />{ name }</span>}>
      <Menu.Item key={ name + ".info" }>information</Menu.Item>
      <Menu.Item key={ name + ".task" }>task list</Menu.Item>
      <Menu.Item key={ name + ".report" }>report</Menu.Item>
      <Menu.Item key={ name + ".control" }>control</Menu.Item>
    </SubMenu> */}
export default ClientSubMenu;
