import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

table_agendamentos = dynamodb.Table('Agendamentos')
TOPICO_SNS_ARN = "arn:aws:sns:us-east-1:123456789012:NotificarMedico"  # Substitua pelo seu ARN

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        profissional = body['profissional']
        especialidade = body['especialidade']
        horario = body['horario']
        nome_pet = body['pet']
        dono = body['dono']

        # Salvar no DynamoDB
        table_agendamentos.put_item(
            Item={
                'profissional': profissional,
                'horario': horario,
                'especialidade': especialidade,
                'pet': nome_pet,
                'dono': dono,
                'timestamp': datetime.utcnow().isoformat()
            }
        )

        # Notificar médico via SNS
        mensagem = (
            f"Novo agendamento!\n"
            f"Profissional: {profissional}\n"
            f"Especialidade: {especialidade}\n"
            f"Horário: {horario}\n"
            f"Pet: {nome_pet}\n"
            f"Dono: {dono}"
        )

        sns.publish(
            TopicArn=TOPICO_SNS_ARN,
            Message=mensagem,
            Subject="Novo agendamento para consulta de pet"
        )

        return {"statusCode": 201, "body": json.dumps({"mensagem": "Agendamento criado e médico notificado"})}

    except Exception as e:
        print("Erro:", e)
        return {"statusCode": 500, "body": json.dumps({"erro": str(e)})}
