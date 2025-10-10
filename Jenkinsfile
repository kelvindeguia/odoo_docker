pipeline {
    agent any

    environment {
        IMAGE_NAME = "odoo18"
        CONTAINER_NAME = "odoo18"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kelvindeguia/odoo_docker.git'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Stop Old') {
            steps {
                sh 'docker stop ${CONTAINER_NAME} || true'
                sh 'docker rm ${CONTAINER_NAME} || true'
            }
        }

        stage('Run Odoo') {
            steps {
                sh '''
                    docker run -d --name ${CONTAINER_NAME} \
                      --network odoo_default \
                      -p 8069:8069 \
                      ${IMAGE_NAME}:latest
                '''
            }
        }
    }

    post {
        success { echo "✅ Odoo deployed successfully!" }
        failure { echo "❌ Build failed." }
    }
}
