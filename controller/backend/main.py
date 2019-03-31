import argparse
import yaml
import service


def main():
    service.run_service()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Autraff controller backend.')
    parser.add_argument('-c', '--client', default='./template-client.yml',
                        help='client information configuration file.')
    parser.add_argument('-j', '--job', default='./template-job.yml',
                        help='job information configuration file.')

    args = parser.parse_args()

    client_conf_file = open(args.client).read()
    job_conf_file = open(args.job).read()

    client_conf = yaml.load(client_conf_file, Loader=yaml.FullLoader)
    job_conf = yaml.load(job_conf_file, Loader=yaml.FullLoader)

    service.run_service()
    service.init_backend_db(client_conf, job_conf)
