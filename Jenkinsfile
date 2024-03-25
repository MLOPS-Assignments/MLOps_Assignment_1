pipeline {
  agent any
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  environment {
    DOCKERHUB_CREDENTIALS = credentials('moizxsania-dockerhub')
  }
  stages {
    stage('Build') {
      steps {
        bat 'docker build -t moizxsania/dp-alpine:latest .' // Use 'bat' for Windows commands
      }
    }
    stage('Scan') {
      steps {
        // Replace 'docker scan' with 'docker scout'
        bat 'docker scout moizxsania/dp-alpine:latest' // Use 'bat' for Windows commands
      }
    }
    stage('Publish') {
      steps {
        bat '''
          docker login -u %DOCKERHUB_CREDENTIALS_USR% -p %DOCKERHUB_CREDENTIALS_PSW%
          docker push moizxsania/dp-alpine:latest
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
