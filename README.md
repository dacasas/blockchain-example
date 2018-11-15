# blockchain-example
Little example of a blockchain architecture

Basado en el ejemplo desarrollado por Gerald Nash ([parte 1](https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b), [parte 2](https://medium.com/crypto-currently/lets-make-the-tiniest-blockchain-bigger-ac360a328f4d)).

Ejecutar server.py, y hacer posibles requests al servidor (localhost:5000):

```(yml)
# Make new transaction
POST /transaction
    headers:
        Content-Type: application/json
    body:
        {
            "from": sender_id,
            "to": receiver_id,
            "amount": amount,
        }

# Mine new block
GET /mine

# Get blocks in the chain
GET /blocks
```