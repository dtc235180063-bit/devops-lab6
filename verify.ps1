# ============================================================
# verify.ps1 - Script kiem tra ket qua Lab 6 (PowerShell)
# ============================================================
$global:pass = 0
$global:fail = 0
$global:total = 0

function Check-Item([string]$desc, [string]$status) {
    $global:total++
    Write-Host "[$global:total] $desc ... " -NoNewline
    if ($status -eq 'OK') {
        Write-Host "PASS" -ForegroundColor Green
        $global:pass++
    } else {
        Write-Host "FAIL: $status" -ForegroundColor Red
        $global:fail++
    }
}

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  VERIFY - Lab 6 Testing & Static Analysis" -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Ensure D:\nodejs in PATH if present
if ((Test-Path "D:\nodejs") -and ($env:Path -notlike "*D:\nodejs*")) {
    $env:Path = "$env:Path;D:\nodejs;$env:APPDATA\npm"
}

# Node.js
$node = Get-Command node -ErrorAction SilentlyContinue
if ($node) { Check-Item "Node.js installed ($(node -v))" 'OK' } else { Check-Item "Node.js installed" 'Not found' }

# Newman
$newman = Get-Command newman -ErrorAction SilentlyContinue
if ($newman) { Check-Item "Newman CLI installed ($(newman --version))" 'OK' } else { Check-Item "Newman CLI installed" 'Run npm install -g newman' }

# Server.js
if (Test-Path "server.js") { Check-Item "server.js exists" 'OK' } else { Check-Item "server.js exists" 'Missing server.js' }

# Postman collection
if (Test-Path "Student-API-Tests.json") {
    $json = Get-Content "Student-API-Tests.json" -Raw | ConvertFrom-Json
    $count = $json.item.Count
    if ($count -ge 5) { Check-Item "Postman collection has >=5 requests ($count)" 'OK' } else { Check-Item "Postman collection" "Only $count requests" }
} else { Check-Item "Student-API-Tests.json exists" 'Missing file' }

# Sonar config
if (Test-Path "sonar-project.properties") { Check-Item "sonar-project.properties exists" 'OK' } else { Check-Item "sonar-project.properties exists" 'Missing file' }

# Newman report
if (Test-Path "newman-report.json") { Check-Item "newman-report.json exists" 'OK' } else { Check-Item "newman-report.json exists" 'Missing file' }

# ZAP report
if (Test-Path "zap-report.html") { Check-Item "zap-report.html exists" 'OK' } else { Check-Item "zap-report.html exists" 'Missing file' }

# CI scripts
if (Test-Path "ci-test.sh") { Check-Item "ci-test.sh exists" 'OK' } else { Check-Item "ci-test.sh exists" 'Missing file' }
if (Test-Path "ci-test.ps1") { Check-Item "ci-test.ps1 exists" 'OK' } else { Check-Item "ci-test.ps1 exists" 'Missing file' }

# Screenshots
$screens = @("01-newman-pass.png", "02-zap-alerts.png", "03-sonarqube-dashboard.png", "04-sonarqube-issues.png", "05-comparison-table.png")
$foundScreens = 0
foreach ($s in $screens) {
    if (Test-Path "screenshots/$s") { $foundScreens++ }
}
if ($foundScreens -ge 5) { Check-Item "All 5 required screenshots exist in screenshots/" 'OK' } else { Check-Item "Screenshots check" "Only $foundScreens/5 found" }

# Student info report
if (Test-Path "ho_ten_mssv.txt") { Check-Item "ho_ten_mssv.txt exists" 'OK' } else { Check-Item "ho_ten_mssv.txt exists" 'Missing file' }

# README
if (Test-Path "README.md") { Check-Item "README.md exists" 'OK' } else { Check-Item "README.md exists" 'Missing README.md' }

Write-Host ""
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  RESULTS: $global:pass/$global:total PASS, $global:fail FAIL" -ForegroundColor $(if ($global:fail -eq 0) { 'Green' } else { 'Yellow' })
Write-Host "===============================================" -ForegroundColor Cyan
if ($global:fail -eq 0) { Write-Host " All checks PASS (100%)!" -ForegroundColor Green }
