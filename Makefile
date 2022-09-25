

build-backend:
	docker build -t smart_curtain-backend \
	  --build-arg NETWORKLOOKUP_BEARERTOKEN="${NETWORKLOOKUP_BEARERTOKEN}" \
	  --build-arg NETWORKLOOKUP_HOST="${NETWORKLOOKUP_HOST}" \
	  --build-arg SMARTCURTAIN_NETWORKNAME="${SMARTCURTAIN_NETWORKNAME}" \
	  --build-arg SMARTCURTAIN_DB_USER="${SMARTCURTAIN_DB_USER}" \
	  --build-arg SMARTCURTAIN_DB_HOST="${SMARTCURTAIN_DB_HOST}" \
	  --build-arg SMARTCURTAIN_DB_PASSWORD="${SMARTCURTAIN_DB_PASSWORD}" \
	  --build-arg SMARTCURTAIN_BACKEND_API_KEY="${SMARTCURTAIN_BACKEND_API_KEY}" \
	  ./Backend


build-frontend:
	docker build -t smart_curtain-frontend ./Frontend


run-backend:
	# https://stackoverflow.com/a/49907758
	docker run --add-host="host.docker.internal:host-gateway" -p 8080:8080 smart_curtain-backend

run-frontend:
	# https://stackoverflow.com/a/49907758
	docker run --add-host="host.docker.internal:host-gateway" -p 3000:3000 smart_curtain-frontend


clean:
	docker rmi `docker images --filter dangling=true -q` --force


kill:
	docker stop `docker ps -q`
