pipeline { 
    agent any
    environ {env = 'mon_venv'
    }
    stages { 
        stage('Checkout') { 
            steps { 
                git branch: 'main', url: 'https://github.com/konateofficiel/DevOpsCours.git' 
            } 
        } 
        stage('Install Dependencies') { 
            steps { 
                sh 'python -m venv mon_venv' 
            } 
        }
 
        stage('Run Script') { 
            steps { 
                bat '.\\mon_venv\\bin\\python Tache1.py' 
            } 
        } 
    }
 
    post { 
    success { 
        emailext subject: "Build SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Le build de ${env.JOB_NAME} a réussi.\nConsultez les logs ici: ${env.BUILD_URL}",
                 recipientProviders: [[$class: 'DevelopersRecipientProvider']],
                 to: 'konateofficiel1997@gmail.com'
    } 
    failure { 
        emailext subject: "Build FAILURE: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                 body: "Le build de ${env.JOB_NAME} a échoué.\nConsultez les logs ici: ${env.BUILD_URL}",
                 recipientProviders: [[$class: 'DevelopersRecipientProvider']],
                 to: 'konateofficiel1997@gmail.com'
            } 
       }
}
