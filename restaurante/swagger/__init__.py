from flask_restx import Api


api = Api(
    version="1.0",
    title="API de Gerenciamento de Pizzaria",
    description="Documentação da API para clientes, professores, pedido, itempedido, itemcardapio",
    doc="/docs",
    mask_swagger=False,
    prefix="/api"
)