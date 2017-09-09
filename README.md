# NUT - network unit testing

## Database schema

Default parameters:
- id
- name
- description
- date added 
- date modified


Test
- data (test json)
- status

Inventory
- hostname
- network

Network
- subnet
- location



## Running
Controller node:
```
docker run -itd --name nut_rabbitmq rabbitmq
docker run -itd -v $(pwd):/opt/nut -p 80:80 -p 443:443 --name nut_app nut
```

Tester node:
```
docker run -itd --name nut_client
```

## TODOs
Security:
- Set REST API clients to view only owned resources

Code
- Add Unit tests for models
- Add Unit tests for API
- Add Code coverage
- Integrate to Trevis
- Integrated Server discovery via DNS (Consul style)

Functionality:
- Deprecated subnets are deleted from API (maybe we should keep them for historical purposes)
- Deprecated networks are deactivated (should they be deactivated or deleted, that is the question)

It would be shame if NUT project would not have Unit tests!
