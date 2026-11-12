#!/bin/bash
# ============================================================
# verify.sh — Script kiểm tra kết quả Lab 6
# ============================================================
set -e

PASS=0; FAIL=0; TOTAL=0

check() {
    TOTAL=$((TOTAL + 1))
    echo -n "[$TOTAL] $1 ... "
    if [ "$2" = "OK" ]; then echo " PASS"; PASS=$((PASS + 1))
    else echo " $2"; FAIL=$((FAIL + 1)); fi
}

echo "==============================================="
echo "  VERIFY — Lab 6 Testing & Static Analysis"
echo "==============================================="
echo ""

# --- Tools ---
command -v node &>/dev/null && check "Node.js installed" "OK" || check "Node.js installed" "Not found"
command -v newman &>/dev/null && check "Newman CLI installed" "OK" || check "Newman CLI installed" "Run: npm install -g newman"

# --- Sample API ---
[ -f "server.js" ] && check "server.js exists" "OK" || check "server.js exists" "File not found"

# --- Postman Collection ---
if [ -f "Student-API-Tests.json" ]; then
    REQ_COUNT=$(python -c "import json; d=json.load(open('Student-API-Tests.json')); print(len(d['item']))" 2>/dev/null || echo "0")
    if [ "$REQ_COUNT" -ge 5 ]; then
        check "Postman collection has >=5 requests ($REQ_COUNT)" "OK"
    else
        check "Postman collection has >=5 requests" "Only $REQ_COUNT requests"
    fi
else
    check "Postman collection exists" "File not found"
fi

# --- Sonar config ---
[ -f "sonar-project.properties" ] && check "sonar-project.properties exists" "OK" || check "sonar-project.properties exists" "Not found"

# --- Newman report ---
[ -f "newman-report.json" ] && check "Newman report exists" "OK" || check "Newman report exists" "Not found"

# --- ZAP report ---
[ -f "zap-report.html" ] && check "ZAP report exists" "OK" || check "ZAP report exists" "Not found"

# --- CI Script ---
[ -f "ci-test.sh" ] && check "ci-test.sh exists" "OK" || check "ci-test.sh exists" "Not found"

# --- Screenshots ---
[ -d "screenshots" ] && [ $(ls screenshots/*.png 2>/dev/null | wc -l) -ge 5 ] && check "All 5 screenshots exist" "OK" || check "Screenshots check" "Missing screenshots"

# --- Student info ---
[ -f "ho_ten_mssv.txt" ] && check "ho_ten_mssv.txt exists" "OK" || check "ho_ten_mssv.txt exists" "Not found"

echo ""
echo "==============================================="
echo "  RESULTS: $PASS/$TOTAL PASS, $FAIL FAIL"
echo "==============================================="
[ "$FAIL" -eq 0 ] && echo " All checks PASS!" || echo " $FAIL issue(s) to fix"
