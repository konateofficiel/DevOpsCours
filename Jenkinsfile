pipeline {
    agent any 

    environment {
        DOCKER_COMPOSE_VERSION = '3.8'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Sheila-Kambou01/Projet_devOps.git'
            }
        }

        stage('Build and Deploy with Docker Compose') {
            steps {
                script {
                    bat 'dir'

                    bat 'docker-compose up --build -d'
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    bat 'curl --fail http://localhost:8000 || exit 1'
                }
            }
        }

        stage('Notify Success') {
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                script {
                    emailext(
                        subject: "Deploiement effectué",
                        body: "L'application a ete déploye avec success",
                        to: "shei.kambou16@gmail.com"
                    )
                }
            }
        }

        stage('Notify Failure') {
            when {
                expression { currentBuild.result == 'FAILURE' }
            }
            steps {
                script {
                    emailext(
                        subject: "Deploiement non effectué",
                        body: "L'application n'a pas ete déploye",
                        to: "shei.kambou16@gmail.com"
                    )
                }
            }
        }
    }

    post {
        always {
            // Nettoyer si nécessaire après l'exécution
            cleanWs()  // Nettoyer l'espace de travail après chaque exécution
        }
    }
}
