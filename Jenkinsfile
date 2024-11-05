pipeline {
    agent {
        docker {
            image 'docker:24.0.1-dind'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock' // Mount Docker socket to access the host's Docker daemon
        }
    }

    environment {
        DOCKER_IMAGE = "xalien073/tmr_api:${env.BUILD_ID}" // Tag image with Jenkins Build ID
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
    
        stage('Push to Docker Hub') {
            steps {
                script {
                    // Use credentials to log in to Docker Hub
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    }

                    // Push the Docker image
                    sh 'docker push $DOCKER_IMAGE'
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

        // stage('Deploy to AKS') {
        //     steps {
        //         script {
        //             sh '''
        //             helm upgrade myapp
