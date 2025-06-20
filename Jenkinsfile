pipeline {
    agent any
    environment {
        REGISTRY = 'registry.softwarepro.solutions'
        IMAGE_NAME = 'cora'
        VERSION = "v${BUILD_NUMBER}"
        USER_PROD = 'ubuntu'
        SERVER_PROD = 'ec2-34-207-192-15.compute-1.amazonaws.com'
    }

    stages {
        stage('Inicializando...') {
            steps {
                echo 'Asignando workspace y validando entorno.'
            }
        }
        stage('Entorno de desarrollo') {
            steps {
                sh 'docker compose up -d --build'
                //sh 'chmod +x script_jenkins.sh'
            }
        }
        stage('Analisis de codigo') {
            steps {
                sh 'docker exec easy-chair-uaz-web flake8 --max-complexity=10 --max-line-length=200 --ignore=F811,E402 .'
                echo 'ok'
            }
        }
        stage('Pruebas Unitarias') {
            steps {
                timeout(time: 20, unit: 'MINUTES') {
                    sleep time: 20, unit: 'SECONDS'
                    //sh 'docker exec easy-chair-uaz-web python3 manage.py test' 
                    sh """docker exec easy-chair-uaz-web bash -c "coverage run --branch --source='.' --omit=*test*,*migrations*,*__init*,*settings*,*apps*,*wsgi*,*admin.py,*asgi.py,manage.py,*urls.py manage.py test" """
                    sh 'docker exec easy-chair-uaz-web coverage html'
                    sh 'docker cp easy-chair-uaz-web:/code/htmlcov . || true'

                    publishHTML target:[
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: './htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Reporte de cobertura CORA',
                        reportTitles: 'Cobertura de código'
                    ]
                }
            }
        }
        stage('Pruebas de aceptacion') {
            steps {
                sh 'docker exec easy-chair-uaz-web python manage.py migrate'
                //sh 'docker exec -w /pruebas_aceptacion easy-chair-uaz-web behave CORA/features/login_cora.feature'
            }
        }
        stage('Limpiando') {
            steps {
                sh 'docker compose down -v'
            }
        }
    }
}
