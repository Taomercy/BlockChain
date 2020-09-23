# bc_demo

Python sample for blockchain application, thanks https://www.cnblogs.com/tinyxiong/p/7761026.html for thoughts and sample codes.

Instruction
- Install Postman for debug
- Check python version is 3.X
- Install flask and other required packages
- Run command 'python server.py -p 5000' to start the server, default port is 5000.
- Run command 'python server.py -p 5001' to start the server, default port is 5000.
- Run command 'python server.py -p 5002' to start the server, default port is 5000.
- Mine a new block: http://localhost:port/mine
- Display chains on current node: http://localhost:port/chain
- Register node (Because we don't implement a P2P protocal now, you need manually register your neigbours)
  - Post: http://localhost:5000/nodes/register
  - Raw data: {"nodes": ["http://localhost:5000","http://localhost:5001", "http://localhost:5002"]}
  - Content-Type: application/json
- Display all nodes registed: http://localhost:port/nodes

- Resolve conflicts and work on the longest chain: http://localhost:port/nodes/resolve
- Resolve conflicts of transactions: http://localhost:port/nodes/resolve_transaction
- Transaction (The transaction will be valid until be packaged to the block)
  - Post: http://localhost:port/transaction/new
  - Raw data: {"sender": "xxx", "recipient": "yyy", "amount": 0.5}
  - Content-Type: application/json
