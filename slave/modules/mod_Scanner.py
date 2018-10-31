"""

* tile Port Scanner Module
* author Ivo
* source Cryton v2018
* date-of-citation Oct 2018

"""

# This module has scanning capabilities using nmap
# input: target ip
# output: list of open tcp/udp ports
import nmap
import csv
import tempfile
import json


def execute(args):
    """

    This module runs an nmap scan against target host/subnet.

    Available arguments are:

    * ports: list of ports to be scanned

    * params (optional): nmap parameters

    :param args: Dictionary of mandatory sub-dictionary 'arguments' and other optional elements.
    :return ret_vals: dictionary with following values:

        * ret: 0 in success, other number in failure,

        * value: return value, usually stdout,

        * err_msg: error message, if any
    """

    ret_vals = dict(dict())
    ret_vals.update({'ret': -1})
    ret_vals.update({'value': None})
    ret_vals.update({'err_msg': None})
    ports = args.get('arguments').get('ports')
    target = args.get('target')
    if ports is None:
        ret_vals.update({'err_msg': 'Parameter "ports" needed'})
        return ret_vals

    ports_ints = ports
    ports = str(ports)

    params = args.get('arguments').get('params')
    nm = nmap.PortScanner()
    if params:
        nm.scan(hosts=target, ports=ports, arguments=params, sudo=False)
    else:
        nm.scan(hosts=target, ports=ports, sudo=False)
    tf = tempfile.NamedTemporaryFile('w', delete=False)
    out_csv = nm.csv()
    tf.writelines(out_csv)
    tf.close()
    csv_f = open(tf.name, 'r')
    scan_dict = csv.DictReader(csv_f, delimiter=';')

    ports_out = list()
    value = list()

    for row in scan_dict:
        if row['state'] == 'open':
            ports_out.append(int(row['port']))

        value = ports_out

        ret_vals.update({'ret': 0, 'value': json.dumps(value).replace("'", r"\'")})

    if ports is not None:

        if all(x in ports_out for x in ports_ints):
            ret = 0
        else:
            ret = -1
        ret_vals.update({'ret': ret})

    if params:
        extra = out_csv
        value.append(extra)

        ret_vals.update({'value': json.dumps(value)})
    return ret_vals


# unit test for mod_Scanner
# author Mingyang
if __name__ == "__main__":
    args = {
        'arguments': {'ports': [22]},
        'target': '127.0.0.1'
    }
    print(execute(args))
