pipeline {
    agent {
        docker {
            image 'docker:24.0.1-dind'
            args '-v /var/run/docker.sock:/var/run/docker.sock'  // Optional: if you need Docker in Docker
        }  // Run inside a Docker container with Docker installed
    }

    environment {
        DOCKER_IMAGE = "xalien073/tmr_api:${env.BUILD_ID}"  // Tag image with Jenkins Build ID
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker --version'
                    echo 'Building docker image using Jenkins!'
                    sh 'docker build -t $DOCKER_IMAGE .'
                }
            }
        }
    }
}
        // stage('SonarQube Analysis') {
        //     environment {
        //         scannerHome = tool 'SonarQubeScanner'  // SonarQube Scanner installation name
        //     }
        //     steps {
        //         script {
        //             withSonarQubeEnv('SonarQube') {
        //                 sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=my_project -Dsonar.sources=src/"
        //             }
        //         }
        //     }
        // }

        // stage('Quality Gate') {
        //     steps {
        //         timeout(time: 1, unit: 'MINUTES') {
        //             waitForQualityGate abortPipeline: true
        //         }
        //     }
        // }

        // stage('Update Helm Chart') {
        //     steps {
        //         script {
        //             sh '''
        //             cd C:/path/to/your/helm/chart
        //             sed -i 's/tag:.*/tag: ${env.BUILD_ID}/' values.yaml
        //             '''
        //         }
        //     }
        // }

        // stage('Deploy to Kubernetes') {
        //     steps {
        //         script {
        //             sh '''
        //             helm upgrade myapp
