# wowza-server
Scripts for managing a Wowza streaming server. This setup is intended to launch a server optimized for 
low-latency, point-to-point uses, such as video chat (as opposed to broadcast streaming).

## Installation
### Prerequisites
1. Create an AWS account with access/secret keys for an admin user. Put those keys as environment variables
named `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, respectively.
2. Create a security group for the server. Here are some example settings:
3. Create a key pair and download the private key. You will need the key to ssh into the host.

### Steps
```
$ pip install requirements/simple.txt
```

## Usage
Open an iPython shell with `ipython -i wowza_server.py`

### Launching a server
```
$ launch_instance(service="my_service",
                  instance_type="<some_ec2_instance_type>",
                  security_group_ids=['sg-foobar'],
                  key_name="my_key")
```

### Terminating a server
```
$ terminate_instance(service="my_service")
```

