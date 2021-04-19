import boto3
import json
import time
import threading
import concurrent.futures
from botocore.config import Config

class AwsInstances():
    '''Queries the configured aws account using aws sdk to list all the instances per region'''

    def __init__(self):
        '''Creates a list of avaliable/enabled regions with ec2 support'''
        ec2 = boto3.client('ec2')
        response = ec2.describe_regions()
        self.instance_dict = {i['RegionName']:{} for i in response['Regions']}

        # threading makes all the api calls at once or close to togeather so its faster
        self.parallelize2()

    def get_instances_in_region(self, region_aws_name):
        '''gets the instances in a specific region and the total number of instances in a region and writes it to the instance_dict'''
        my_config = Config( region_name = region_aws_name)
        ec2_region = boto3.client('ec2', config=my_config)
        response = ec2_region.describe_instances()
        try:
            instance_ids = [instance['Instances'][0]['InstanceId'] for instance in response['Reservations']]
            self.instance_dict[region_aws_name] = {'instanceIDs': instance_ids, 'totalInstances': len(instance_ids)}
        except IndexError:
            self.instance_dict[region_aws_name] = {}
    
    def parallelize(self):
        ''' old method of paralleizing runs all api calls at in parallel '''
        threads = []
        for region in self.instance_dict.keys():
            t = threading.Thread(target = self.get_instances_in_region, args = [region])
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()

    def parallelize2(self):
        ''' newer metheod of threading using thread pools runs all api calls at in parallel '''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.get_instances_in_region, self.instance_dict.keys())

# Lambda handler , this is called by the api gateway when there is an event
def lambda_handler(event, context):

    instance_list = AwsInstances()
    return {
        'statusCode': 200,
        'body': json.dumps(instance_list.instance_dict)
    }