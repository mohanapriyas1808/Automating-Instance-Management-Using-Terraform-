import boto3

def is_dev(instance):
    is_dev = False
    if 'Tags' in instance:
        for tag in instance['Tags']:
            if tag['Key'] == 'Environment' and tag['Value'] == 'Dev':
                is_dev = True
                break
    return is_dev

def is_running(instance):
    return instance['State']['Name'] == 'running'

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='ap-south-1')
    
    try:
        response = ec2.describe_instances()
        reservations = response['Reservations']
        
        for reservation in reservations:
            for instance in reservation['Instances']:
                if is_dev(instance) and is_running(instance):
                    instance_id = instance['InstanceId']
                    ec2.stop_instances(InstanceIds=[instance_id])
                    print(f'Stopping instance: {instance_id}')
                    
    except Exception as e:
        print(f'Error stopping instances: {str(e)}')

    return {
        'statusCode': 200,
        'body': 'Function executed successfully'
    }
