pipeline {
    agent any

    environment {
        DB_URL = 'postgresql://postgres:postgres@flask_db:5432/postgres'
    }

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build('flask_app:1.0.0', '.')
                }
            }
        }

        stage('Start DB') {
            steps {
                script {
                    sh 'docker run -d --rm --name flask_db -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -v pgdata:/var/lib/postgresql/data postgres:12'
                }
            }
        }

        stage('Wait for DB') {
            steps {
                script {
                    // Esperar hasta que el puerto 5432 de PostgreSQL esté disponible
                    sh '''
                        echo "Esperando a que PostgreSQL esté disponible..."
                        for i in {1..20}; do
                          nc -z flask_db 5432 && echo "PostgreSQL está listo." && exit 0
                          echo "Esperando..."
                          sleep 2
                        done
                        echo "Tiempo de espera agotado"
                        exit 1
                    '''
                }
            }
        }

        stage('Test DB Connection') {
            steps {
                script {
                    docker.image('flask_app:1.0.0').withRun("-p 4000:4000 --name flask_app --link flask_db -e DB_URL=${env.DB_URL}") { c ->
                        // Aquí se verifica conexión con psycopg2 o similar
                        sh """
                        docker exec flask_app python3 -c "import psycopg2; conn = psycopg2.connect('${env.DB_URL}'); print('Conexión exitosa'); conn.close()"
                        """
                        // Aquí podrías agregar tus pruebas
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                // Limpiar contenedores y volumenes si están corriendo
                sh 'docker rm -f flask_app || true'
                sh 'docker rm -f flask_db || true'
                sh 'docker volume rm pgdata || true'
            }
        }
    }
}