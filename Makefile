

all:
	docker build -t smartcurtain:backend ./Source


run:
	set -a; source .env; set +a && docker run \
		-p 8001:8001 \
		-e SMARTCURTAIN_MQTT_HOST="$${SMARTCURTAIN_MQTT_HOST}" \
		-e SMARTCURTAIN_DB_USER="$${SMARTCURTAIN_DB_USER}" \
		-e SMARTCURTAIN_DB_HOST="$${SMARTCURTAIN_DB_HOST}" \
		-e SMARTCURTAIN_DB_PASSWORD="$${SMARTCURTAIN_DB_USER}" \
		smartcurtain:backend


clean:
	docker rmi `docker images --filter dangling=true -q` --force


kill:
	docker stop `docker ps -q`
