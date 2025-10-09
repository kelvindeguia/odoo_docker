pipeline {
    agent any

    environment {
        IMAGE_NAME = "odoo18"
        CONTAINER_NAME = "odoo18"
        DB_CONTAINER = "odoo18-db"
        NETWORK_NAME = "odoo_default"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kelvindeguia/odoo_docker.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Stop Old Container') {
            steps {
                sh "docker stop ${CONTAINER_NAME} || true"
                sh "docker rm ${CONTAINER_NAME} || true"
            }
        }

        stage('Run New Container') {
            steps {
                sh """
                docker run -d \
                  --name ${CONTAINER_NAME} \
                  --network ${NETWORK_NAME} \
                  -p 8069:8069 \
                  -v \$PWD/odoo.conf:/etc/odoo/odoo.conf \
                  -v \$PWD/addons:/mnt/extra-addons \
                  -v \$PWD/odoo-data:/var/lib/odoo \
                  ${IMAGE_NAME}:latest
                """
            }
        }
    }

    post {
        success {
            echo "✅ Build & Deploy successful!"
        }
        failure {
            echo "❌ Build failed. Check console output."
        }
    }
}
