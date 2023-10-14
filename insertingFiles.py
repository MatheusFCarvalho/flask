from pymongo import MongoClient

# Conectando ao servidor MongoDB
MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

db = client['pequi']

collection = db['roteiro']

data = {
    "data": "06-10-2023",
    "pedidos": [
        {
            "cliente": "TIAGO SANTA MARIA",
            "isDone": False,
            "isError": False,
            "messagesError": [],
            "pedidos": [
                {
                    "endereco": "COLOCAR ENDEREÇO NO SISTEMA",
                    "numero": 0,
                    "observacoes": "LIBERADO",
                    "pecas": 13,
                    "isDone": False,
                }
            ],
        },
        {
            "cliente": "VIDRAÇARIA VIRGINIA",
            "isDone": False,
            "isError": False,
            "messagesError": [],
            "pedidos": [
                {
                    "endereco": "RUA JOSE DE PAULA SILVA NEVES - 141 SANTA INES",
                    "numero": 0,
                    "observacoes": "",
                    "pecas": 2,
                    "isDone": False,
                }
            ],
        },
        {
            "cliente": "ESQUADRI GLASS",
            "isDone": False,
            "isError": False,
            "messagesError": [],
            "pedidos": [
                {
                    "endereco": "RUA DOS SERRALHEIROS - 45",
                    "numero": 0,
                    "observacoes": "",
                    "pecas": 8,
                    "isDone": False,
                }
            ],
        },
        {
            "cliente": "CAVALCANTE",
            "isDone": False,
            "isError": False,
            "messagesError": [],
            "pedidos": [
                {
                    "endereco": "RUA BENEDITO FERNANDES DE ANDRADE",
                    "numero": 0,
                    "observacoes": "",
                    "pecas": 1,
                    "isDone": False,
                },
                {
                    "endereco": "",
                    "numero": 0,
                    "observacoes": "",
                    "pecas": 11,
                    "isDone": False,
                },
                {
                    "endereco": "",
                    "numero": 0,
                    "observacoes": "",
                    "pecas": 1,
                    "isDone": False,
                },
            ],
        },
        {
            "cliente": "2M MOVELARIA",
            "isDone": False,
            "isError": False,
            "messagesError": [],
            "pedidos": [
                {
                    "endereco": "AV PRES. TANCREDO NEVES - 797",
                    "numero": 0,
                    "observacoes": "LIBERADO",
                    "pecas": 1,
                    "isDone": False,
                },
                {
                    "endereco": "",
                    "numero": 0,
                    "observacoes": "",
                    "pecas": 2,
                    "isDone": False,
                },
            ],
        },
        {
            "cliente": "MARCENARIA JOSEENSE",
            "isDone": False,
            "isError": False,
            "messagesError": [],
            "pedidos": [
                {
                    "endereco": "RUA HELEODORA PEREIRA LEMES - 77",
                    "numero": 0,
                    "observacoes": "",
                    "pecas": 2,
                    "isDone": False,
                }
            ],
        },
        {
            "cliente": "ESQUADRI GLASS",
            "isDone": False,
            "isError": False,
            "messagesError": [],
            "pedidos": [
                {
                    "endereco": "RUA DOS SERRALHEIROS - 45",
                    "numero": 0,
                    "observacoes": "",
                    "pecas": 3,
                    "isDone": False,
                }
            ],
        },
    ],
    "total_pedidos": 9,
    "total_pecas": 44,
}

# Inserindo o documento na coleção
result = collection.insert_one(data)

print(f"Documento inserido com ID: {result.inserted_id}")

# Fechando a conexão
client.close()
