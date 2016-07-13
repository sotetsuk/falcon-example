serve:
	python server.py

get:
	curl http://localhost:3001/api/comments -X GET

post:
	curl http://localhost:3001/api/comments --data '{"text": "added text", "id": "1002", "author": "anonymous"}' -X POST

