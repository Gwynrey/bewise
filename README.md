# bewise

1. Запустите контейнер postgresql с помощью команды "docker-compose up -d".
2. Соберите Docker-образ с помощью команды "docker build -t quiz-service".
3. Запустите контейнер с помощью команды docker run -d --name quiz-service -p 80:80 quiz-service