

all:
	docker build -t smartcurtain:backend ./Source


run:
	set -a; source .env; set +a; docker run \
		-p 8001:8001 \
		-e SMARTCURTAIN_MQTT_HOST="host.docker.internal" \
		-e SMARTCURTAIN_DB_USER=mpzinke \
		-e SMARTCURTAIN_DB_HOST="host.docker.internal" \
		-e SMARTCURTAIN_DB_PASSWORD="" \
		smartcurtain:backend


clean:
	docker rmi `docker images --filter dangling=true -q` --force


kill:
	docker stop `docker ps -q`
