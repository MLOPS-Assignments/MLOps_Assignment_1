pipeline {
  agent { label 'windows' } // Use 'windows' label for Windows agents
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('saniaarshad-dockerhub')
  }
  stages {
    stage('Build') {
      steps {
        bat 'docker build -t saniaarshad/dp-alpine:latest .' // Use 'bat' for Windows commands
      }
    }
    stage('Scan') {
      steps {
        bat 'docker scan saniaarshad/dp-alpine:latest' // Use 'bat' for Windows commands
      }
    }
    stage('Publish') {
      steps {
        bat '''
          docker login -u %DOCKERHUB_CREDENTIALS_USR% -p %DOCKERHUB_CREDENTIALS_PSW%
          docker push saniaarshad/dp-alpine:latest
          docker logout
        '''
      }
    }
  }
  post { // Add a post section for post-build actions
    success { // Execute these steps only if the pipeline succeeds
      emailext (
        to: 'i202425@nu.edu.pk', // Specify the email address of the admin
        subject: "Pipeline Successful", // Subject of the email
        body: "Your Jenkins pipeline has been successfully executed." // Body of the email
      )
    }
  }
}
