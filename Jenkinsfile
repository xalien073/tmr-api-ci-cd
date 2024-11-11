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
            stage('Static Code Analysis') {
                environment {
                    SONAR_URL = 'http://20.44.59.222:9000'
                }
                steps {
                    withCredentials([string(credentialsId: 'sonarqube', variable: 'SONAR_AUTH_TOKEN')]) {
                        echo 'Running SonarQube analysis'
                        sh """
                            apk update
                            apk add openjdk11 curl unzip python3 py3-pip git
                            curl -o sonar-scanner.zip -L https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.7.0.2747-linux.zip
                            unzip sonar-scanner.zip -d /opt
                            ln -s /opt/sonar-scanner-4.7.0.2747-linux/bin/sonar-scanner /usr/bin/sonar-scanner
                            sed -i 's/use_embedded_jre=true/use_embedded_jre=false/' /opt/sonar-scanner-4.7.0.2747-linux/bin/sonar-scanner
                            sonar-scanner --version
                            
                            python3 -m pip install --no-cache-dir -r requirements.txt
                            sonar-scanner \
                            -Dsonar.projectKey=TMR-API \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_URL} \
                            -Dsonar.login=${SONAR_AUTH_TOKEN}
                        """
                    }
                }
            }
            
            // stage('Quality Gate') {
            //     steps {
            //         timeout(time: 1, unit: 'MINUTES') {
            //             waitForQualityGate abortPipeline: true
            //         }
            //     }
            // }
            
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
            
            stage('Update Helm Chart') {
                environment {
                    GIT_REPO_NAME = "tmr-api-ci-cd"
                    GIT_USER_NAME = "xalien073"
                }
                steps {
                    withCredentials([string(credentialsId: 'github', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        git config user.email "xalien073@gmail.com"
                        git config user.name "xalien073"
                        BUILD_NUMBER=${BUILD_NUMBER}
                        sed -i 's/tag:.*/tag: ${env.BUILD_ID}/' values.yaml k8s/AKS/helm/fastapi-app
                        git add values.yaml
                        git commit -m "Update deployment image to version ${BUILD_NUMBER}"
                        git push https://${GITHUB_TOKEN}@github.com/${GIT_USER_NAME}/${GIT_REPO_NAME} HEAD:main
                    '''
                    }
                }
            }

            // stage('Deploy to AKS') {
            //     steps {
            //         script {
            //             sh '''
            //             helm upgrade myapp
        }
    }