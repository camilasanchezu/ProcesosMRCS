pipeline {
    agent any

    options {
        skipDefaultCheckout()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        VENV_PATH = "${WORKSPACE}\\.venv"
    DEPLOY_PATH = 'C:\\deploy\\python_ci_app'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Clonando el repositorio...'
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Preparando entorno virtual...'
                bat 'if not exist TestResults mkdir TestResults'
                bat '''
python -m venv .venv
call .venv\\Scripts\\activate
pip install --upgrade pip
pip install -r requirements.txt
'''
            }
        }

        stage('Build Application') {
            steps {
                echo 'Construyendo artefactos (compilación bytecode)...'
                bat '''
call .venv\\Scripts\\activate
python -m compileall app
'''
                stash includes: 'app/**', name: 'app-source'
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Ejecutando pruebas unitarias...'
                bat '''
call .venv\\Scripts\\activate
pytest --junitxml=TestResults\\pytest-results.xml
'''
                junit 'TestResults/pytest-results.xml'
            }
        }

        stage('Code Quality - Flake8') {
            steps {
                echo 'Analizando calidad de código con flake8...'
                bat '''
call .venv\\Scripts\\activate
flake8 app tests --statistics --output-file=TestResults\\flake8-report.txt
'''
                archiveArtifacts artifacts: 'TestResults/flake8-report.txt', allowEmptyArchive: false
            }
        }

        stage('Deploy (main)') {
            when {
                branch 'main'
            }
            steps {
                echo 'Despliegue simulado al entorno de producción...'
                unstash 'app-source'
                bat 'if not exist %DEPLOY_PATH% mkdir %DEPLOY_PATH%'
                bat 'xcopy /E /I /Y app %DEPLOY_PATH%\\app'
            }
        }
    }

    post {
        always {
            echo "Limpieza final: estado ${currentBuild.currentResult}."
            archiveArtifacts artifacts: 'TestResults/**', allowEmptyArchive: true
            // Notificar solo por email si se definieron destinatarios en EMAIL_RECIPIENTS
            script {
                try {
                    if (env.EMAIL_RECIPIENTS) {
                        echo "Enviando notificación por email a: ${env.EMAIL_RECIPIENTS}"
                        emailext subject: "[Jenkins] ${env.JOB_NAME} #${env.BUILD_NUMBER} - ${currentBuild.currentResult}",
                                 body: "Job: ${env.JOB_NAME}\nBuild: ${env.BUILD_NUMBER}\nResultado: ${currentBuild.currentResult}\nURL: ${env.BUILD_URL}",
                                 to: env.EMAIL_RECIPIENTS
                    } else {
                        echo 'EMAIL_RECIPIENTS no configurado — omitiendo notificación por email.'
                    }
                } catch (ee) {
                    echo "Fallo al enviar email: ${ee}"
                }
            }
        }

        success {
            echo 'Pipeline completado correctamente.'
        }

        failure {
            echo 'El pipeline falló.'
        }
    }
}
