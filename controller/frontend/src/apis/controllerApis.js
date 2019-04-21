import { GET_NAMESERVER_CONTROLLER_INFO, OPEN_NAMESERVER_CONTROLLER_CONNECTION } from './apiLib'
import { GET_REQUEST_HEADER } from '../utils/requestHeaders'

import { message } from 'antd'

export function getNameserverAndControllerInfo() {
  return fetch(
    GET_NAMESERVER_CONTROLLER_INFO,
    {
      ...GET_REQUEST_HEADER,
    }
  ).then(response => {
    return response.json()
  }).then(data => {
    return data
  })
}

export function connectToNameserverAndController() {
  return fetch(
    OPEN_NAMESERVER_CONTROLLER_CONNECTION,
    {
      ...GET_REQUEST_HEADER,
    }
  ).then((response) => {
    return response.json()
  }).then((data) => {
    if (data.result === 'success') {
      message.success('nameserver and controller is running.')
    } else {
      message.error(data.result)
    }
    return data
  })
}
