pipeline {
    agent any

    triggers {
        // Fires on every GitHub push (needs the GitHub webhook -> http://<EC2-IP>:8080/github-webhook/)
        githubPush()
    }

    environment {
        APP_NAME = 'flask-backend'
        APP_DIR  = '/opt/apps/flask-backend'
        // Optional: sensitive values from Jenkins > Manage Jenkins > Credentials (Secret text, ID: flask-api-key)
        // API_KEY = credentials('flask-api-key')
    }

    stages {
        stage('Pull Latest Code') {
            steps {
                checkout scm
                sh 'git log -1 --pretty="Commit: %h - %s (%an)"'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    python -m pytest tests -v
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    mkdir -p "$APP_DIR"
                    rsync -a --delete --exclude '.git' --exclude '.venv' --exclude 'venv' ./ "$APP_DIR"/
                    cd "$APP_DIR"
                    python3 -m venv venv
                    venv/bin/pip install -r requirements.txt
                    pm2 startOrRestart ecosystem.config.js --update-env
                    pm2 save
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    sleep 3
                    curl -fsS http://localhost:5000/health
                '''
            }
        }
    }

    post {
        success { echo 'Flask backend deployed successfully.' }
        failure { echo 'Flask pipeline failed - check the console output above.' }
    }
}
