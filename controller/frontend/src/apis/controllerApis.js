import { GET_NAMESERVER_CONTROLLER_INFO, OPEN_NAMESERVER_CONTROLLER_CONNECTION } from './apiLib'
import { GET_REQUEST_HEADER } from '../utils/requestHeaders'

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
    alert(data.result)
    return data
  })
}
