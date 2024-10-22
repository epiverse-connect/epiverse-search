Steps to replicate Docker container on your local:


1.	This installations assumes that docker is already installed on the machine. Use https://www.docker.com/products/docker-desktop/ to download relevant docker version.
2.	Download the following official images from Docker hub :
a.	Elasticsearch : docker pull --platform linux/arm64 elasticsearch:8.15.3
b.	Pytorch : docker pull pytorch/pytorch:2.5.0-cuda12.4-cudnn9-runtime [This is linux/amd , while building the new image we will use docker buildx to make it arm compatible] 
3.	Create a directory and copy all the Github files into this directory.
4.	Download “sources.zip” file containing all the text data and add it to the directory
5.	Use the following code to create the docker image: <br>
      _docker buildx build --platform linux/arm64 -f Dockerfile-poc-api -t api-demo:arm64-3 ._
      _docker buildx build --platform linux/arm64 -f Dockerfile-poc-elasticsearch -t populate-index:v1.0 ._
6.	Run the docker container to update elasticsearch index: <br>
      _docker run  --name cont-elastic-1 -p 9200:9200 populate-index:v1.0_
      _docker run  --name cont-elastic-1 -p 8000:8000 api-demo:arm64-3_

