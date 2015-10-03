import os
import time
from boto import ec2

def _get_ec2_connection():
    return ec2.connect_to_region("us-west-2",
                                 aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                                 aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])


def launch_instance(service,
                    instance_type,
                    ami_id='ami-c7716cf7',
                    security_group_ids=['sg-5ded7339'],
                    key_name='yi',
                    tags=None):
    if not service:
        print "Specify a service tag"
        return

    if tags and "service" in tags:
        print "Do not put 'service' in the tags dict - it should be passed separately"
        return

    conn = _get_ec2_connection()
    reservation = conn.run_instances(ami_id,
                                     key_name=key_name,
                                     instance_type=instance_type,
                                     security_group_ids=security_group_ids)

    pending_instances = reservation.instances[:]
    while len(pending_instances) > 0:
        curr_instance = pending_instances[0]
        status = curr_instance.update()
        if status == "pending":
            # Instance isn't ready yet - start from the beginning since all of the instances are being
            # prepared in parallel anyway.
            print "Waiting for instance to come online..."
            time.sleep(10)
            break
        else:
            if status == "running":
                pending_instances.pop(0)
            else:
                # Something went wrong - abort and terminate everything
                conn.terminate_instances(instance_ids=[instance.id for instance in reservation.instances])
                return

    # Now all the instances are ready, so add on some tags
    print "All instances online, adding tags"
    tags = tags or {}
    tags["service"] = service
    for instance in reservation.instances:
        instance.add_tags(tags)

def terminate_instance(service):
    if not service:
        print "Specify a service tag"
        return

    conn = _get_ec2_connection()
    reservations = conn.get_all_reservations(filters={"tag:service": service})
    instance_ids = []
    for r in reservations:
        instance_ids += [instance.id for instance in r.instances if instance.state == 'running']
    print "Terminating instances: %s" % instance_ids
    conn.terminate_instances(instance_ids=instance_ids)

