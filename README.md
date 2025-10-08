**🧪 Testes Locais**
🔍 Teste 1 – Verificar disponibilidade

**Crie o arquivo event_disponibilidade.json:**

{
  "queryStringParameters": {
    "especialidade": "Cardiologia",
    "profissional": "Dr. Pedro"
  }
}


Execute:

python lambda_verificar_disponibilidade.py


Saída esperada:

{
  "profissional": "Dr. Pedro",
  "especialidade": "Cardiologia",
  "melhor_horario": "10:00"
}

🗓️ Teste 2 – Criar agendamento

Crie o arquivo event_agendamento.json:

{
  "body": "{\"profissional\": \"Dr. Pedro\", \"especialidade\": \"Cardiologia\", \"horario\": \"10:00\", \"pet\": \"Thor\", \"dono\": \"Derick\"}"
}


Execute:

python lambda_criar_agendamento.py


Saída esperada:

{"mensagem": "Agendamento criado e médico notificado"}


Após isso, o médico cadastrado no tópico SNS receberá uma notificação (e-mail ou SMS).

🌩️ Teste pela AWS (via API Gateway)
1️⃣ Endpoint 1 – Consultar disponibilidade
GET https://{api-id}.execute-api.{region}.amazonaws.com/dev/disponibilidade?especialidade=Cardiologia&profissional=Dr.%20Pedro

2️⃣ Endpoint 2 – Criar agendamento
POST https://{api-id}.execute-api.{region}.amazonaws.com/dev/agendar
Content-Type: application/json
Body:
{
  "profissional": "Dr. Pedro",
  "especialidade": "Cardiologia",
  "horario": "10:00",
  "pet": "Thor",
  "dono": "Derick"
}