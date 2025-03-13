pipeline {
    agent any

    environment {
        DB_HOST = 'postgres_db'
        DB_NAME = 'eventdb'
        VENV_PATH = 'venv'
    }

    stages {
        stage('Clonar repositorio') {
            steps {
                git branch: 'main',
                    credentialsId: 'L00event1',
                    url: 'https://github.com/Ricardo16365Travez/event-organizer-ai-extension.git'
            }
        }

        stage('Construir y levantar servicios con Docker') {
            steps {
                script {
                    bat 'docker-compose down'
                    bat 'docker-compose up -d --build'
                }
            }
        }

        stage('Esperar a que PostgreSQL esté disponible') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'L00event1', usernameVariable: 'DB_CREDENTIALS_USR', passwordVariable: 'DB_CREDENTIALS_PSW')]) {
                        bat '''
                            echo Esperando a que PostgreSQL esté disponible...
                            :loop
                            docker exec postgres_db pg_isready -h postgres_db -U %DB_CREDENTIALS_USR%
                            if ERRORLEVEL 1 (
                                echo PostgreSQL aún no está listo. Esperando...
                                timeout /t 5 /nobreak
                                goto loop
                            )
                        '''
                    }
                }
            }
        }

        stage('Configurar backend') {
            steps {
                script {
                    bat '''
                        python -m venv %VENV_PATH%
                        call %VENV_PATH%\\Scripts\\activate
                        pip install -r backend/requirements.txt
                    '''
                }
            }
        }

        stage('Ejecutar migraciones de base de datos') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'L00event1', usernameVariable: 'DB_CREDENTIALS_USR', passwordVariable: 'DB_CREDENTIALS_PSW')]) {
                        bat '''
                            call %VENV_PATH%\\Scripts\\activate
                            alembic -c backend/alembic.ini upgrade head
                        '''
                    }
                }
            }
        }

        stage('Ejecutar pruebas del backend') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'L00event1', usernameVariable: 'DB_CREDENTIALS_USR', passwordVariable: 'DB_CREDENTIALS_PSW')]) {
                        withEnv(["TEST_DATABASE_URL=postgresql://%DB_CREDENTIALS_USR%:%DB_CREDENTIALS_PSW%@%DB_HOST%/test_eventdb"]) {
                            bat '''
                                call %VENV_PATH%\\Scripts\\activate
                                pytest backend/tests/ --db-url=%TEST_DATABASE_URL%
                            '''
                        }
                    }
                }
            }
        }

        stage('Verificar frontend') {
            steps {
                script {
                    bat '''
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
                    bat 'echo Aplicación desplegada con éxito.'
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
