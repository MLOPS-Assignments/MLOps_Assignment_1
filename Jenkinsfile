pipeline {
    agent any 

    environment {
        DOCKERHUB_CREDENTIALS_ID = 'moizxsania-dockerhub'
        DOCKER_REPO = 'moizasghar/mlops_a01'
        IMAGE_TAG = 'latest'
        EMAIL_RECIPIENT = 'i202425@nu.edu.pk'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Building the Docker image
                    docker.build("${DOCKER_REPO}:${IMAGE_TAG}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Logging into Docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDENTIALS_ID) {
                        // Pushing the image to Docker Hub
                        docker.image("${DOCKER_REPO}:${IMAGE_TAG}").push()
                    }
                }
            }
        }

        stage('Send Notification Email') {
            steps {
                script {
                    // Sending email notification
                    mail bcc: '', 
                         body: 'The Jenkins job successfully containerized the application and pushed it to Docker Hub.', 
                         cc: '', 
                         from: '', 
                         replyTo: '', 
                         subject: 'Jenkins Job Success', 
                         to: EMAIL_RECIPIENT
                }
            }
        }
    }
    post {
        failure {
            script {
                // Sending email notification upon failure
                mail bcc: '', 
                     body: 'The Jenkins job failed. Please check the Jenkins logs for more details.', 
                     cc: '', 
                     from: '', 
                     replyTo: '', 
                     subject: 'Jenkins Job Failure', 
                     to: EMAIL_RECIPIENT
            }
        }
    }
}
