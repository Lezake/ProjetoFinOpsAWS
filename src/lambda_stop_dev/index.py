import boto3

def lambda_handler(event, context):
    regiao = 'us-east-2'
    ec2 = boto3.client('ec2', region_name=regiao)
    rds = boto3.client('rds', region_name=regiao)
    asg = boto3.client('autoscaling', region_name=regiao)
    
    contadores = {'rds': 0, 'asg': 0, 'ebs_orfaos': 0}
                
    for banco in rds.describe_db_instances()['DBInstances']:
        if banco['DBInstanceIdentifier'] == 'banco-dev' and banco['DBInstanceStatus'] == 'available':
            rds.stop_db_instance(DBInstanceIdentifier=banco['DBInstanceIdentifier'])
            contadores['rds'] += 1
            
    for grupo in asg.describe_auto_scaling_groups()['AutoScalingGroups']:
        tags = {tag['Key'].lower(): tag['Value'].lower() for tag in grupo['Tags']}
        if tags.get('ambiente') == 'dev' and grupo['DesiredCapacity'] > 0:
            asg.update_auto_scaling_group(
                AutoScalingGroupName=grupo['AutoScalingGroupName'],
                MinSize=0, 
                DesiredCapacity=0
            )
            contadores['asg'] += 1
            
    filtros_ebs = [{'Name': 'status', 'Values': ['available']}]
    for volume in ec2.describe_volumes(Filters=filtros_ebs)['Volumes']:
        ec2.delete_volume(VolumeId=volume['VolumeId'])
        contadores['ebs_orfaos'] += 1
        
    detalhes = []
    if contadores['rds'] > 0:
        detalhes.append(f"{contadores['rds']} RDS parados")
    if contadores['asg'] > 0:
        detalhes.append(f"{contadores['asg']} ASGs zerados")
    if contadores['ebs_orfaos'] > 0:
        detalhes.append(f"{contadores['ebs_orfaos']} Discos deletados")
        
    if detalhes:
        relatorio = f"FinOps Executado (STOP)! Economia: " + " | ".join(detalhes) + "."
    else:
        relatorio = "FinOps Executado (STOP)! Nenhum recurso precisou ser desligado."
                 
    print(relatorio)
                 
    return {
        'statusCode': 200,
        'body': relatorio
    }