# Use an official OpenJDK runtime as a parent image
FROM debian:latest

USER root

# Set the working directory inside the container
WORKDIR /app 

COPY ./ ./

RUN apt-get update && apt-get install -y maven openjdk-21-jdk

RUN  mvn clean install
EXPOSE 8080

ENTRYPOINT ["mvn", "spring-boot:run"]