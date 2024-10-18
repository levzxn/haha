from jinja2 import Template


TEMPLATE_PASSWORD_RESET = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recuperação de Senha</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        .header {
            background-color: #007bff;
            padding: 20px;
            text-align: center;
            color: white;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .content {
            padding: 30px;
            text-align: center;
        }
        .content p {
            font-size: 16px;
            color: #333333;
            margin: 0 0 20px;
        }
        .content .highlight {
            color: #ffc107;
            font-weight: bold;
        }
        .token {
            display: inline-block;
            padding: 12px 25px;
            background-color: #ffc107;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
            font-size: 16px;
            margin-top: 20px;
        }
        .footer {
            background-color: #007bff;
            color: white;
            padding: 10px;
            text-align: center;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Cabeçalho -->
        <div class="header">
            <h1>Recuperação de Senha</h1>
        </div>

        <!-- Conteúdo -->
        <div class="content">
            <p>Olá,</p>
            <p>Recebemos um pedido para redefinir a sua senha.</p>
            <p>Para redefinir a sua senha, informe o token abaixo:</p>
            <p class="token">{{token}}</p>
            <p class="highlight">Se você não solicitou a redefinição, ignore este e-mail.</p>
        </div>

        <!-- Rodapé -->
        <div class="footer">
            <p>Atenciosamente,</p>
            <p>Equipe de Suporte</p>
        </div>
    </div>
</body>
</html>
"""


def render_template(template_str, context):
    template = Template(template_str)
    return template.render(context)

def EmailTemplate(keys):
    template = Template(TEMPLATE_PASSWORD_RESET)
    body = template.render(keys)
    return body