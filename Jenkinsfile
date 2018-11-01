#!/usr/bin/env groovy

pipeline {
    agent none

    stages {
        stage('Validate') {
            agent {
                dockerfile {
                    additionalBuildArgs '--target build'
                }
            }
            environment {
                OUTPUT_FILE = 'pylint.out'
            }
            steps {
                sh "./lint.py $OUTPUT_FILE"
            }
            post {
                always {
                    warnings canRunOnFailed: true, parserConfigurations: [[parserName: 'PyLint', pattern: OUTPUT_FILE]]
                }
            }
        }
    }
}