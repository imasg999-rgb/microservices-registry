# microservices-registry
test

1) Open Docker Desktop

2) Open up 2 terminal tabs
one used for registry (cd /registry)
one used for service (cd /microservices/core/microservice-working-template-service)

3) in both terminals, call "docker-compose up --build" (build docker container for registry)
this should be reflected on Docker Desktop (under the containers tab)

4) in Docker Desktop > Containers tab > expand 'registry' containers > 'db-1' container ellipses > Open in Terminal > "mysql -u root -p" > pw="group4" > NOW IN SQL TERMINAL
use for accessing/viewing from application databases

5) Registry whipped up locally @ Port-[7993](http://127.0.0.1:7993) | Template Service @ Port-[8080](http://127.0.0.1:8080)

6) 