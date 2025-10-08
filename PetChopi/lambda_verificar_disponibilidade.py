import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_profissionais = dynamodb.Table('Profissionais')
table_agendamentos = dynamodb.Table('Agendamentos')

def lambda_handler(event, context):
    try:
        especialidade = event['queryStringParameters']['especialidade']
        profissional = event['queryStringParameters']['profissional']

        # Busca horários disponíveis do profissional
        prof_data = table_profissionais.get_item(Key={'nome': profissional})
        if 'Item' not in prof_data:
            return {"statusCode": 404, "body": json.dumps({"erro": "Profissional não encontrado"})}

        horarios = prof_data['Item'].get('horarios', [])

        # Busca horários já agendados
        agendamentos = table_agendamentos.query(
            KeyConditionExpression=Key('profissional').eq(profissional)
        )['Items']

        ocupados = [a['horario'] for a in agendamentos]
        disponiveis = [h for h in horarios if h not in ocupados]

        if not disponiveis:
            return {"statusCode": 200, "body": json.dumps({"mensagem": "Sem horários disponíveis"})}

        melhor_horario = sorted(disponiveis)[0]

        return {
            "statusCode": 200,
            "body": json.dumps({
                "profissional": profissional,
                "especialidade": especialidade,
                "melhor_horario": melhor_horario
            })
        }

    except Exception as e:
        print("Erro:", e)
        return {"statusCode": 500, "body": json.dumps({"erro": str(e)})}
