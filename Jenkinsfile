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
            // Intentar notificar por Slack si SLACK_CHANNEL está configurado; si falla, usar webhook (sin plugin)
            script {
                def msg = "${env.JOB_NAME} #${env.BUILD_NUMBER} finalizó con estado: ${currentBuild.currentResult} - ${env.BUILD_URL}"
                def color = currentBuild.currentResult == 'SUCCESS' ? 'good' : (currentBuild.currentResult == 'FAILURE' ? 'danger' : 'warning')
                try {
                    if (env.SLACK_CHANNEL) {
                        // Intentamos slackSend (requiere Slack plugin). Si el plugin no existe, atrapamos la excepción.
                        slackSend channel: env.SLACK_CHANNEL, color: color, message: msg
                        echo 'Enviado mensaje vía slackSend.'
                    } else {
                        throw new Exception('SLACK_CHANNEL no configurado')
                    }
                } catch (e) {
                    echo "Slack not available or failed: ${e}. Attempting webhook fallback."
                    try {
                        // Fallback: usar webhook guardado en credencial NOTIFY_WEBHOOK (Secret text)
                        withCredentials([string(credentialsId: 'NOTIFY_WEBHOOK', variable: 'WEBHOOK_URL')]) {
                            powershell(returnStdout: true, script: """
$payload = ConvertTo-Json @{ text = '${msg}' }
Invoke-RestMethod -Uri '$env:WEBHOOK_URL' -Method Post -Body $payload -ContentType 'application/json'
""")
                            echo 'Notificación enviada via webhook.'
                        }
                    } catch (e2) {
                        echo "Webhook notification failed or NOTIFY_WEBHOOK not configured: ${e2}"
                    }
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
