import boto3

def lambda_handler(event, context):
    regiao = 'us-east-2'
    rds = boto3.client('rds', region_name=regiao)
    asg = boto3.client('autoscaling', region_name=regiao)
    
    contadores = {'rds': 0, 'asg': 0}
                
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
            
    detalhes = []
    if contadores['rds'] > 0:
        detalhes.append(f"{contadores['rds']} RDS ligados")
    if contadores['asg'] > 0:
        detalhes.append(f"{contadores['asg']} ASGs restaurados")
        
    if detalhes:
        relatorio = f"Ambiente INICIADO (START)! " + " | ".join(detalhes) + "."
    else:
        relatorio = "Ambiente INICIADO (START)! Nenhum recurso precisou ser alterado."
                 
    print(relatorio)
                 
    return {
        'statusCode': 200,
        'body': relatorio
    }