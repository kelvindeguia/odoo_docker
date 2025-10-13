pipeline {
    agent any

    environment {
        IMAGE_NAME     = "odoo18"
        DB_CONTAINER   = "odoo18-db"
        NETWORK_NAME   = "odoo18-network"
        DB_USER        = "odoo"
        DB_PASSWORD    = "Pr0t3ct10n!"
        DB_NAME        = "postgres"
        NGINX_CONTAINER = "odoo18-nginx"   // container name of your reverse proxy
        NGINX_CONF_PATH = "/etc/nginx/conf.d/odoo-upstream.conf" // update this if different
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

        stage('Blue-Green Deploy') {
            steps {
                sh '''
                  # Detect which container is live
                  if docker ps --format '{{.Names}}' | grep -q "odoo18-blue"; then
                      LIVE="odoo18-blue"
                      NEW="odoo18-green"
                      NEW_PORT=8070
                  else
                      LIVE="odoo18-green"
                      NEW="odoo18-blue"
                      NEW_PORT=8069
                  fi
        
                  echo "🔵 Live container: $LIVE"
                  echo "🟢 Deploying new container: $NEW on port $NEW_PORT"
        
                  # Check if port is already in use
                  if ss -tln | grep -q ":$NEW_PORT "; then
                      echo "⚠️ Port $NEW_PORT already in use. Incrementing to avoid conflict."
                      NEW_PORT=$((NEW_PORT+1))
                  fi
        
                  # Remove old $NEW container if exists
                  docker rm -f $NEW || true
        
                  # Start new container on the alternate port
                  docker run -d --name $NEW \
                    --network ${NETWORK_NAME} \
                    -p $NEW_PORT:8069 \
                    -v odoo-data:/var/lib/odoo \
                    ${IMAGE_NAME}:latest
        
                  # Copy config and addons
                  docker cp $WORKSPACE/odoo.conf $NEW:/etc/odoo/odoo.conf
                  docker exec $NEW mkdir -p /mnt/extra-addons
                  docker cp $WORKSPACE/addons/. $NEW:/mnt/extra-addons/
        
                  echo "Waiting for Odoo ($NEW) to initialize..."
                  sleep 20
        
                  echo "🩺 Checking health..."
                  if docker exec $NEW curl -sSf http://localhost:8069/web/login > /dev/null; then
                      echo "✅ Odoo $NEW is healthy!"
                  else
                      echo "❌ Health check failed. Keeping $LIVE active."
                      docker logs $NEW | tail -n 30
                      exit 1
                  fi
        
                  echo "Switching Nginx upstream to $NEW..."
                  docker exec ${NGINX_CONTAINER} bash -c "cat > ${NGINX_CONF_PATH}" <<EOF
                  upstream odoo_backend {
                      server ${NEW}:8069;
                  }
                  server {
                      listen 80;
                      server_name _;
                      location / {
                          proxy_pass http://odoo_backend;
                          proxy_set_header Host \$host;
                          proxy_set_header X-Real-IP \$remote_addr;
                          proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
                          proxy_set_header X-Forwarded-Proto \$scheme;
                      }
                  }
                  EOF
        
                  docker exec ${NGINX_CONTAINER} nginx -s reload
                  echo "🔁 Switched Nginx to ${NEW} successfully."
        
                  echo "🧹 Stopping old container: $LIVE"
                  docker stop $LIVE || true
                '''
            }
        }
    }

    post {
        success { echo "✅ Blue-Green Odoo Deployment Successful!" }
        failure { echo "❌ Blue-Green Deployment Failed. Previous version kept running." }
    }
}
