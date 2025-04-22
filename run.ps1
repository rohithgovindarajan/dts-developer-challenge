# run.ps1

# 1) Activate venv if it exists
if (Test-Path .venv\Scripts\Activate.ps1) {
    . .\.venv\Scripts\Activate.ps1
}

# 2) Locate script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

# 3) Export environment variables
$Env:FLASK_APP                = 'uk.gov.hmcts.reform.dev.Application'
$Env:FLASK_ENV                = 'development'
$Env:PYTHONPATH               = "$scriptDir\src\main\python"
$Env:BASIC_AUTH_USERNAME      = 'admin'
$Env:BASIC_AUTH_PASSWORD      = 'secret'

# 4) Database migrations
Push-Location $scriptDir
if (!(Test-Path "$scriptDir\migrations")) {
    Write-Host "Initializing migrations..."
    flask db init
}
Write-Host "Generating and applying migrations..."
flask db migrate -m "auto" 
flask db upgrade
Pop-Location

# 5) Run tests
Write-Host "Running root‑level tests..."
& python "$scriptDir\test.py" -v

Write-Host "Running package‑based tests..."
& python "$scriptDir\src\test\python\uk\gov\hmcts\reform\dev\test_tasks.py" -v

# 6) Start the Flask server
Write-Host "Starting Flask server at http://localhost:5000/"
flask run --host=0.0.0.0 --port=5000
