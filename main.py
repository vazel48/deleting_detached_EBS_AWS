import boto3
import time
import datetime

'''This script is designed for AWS Lambda to automate the deletion of detached EBS volumes 
older than 5 days (432000 seconds)'''


def lambda_handler(event, context):
    # Get the current time in epoch format
    current_epoch = time.time()

    # Initialize boto3 EC2 resource
    ec2 = boto3.resource('ec2')

    # Counter for tracking the number of volumes deleted
    volumes_deleted = 0

    # Iterate over all volumes
    for volume in ec2.volumes.all():
        # Check if the volume has tags and is not in use
        if volume.tags is not None and volume.state != 'in-use':
            for tag in volume.tags:
                # Check for 'DETACH_TIMESTAMP' tag
                if tag['Key'] == 'DETACH_TIMESTAMP':
                    # Extract the detachment date and convert it to epoch
                    detach_date = tag['Value'][0:10].replace("-", "/")
                    detach_timestamp = time.mktime(datetime.datetime.strptime(detach_date, "%Y/%m/%d").timetuple())

                    # Check if the volume was detached more than 5 days ago
                    if current_epoch - detach_timestamp > 432000:
                        # Log and delete the volume
                        print(f"EBS Volume to delete: {volume.id}")
                        volume.delete()
                        volumes_deleted += 1

    print(f"{volumes_deleted} volume(s) have been deleted")

    return 'All old volumes have been deleted!'
