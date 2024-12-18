up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans --rmi 'all'