pipeline {
    agent any
    environment {
        VENV_DIR = 'mon_venv'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/konateofficiel/DevOpsCours.git'
            }
        }
        stage('Setup') {
            steps {
                bat 'python -m venv mon_venv'  // Crée un environnement virtuel
                // bat '.\\venv\\Scripts\\pip install -r requirements.txt'  // Installe les dépendances
            }
        }
        stage('Run Script') {
            steps {
                bat '.\\mon_venv\\Scripts\\python Tache1.py'  // Exécute le script Python
            }
        }
        stage('Notify') {
            steps {
                script {
                    def result = currentBuild.result ?: 'SUCCESS'
                    emailext subject: "Jenkins Build: ${result}",
                        body: "Build Status: ${result}\nVoir Jenkins: ${env.BUILD_URL}",
                        to: 'konateofficiel1997@gmail.com'
                }
            }
        }
    }
    post {
        failure {
            emailext subject: "Échec du build Jenkins",
                body: "Échec du pipeline : ${env.BUILD_URL}",
                to: 'konateofficiel1997@gmail.com'
        }
    }
}
