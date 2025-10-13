pipeline {
    agent any

    environment {
        IMAGE_NAME = "odoo18"
        ODOO_CONTAINER = "odoo18"
        DB_CONTAINER = "odoo18-db"
        NETWORK_NAME = "odoo18-network"
        DB_USER = "odoo"
        DB_PASSWORD = "Pr0t3ct10n!"
        DB_NAME = "postgres"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/kelvindeguia/odoo_docker.git'
            }
        }

        stage('Build Odoo Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Create Network') {
            steps {
                sh '''
                  if [ -z "$(docker network ls --filter name=^${NETWORK_NAME}$ -q)" ]; then
                    docker network create ${NETWORK_NAME}
                  fi
                '''
            }
        }

        stage('Start Postgres') {
            steps {
                sh '''
                  if [ -z "$(docker ps -q -f name=${DB_CONTAINER})" ]; then
                    docker run -d --name ${DB_CONTAINER} \
                      --network ${NETWORK_NAME} \
                      -e POSTGRES_USER=${DB_USER} \
                      -e POSTGRES_PASSWORD=${DB_PASSWORD} \
                      -e POSTGRES_DB=${DB_NAME} \
                      -v pg-data:/var/lib/postgresql/data \
                      postgres:15
                  fi
                '''
            }
        }

        stage('Deploy Odoo') {
            steps {
                sh '''
                  docker stop ${ODOO_CONTAINER} || true
                  docker rm ${ODOO_CONTAINER} || true
        
                  # Start Odoo container (without mounting odoo.conf)
                  docker run -d --name ${ODOO_CONTAINER} \
                    --network ${NETWORK_NAME} \
                    -p 8069:8069 \
                    -v $WORKSPACE/addons:/mnt/extra-addons \
                    -v odoo-data:/var/lib/odoo \
                    ${IMAGE_NAME}:latest
        
                  # Copy odoo.conf into the container after it starts
                  docker cp $WORKSPACE/odoo.conf ${ODOO_CONTAINER}:/etc/odoo/odoo.conf
        
                  # Optional: Restart to reload config cleanly
                  docker restart ${ODOO_CONTAINER}
                '''
            }
        }
    }

    // test
    post {
        success { echo "✅ Odoo deployed successfully!" }
        failure { echo "❌ Build failed." }
    }
}
