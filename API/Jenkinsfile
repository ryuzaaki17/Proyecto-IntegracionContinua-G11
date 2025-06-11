pipeline {
    agent any

    environment {
        DB_URL = 'postgresql://postgres:postgres@flask_db:5432/postgres'
        REPO_URL = 'https://github.com/ryuzaaki17/Proyecto-IntegracionContinua-G11.git'
        REPO_DIR = 'Proyecto-IntegracionContinua-G11'
    }

    stages {
        stage('Cleanup Previous Run') {
            steps {
                script {
                    sh '''
                        docker rm -f flask_app || true
                        docker rm -f flask_db || true
                        docker volume rm pgdata || true
                    '''
                }
            }
        }

        stage('Clone Repository') {
            steps {
                sh 'rm -rf $REPO_DIR || true'
                sh 'git clone $REPO_URL $REPO_DIR'
            }
        }

        stage('Build') {
            steps {
                dir("$REPO_DIR"){
                    sh '''
                        cd API/
                        docker compose build
                    '''
                }
            }
        }

        stage('Start DB') {
            steps {
                script {
                    sh '''
                        docker run -d --rm --name flask_db \
                        -p 5432:5432 \
                        -e POSTGRES_USER=postgres \
                        -e POSTGRES_PASSWORD=postgres \
                        -e POSTGRES_DB=postgres \
                        -v pgdata:/var/lib/postgresql/data \
                        postgres:12
                    '''
                }
            }
        }

        stage('Wait for DB') {
            steps {
                script {
                    sh '''
                        echo "Esperando a que PostgreSQL esté disponible..."
                        COUNTER=0
                        MAX_RETRIES=30
                        while [ $COUNTER -lt $MAX_RETRIES ]; do
                            if docker exec flask_db pg_isready -U postgres -h localhost; then
                                echo "PostgreSQL está listo después de $COUNTER intentos"
                                exit 0
                            fi
                            COUNTER=$((COUNTER+1))
                            echo "Intento $COUNTER/$MAX_RETRIES - Esperando..."
                            sleep 2
                        done
                        echo "ERROR: Tiempo de espera agotado - PostgreSQL no está disponible"
                        docker logs flask_db
                        exit 1
                    '''
                }
            }
        }

        stage('Test DB Connection') {
            steps {
                script {
                    dir("$REPO_DIR/API") {
                        sh 'docker compose build'
                    }
                    
                    docker.image('francescoxx/flask_live_app:1.0.0').withRun(
                        "-p 4000:4000 --name flask_app --link flask_db -e DB_URL=${env.DB_URL}"
                    ) { c ->
                        sh """
                        docker exec flask_app python3 -c \\
                        "import psycopg2; \\
                        conn = psycopg2.connect('${env.DB_URL}'); \\
                        print('Conexión exitosa'); \\
                        conn.close()"
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                sh 'docker rm -f flask_app || true'
                sh 'docker rm -f flask_db || true'
                sh 'docker volume rm pgdata || true'
            }
        }
    }
}