# API

This folder contains relevant information to building the docker image and running it locally.

```
docker buildx build --platform linux/arm64 -f Dockerfile-poc-api -t api-demo:arm64-5 .

docker run -d  --name cont-elastic-1 -p 8000:8000 api-demo:arm64-5
```

Please note that this requires the ElasticSearch Docker image to also be running.