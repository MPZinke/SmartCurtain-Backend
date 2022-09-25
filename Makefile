

build:
	docker build -t test --build-arg NETWORKLOOKUP_BEARERTOKEN="${NETWORKLOOKUP_BEARERTOKEN}" --build-arg NETWORKLOOKUP_HOST="${NETWORKLOOKUP_HOST}" --build-arg SMARTCURTAIN_NETWORKNAME="${SMARTCURTAIN_NETWORKNAME}" --build-arg SMARTCURTAIN_DB_USER="${SMARTCURTAIN_DB_USER}" --build-arg SMARTCURTAIN_DB_HOST="${SMARTCURTAIN_DB_HOST}" --build-arg SMARTCURTAIN_API_TOKEN="${SMARTCURTAIN_API_TOKEN}" .

run:
	# https://stackoverflow.com/a/49907758
	docker run --add-host="host.docker.internal:host-gateway" -p 3000:3000 -p 8080:8080 test

kill:
	docker stop $(docker ps)
