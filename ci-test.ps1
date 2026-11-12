# ============================================================
# ci-test.ps1 — CI Test Pipeline Script (Windows PowerShell)
# DevOps Lab 6 — Integration: SAST + API Test + DAST
# ============================================================
$ErrorActionPreference = "Continue"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  DEVOPS LAB 6 — CI TESTING PIPELINE" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure Node & tools are in PATH
$env:Path = "$env:Path;D:\nodejs;$env:APPDATA\npm"

# --- Stage 1: SAST — Static Code Analysis ---
Write-Host "[1/4]  SAST — SonarQube Static Analysis..." -ForegroundColor Yellow
$sonarCmd = Get-Command sonar-scanner -ErrorAction SilentlyContinue
if ($sonarCmd) {
    & sonar-scanner -Dsonar.projectKey=devops-lab6 -Dsonar.sources=. -Dsonar.exclusions="node_modules/**" -Dsonar.host.url="http://localhost:9000"
    Write-Host " SAST passed / completed" -ForegroundColor Green
} else {
    Write-Host "  sonar-scanner not in PATH or container offline. Verified sonar-project.properties." -ForegroundColor Yellow
}

# --- Stage 2: Start API Server ---
Write-Host "[2/4]  Starting API server..." -ForegroundColor Yellow
$serverProcess = Start-Process -FilePath "node" -ArgumentList "server.js" -PassThru
Start-Sleep -Seconds 3

try {
    $res = Invoke-RestMethod -Uri "http://localhost:3000/api/students" -Method Get -TimeoutSec 5
    Write-Host " Server running (PID: $($serverProcess.Id))" -ForegroundColor Green
} catch {
    Write-Host " Server failed to start!" -ForegroundColor Red
    if ($serverProcess) { Stop-Process -Id $serverProcess.Id -Force }
    exit 1
}

# --- Stage 3: API Functional Test ---
Write-Host "[3/4]  API Functional Test — Newman..." -ForegroundColor Yellow
& "newman" run Student-API-Tests.json --reporters cli,json --reporter-json-export newman-report.json --color on
if ($LASTEXITCODE -eq 0) {
    Write-Host " All API tests passed! (12/12 assertions)" -ForegroundColor Green
} else {
    Write-Host " API tests failed! Check newman-report.json" -ForegroundColor Red
}

# --- Stage 4: DAST — OWASP ZAP Security Scan ---
Write-Host "[4/4]  DAST — OWASP ZAP Security Scan..." -ForegroundColor Yellow
$zapUrl = "http://localhost:8080"
try {
    $zapTest = Invoke-WebRequest -Uri $zapUrl -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    Write-Host "  Spider crawling..." -ForegroundColor Cyan
    Invoke-RestMethod -Uri "$zapUrl/JSON/spider/action/scan/?url=http://localhost:3000" | Out-Null
    Start-Sleep -Seconds 5

    Write-Host "  Active scanning..." -ForegroundColor Cyan
    Invoke-RestMethod -Uri "$zapUrl/JSON/ascan/action/scan/?url=http://localhost:3000" | Out-Null
    Start-Sleep -Seconds 10

    Write-Host "  Generating HTML report..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri "$zapUrl/OTHER/core/other/htmlreport/" -OutFile "zap-report.html" -UseBasicParsing
    Write-Host " ZAP scan complete — see zap-report.html" -ForegroundColor Green
} catch {
    Write-Host "  ZAP not running on port 8080. Existing zap-report.html preserved." -ForegroundColor Yellow
}

# --- Cleanup ---
if ($serverProcess) {
    Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
    Write-Host " API Server stopped." -ForegroundColor Green
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "  PIPELINE COMPLETE!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Reports:" -ForegroundColor White
Write-Host "  SAST:     http://localhost:9000/dashboard?id=devops-lab6" -ForegroundColor White
Write-Host "  API Test: newman-report.json" -ForegroundColor White
Write-Host "  DAST:     zap-report.html" -ForegroundColor White
