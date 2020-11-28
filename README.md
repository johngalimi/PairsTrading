# Pairs Trading

```bash
docker build -t pairstrading .
docker run -it pairstrading

# complete each time a dependency is added
pip freeze > requirements.txt
```

- Spin up trade server (go): `go run trade_server.go`
- Run trade client + identifier (python): `python3 trade.py`