pipeline {
    agent any

    environment {
        DB_CREDENTIALS = credentials('postgresql-credentials')
        DB_HOST = 'postgres_db'
        DB_NAME = 'eventdb'
        SQLALCHEMY_DATABASE_URL = "postgresql://${DB_CREDENTIALS_USR}:${DB_CREDENTIALS_PSW}@${DB_HOST}/${DB_NAME}"
        VENV_PATH = 'venv'
    }

    stages {
        stage('Clonar repositorio') {
            steps {
                git branch: 'main', url: 'https://github.com/tu-usuario/event-organizer-ai-extension.git'
            }
        }

        stage('Construir y levantar servicios con Docker') {
            steps {
                script {
                    sh 'docker-compose down'
                    sh 'docker-compose up -d --build'
                }
            }
        }

        stage('Esperar a que PostgreSQL esté disponible') {
            steps {
                script {
                    sh 'echo "Esperando a que PostgreSQL esté disponible..."'
                    sh '''
                        until docker exec postgres_db pg_isready -h ${DB_HOST} -U ${DB_CREDENTIALS_USR}; do
                            echo "Esperando a PostgreSQL..."
                            sleep 5
                        done
                    '''
                }
            }
        }

        stage('Configurar backend') {
            steps {
                script {
                    sh '''
                        python -m venv ${VENV_PATH}
                        source ${VENV_PATH}/bin/activate
                        pip install -r backend/requirements.txt
                    '''
                }
            }
        }

        stage('Ejecutar migraciones de base de datos') {
            steps {
                script {
                    sh '''
                        source ${VENV_PATH}/bin/activate
                        alembic -c backend/alembic.ini upgrade head
                    '''
                }
            }
        }

        stage('Ejecutar pruebas del backend') {
            steps {
                script {
                    sh '''
                        source ${VENV_PATH}/bin/activate
                        export TEST_DATABASE_URL="postgresql://${DB_CREDENTIALS_USR}:${DB_CREDENTIALS_PSW}@${DB_HOST}/test_eventdb"
                        pytest backend/tests/ --db-url=$TEST_DATABASE_URL
                    '''
                }
            }
        }

        stage('Verificar frontend') {
            steps {
                script {
                    sh '''
                        cd frontend
                        npm install
                        npm run build
                    '''
                }
            }
        }

        stage('Desplegar aplicación') {
            steps {
                script {
                    sh 'echo "Aplicación desplegada con éxito."'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completado con éxito.'
        }
        failure {
            echo 'Pipeline fallido.'
        }
    }
}
