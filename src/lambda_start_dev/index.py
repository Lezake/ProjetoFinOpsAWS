import boto3

def lambda_handler(event, context):
    regiao = 'us-east-2'
    ec2 = boto3.client('ec2', region_name=regiao)
    rds = boto3.client('rds', region_name=regiao)
    asg = boto3.client('autoscaling', region_name=regiao)
    
    contadores = {'ec2': 0, 'rds': 0, 'asg': 0}
    
    filtros_ec2 = [{'Name': 'tag:ambiente', 'Values': ['dev']}]
    for reserva in ec2.describe_instances(Filters=filtros_ec2)['Reservations']:
        for inst in reserva['Instances']:
            if inst['State']['Name'] == 'stopped':
                ec2.start_instances(InstanceIds=[inst['InstanceId']])
                contadores['ec2'] += 1
                
    for banco in rds.describe_db_instances()['DBInstances']:
        if banco['DBInstanceIdentifier'] == 'banco-dev' and banco['DBInstanceStatus'] == 'stopped':
            rds.start_db_instance(DBInstanceIdentifier=banco['DBInstanceIdentifier'])
            contadores['rds'] += 1
            
    for grupo in asg.describe_auto_scaling_groups()['AutoScalingGroups']:
        tags = {tag['Key'].lower(): tag['Value'].lower() for tag in grupo['Tags']}
        if tags.get('ambiente') == 'dev' and grupo['DesiredCapacity'] == 0:
            asg.update_auto_scaling_group(
                AutoScalingGroupName=grupo['AutoScalingGroupName'],
                MinSize=1, 
                DesiredCapacity=1
            )
            contadores['asg'] += 1
            
    relatorio = (f"Ambiente INICIADO (START)! "
                 f"{contadores['ec2']} EC2 ligadas | "
                 f"{contadores['rds']} RDS ligados | "
                 f"{contadores['asg']} ASGs restaurados.")
                 
    print(relatorio)
                 
    return {
        'statusCode': 200,
        'body': relatorio
    }