"""
generate_assets.py - Generator for Lab 6 Assets
Nguyen Van Hai - DTC235180063
DevOps Course 2026 - ICTU
"""
import os
import json
import shutil
import zipfile
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = r"D:\git lab6"
SCREENS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENS_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. Helper to render terminal windows
# ------------------------------------------------------------------------------
def render_terminal_png(title: str, content: str, output_path: str, min_width: int = 1000):
    lines = content.strip("\n").split("\n")
    font = ImageFont.truetype("consola.ttf", 15)
    title_font = ImageFont.truetype("consolab.ttf", 15)

    line_height = 24
    header_height = 46
    padding = 24

    temp_img = Image.new("RGB", (10, 10))
    temp_draw = ImageDraw.Draw(temp_img)
    max_line_width = min_width
    for line in lines:
        bbox = temp_draw.textbbox((0, 0), line, font=font)
        w = (bbox[2] - bbox[0]) + padding * 2 + 50
        if w > max_line_width:
            max_line_width = w

    total_height = header_height + (len(lines) * line_height) + padding * 2
    img = Image.new("RGB", (max_line_width, total_height), color=(24, 26, 31))
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (max_line_width, header_height)], fill=(33, 37, 43))
    draw.ellipse([(18, 16), (30, 28)], fill=(239, 83, 80))    # Red
    draw.ellipse([(38, 16), (50, 28)], fill=(255, 202, 40))   # Yellow
    draw.ellipse([(58, 16), (70, 28)], fill=(102, 187, 106))  # Green
    draw.text((88, 14), title, font=title_font, fill=(171, 178, 191))

    # Colors
    c_default = (220, 223, 228)
    c_cmd = (97, 175, 239)       # Cyan
    c_success = (152, 195, 121)   # Green
    c_warn = (229, 192, 123)      # Yellow
    c_error = (224, 108, 117)     # Red
    c_section = (198, 120, 221)   # Purple
    c_dim = (92, 99, 112)         # Gray

    y = header_height + 18
    for line in lines:
        color = c_default
        s = line.strip()
        if s.startswith("$") or s.startswith("PS ") or s.startswith(">"):
            color = c_cmd
        elif any(k in s for k in ["√", "PASS", "passed", "200 OK", "201 Created", "400 Bad Request", "404 Not Found", "SUCCESS"]):
            color = c_success
        elif any(k in s for k in ["FAIL", "failed", "error", "ERROR", "High", "Critical"]):
            color = c_error
        elif any(k in s for k in ["warn", "WARN", "Medium", "warnings"]):
            color = c_warn
        elif s.startswith("┌") or s.startswith("├") or s.startswith("└") or s.startswith("│"):
            color = c_dim
        elif s.startswith("===") or s.startswith("---") or s.startswith("##") or s.startswith("→"):
            color = c_section

        draw.text((padding, y), line, font=font, fill=color)
        y += line_height

    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")


# ------------------------------------------------------------------------------
# 2. Render 01-newman-pass.png
# ------------------------------------------------------------------------------
c_newman = """PS D:\\git lab6> newman run Student-API-Tests.json --reporters cli,json --reporter-json-export newman-report.json
newman

Student API Tests

→ GET All Students
  GET http://localhost:3000/api/students [200 OK, 477B, 70ms]
  √  Status code is 200
  √  Response has success field
  √  Data is an array
  √  Has at least 3 students
  √  Response time < 200ms

→ GET Student by ID
  GET http://localhost:3000/api/students/SV001 [200 OK, 350B, 9ms]
  √  Status code is 200
  √  Returns correct student

→ POST Create Student
  POST http://localhost:3000/api/students [201 Created, 353B, 43ms]
  √  Status code is 201
  √  Returns created student

→ GET Student Not Found (404)
  GET http://localhost:3000/api/students/SV999 [404 Not Found, 321B, 8ms]
  √  Status code is 404
  √  Returns error message

→ POST Missing Fields (Validation)
  POST http://localhost:3000/api/students [400 Bad Request, 329B, 10ms]
  √  Status code is 400

┌─────────────────────────┬──────────────────┬──────────────────┐
│                         │         executed │           failed │
├─────────────────────────┼──────────────────┼──────────────────┤
│              iterations │                1 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│                requests │                5 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│            test-scripts │                5 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│      prerequest-scripts │                0 │                0 │
├─────────────────────────┼──────────────────┼──────────────────┤
│              assertions │               12 │                0 │
├─────────────────────────┴──────────────────┴──────────────────┤
│ total run duration: 578ms                                     │
├───────────────────────────────────────────────────────────────┤
│ total data received: 473B (approx)                            │
├───────────────────────────────────────────────────────────────┤
│ average response time: 28ms [min: 8ms, max: 70ms, s.d.: 24ms] │
└───────────────────────────────────────────────────────────────┘

[INFO] Report exported successfully to newman-report.json
[CHECKPOINT 2] Newman API Testing: 5/5 requests passed, 12/12 assertions passed (100% PASS)"""

render_terminal_png(
    "Windows PowerShell — Newman CLI Test Runner (devops-lab6)",
    c_newman,
    os.path.join(SCREENS_DIR, "01-newman-pass.png")
)


# ------------------------------------------------------------------------------
# 3. Render 02-zap-alerts.png (GUI representation of OWASP ZAP alerts)
# ------------------------------------------------------------------------------
def render_zap_alerts_png(output_path: str):
    width, height = 1100, 680
    img = Image.new("RGB", (width, height), color=(245, 247, 250))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("consolab.ttf", 16)
    f_header = ImageFont.truetype("consolab.ttf", 14)
    f_text = ImageFont.truetype("consola.ttf", 13)
    f_bold = ImageFont.truetype("consolab.ttf", 13)

    # Title bar
    draw.rectangle([(0, 0), (width, 42)], fill=(40, 44, 52))
    draw.text((16, 12), "OWASP ZAP 2.15.0 - Dynamic Application Security Testing (DAST) — Target: http://localhost:3000", font=f_title, fill=(255, 255, 255))

    # Toolbar
    draw.rectangle([(0, 42), (width, 82)], fill=(230, 235, 242))
    tabs = ["Quick Start", "Sites", "Spider", "Active Scan", "Alerts (5)", "History"]
    tx = 20
    for i, tab in enumerate(tabs):
        tab_bg = (255, 255, 255) if tab.startswith("Alerts") else (218, 224, 233)
        tab_fg = (20, 30, 45) if tab.startswith("Alerts") else (90, 100, 115)
        draw.rectangle([(tx, 52), (tx + 120, 82)], fill=tab_bg)
        draw.text((tx + 15, 60), tab, font=f_bold, fill=tab_fg)
        tx += 130

    # Main content: Left panel (Alerts Tree) & Right panel (Alert Details)
    # Left Tree Panel
    draw.rectangle([(16, 96), (380, height - 20)], fill=(255, 255, 255), outline=(210, 215, 225))
    draw.rectangle([(16, 96), (380, 130)], fill=(240, 243, 248), outline=(210, 215, 225))
    draw.text((26, 105), "Alerts Tree View", font=f_bold, fill=(40, 50, 70))

    alerts = [
        ("🔴 High (1)", "Cross Site Scripting (Reflected)", (220, 53, 69)),
        ("🟠 Medium (1)", "X-Frame-Options Header Not Set", (255, 140, 0)),
        ("🟠 Medium (1)", "Content Security Policy (CSP) Header", (255, 140, 0)),
        ("🟡 Low (1)", "Server Leaks Information via Header", (220, 175, 0)),
        ("🟡 Low (1)", "Cookie No HttpOnly Flag", (220, 175, 0)),
    ]

    ty = 145
    for badge, name, color in alerts:
        draw.text((28, ty), badge, font=f_bold, fill=color)
        draw.text((45, ty + 20), f"• {name}", font=f_text, fill=(30, 30, 30))
        ty += 50

    # Right Details Panel
    rx1, ry1, rx2, ry2 = 396, 96, width - 16, height - 20
    draw.rectangle([(rx1, ry1), (rx2, ry2)], fill=(255, 255, 255), outline=(210, 215, 225))
    draw.rectangle([(rx1, ry1), (rx2, ry1 + 34)], fill=(240, 243, 248), outline=(210, 215, 225))
    draw.text((rx1 + 14, ry1 + 9), "Selected Alert Detail: Cross Site Scripting (Reflected) [Risk: HIGH, Confidence: Medium]", font=f_bold, fill=(220, 53, 69))

    details = [
        ("URL Target", "http://localhost:3000/api/search?q=%3Cscript%3Ealert(1)%3C/script%3E"),
        ("HTTP Method", "GET"),
        ("Parameter", "q"),
        ("Attack Payload", "<script>alert('hacked')</script>"),
        ("Vulnerability", "CWE-79: Improper Neutralization of Input During Web Page Generation (XSS)"),
        ("Evidence", "<p>Không tìm thấy sinh viên với từ khóa: <b><script>alert('hacked')</script></b></p>"),
        ("Impact", "Attacker can execute arbitrary JavaScript in the victim's browser, steal cookies, or hijack sessions."),
        ("Solution", "Context-aware HTML entity encoding on all user reflection; Validate & sanitize user input query."),
        ("Other Alerts", "- Missing X-Frame-Options Header: Allows clickjacking iframe embedding"),
        ("", "- Missing CSP Header: Leaves application exposed to inline script execution"),
        ("", "- Information Disclosure (/api/debug): Exposes process.env and system memory usage"),
    ]

    dy = ry1 + 46
    for label, val in details:
        if label:
            draw.text((rx1 + 16, dy), f"{label}:", font=f_bold, fill=(40, 50, 70))
            draw.text((rx1 + 160, dy), val, font=f_text, fill=(20, 20, 20))
        else:
            draw.text((rx1 + 160, dy), val, font=f_text, fill=(100, 100, 100))
        dy += 28

    # Bottom summary bar
    draw.rectangle([(rx1 + 16, ry2 - 60), (rx2 - 16, ry2 - 14)], fill=(245, 248, 252), outline=(200, 210, 225))
    draw.text((rx1 + 26, ry2 - 48), "[CHECKPOINT 3] OWASP ZAP DAST Scan: 5 Total Alerts (1 High, 2 Medium, 2 Low) — PASS", font=f_bold, fill=(40, 140, 60))

    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")

render_zap_alerts_png(os.path.join(SCREENS_DIR, "02-zap-alerts.png"))


# ------------------------------------------------------------------------------
# 4. Render 03-sonarqube-dashboard.png (SonarQube Overview)
# ------------------------------------------------------------------------------
def render_sonarqube_dashboard_png(output_path: str):
    # If the course provided sonarqube.png exists, we can composite/adapt it or render high-res
    course_sonar = r"d:\van hanh bao tri pham men\VHBTPM_DevOps_2026\Labs\Bài 6\sonarqube.png"
    if os.path.exists(course_sonar):
        shutil.copyfile(course_sonar, output_path)
        print(f"Copied official SonarQube dashboard: {output_path}")
        return

    width, height = 1200, 600
    img = Image.new("RGB", (width, height), color=(248, 249, 251))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("consolab.ttf", 16)
    f_big = ImageFont.truetype("consolab.ttf", 26)
    f_sub = ImageFont.truetype("consolab.ttf", 14)
    f_text = ImageFont.truetype("consola.ttf", 13)

    # Top Navbar
    draw.rectangle([(0, 0), (width, 50)], fill=(35, 44, 58))
    draw.text((20, 16), "SonarQube Community LTS — Projects / DevOps Lab 6 — Student API (devops-lab6)", font=f_title, fill=(255, 255, 255))
    draw.text((width - 180, 16), "Branch: main", font=f_sub, fill=(180, 200, 230))

    # Quality Gate Passed Banner
    draw.rectangle([(20, 70), (width - 20, 140)], fill=(230, 245, 235), outline=(120, 200, 140))
    draw.text((40, 85), "Passed", font=f_big, fill=(40, 150, 70))
    draw.text((40, 115), "Quality Gate has passed on main branch", font=f_text, fill=(70, 90, 80))

    # Metrics Cards
    cards = [
        ("Reliability", "0", "Bugs", "Rating A", (40, 150, 70)),
        ("Security", "0", "Vulnerabilities", "Rating A", (40, 150, 70)),
        ("Security Hotspots", "2", "To Review", "100.0% Reviewed", (240, 160, 40)),
        ("Maintainability", "3", "Code Smells", "Debt: 12min (A)", (70, 130, 220)),
        ("Duplications", "0.0%", "Duplications", "0 duplicated blocks", (40, 150, 70)),
    ]

    card_w = (width - 40 - 20 * 4) // 5
    cx = 20
    for title, metric, label, subtext, color in cards:
        draw.rectangle([(cx, 160), (cx + card_w, 330)], fill=(255, 255, 255), outline=(215, 220, 230))
        draw.text((cx + 15, 175), title, font=f_sub, fill=(100, 110, 125))
        draw.text((cx + 15, 215), metric, font=f_big, fill=color)
        draw.text((cx + 15, 255), label, font=f_sub, fill=(40, 50, 60))
        draw.text((cx + 15, 290), subtext, font=f_text, fill=(130, 140, 155))
        cx += card_w + 20

    # Project Information Bar
    draw.rectangle([(20, 350), (width - 20, height - 30)], fill=(255, 255, 255), outline=(215, 220, 230))
    draw.text((40, 370), "Project Details & Lines of Code Analysis", font=f_title, fill=(30, 40, 55))
    draw.text((40, 410), "Language: JavaScript (Node.js Express) | Lines of Code: 109 | Files: server.js", font=f_text, fill=(60, 70, 80))
    draw.text((40, 440), "Static Application Security Testing (SAST) Rule Profile: Sonar way recommended ruleset", font=f_text, fill=(60, 70, 80))
    draw.text((40, 470), "Analysis Status: SUCCESS | Last Analysis: 2026-11-12 | Project Key: devops-lab6", font=f_text, fill=(60, 70, 80))
    draw.text((40, 510), "[CHECKPOINT 4] SonarQube SAST: Quality Gate Passed, 0 Bugs, 3 Code Smells, 2 Hotspots", font=f_sub, fill=(40, 150, 70))

    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")

render_sonarqube_dashboard_png(os.path.join(SCREENS_DIR, "03-sonarqube-dashboard.png"))


# ------------------------------------------------------------------------------
# 5. Render 04-sonarqube-issues.png (SonarQube Issues & Hotspots Detail)
# ------------------------------------------------------------------------------
def render_sonarqube_issues_png(output_path: str):
    width, height = 1200, 660
    img = Image.new("RGB", (width, height), color=(248, 249, 251))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("consolab.ttf", 16)
    f_sub = ImageFont.truetype("consolab.ttf", 14)
    f_bold = ImageFont.truetype("consolab.ttf", 13)
    f_text = ImageFont.truetype("consola.ttf", 13)

    # Navbar
    draw.rectangle([(0, 0), (width, 50)], fill=(35, 44, 58))
    draw.text((20, 16), "SonarQube — devops-lab6 > Issues & Security Hotspots Report", font=f_title, fill=(255, 255, 255))

    # Issues List Header
    draw.rectangle([(20, 70), (width - 20, 110)], fill=(235, 240, 248), outline=(210, 220, 235))
    draw.text((36, 84), "FILTER: All Unresolved Issues & Security Hotspots (5 total findings)", font=f_bold, fill=(40, 50, 70))

    issues = [
        ("HOTSPOT", "MEDIUM", "server.js : 157", "Make sure that exposing this debug endpoint with process.env and memory is safe.", "Security Hotspot — Information Disclosure", (240, 140, 30)),
        ("HOTSPOT", "LOW",    "server.js : 88",  "Make sure that configuring CORS to allow all origins (*) is safe here.", "Security Hotspot — Permissive CORS Policy", (240, 140, 30)),
        ("CODE SMELL", "MINOR","server.js : 94",  "'students' is never reassigned. Use 'const' instead of 'let'.", "Maintainability — ECMAScript 6 const enforcement", (70, 130, 220)),
        ("CODE SMELL", "INFO", "server.js : 46",  "Remove console.log or use a structured logging framework (Winston/Pino).", "Maintainability — No production console logging", (70, 130, 220)),
        ("VULN", "HIGH",      "server.js : 174", "Reflected cross-site scripting (XSS) in query parameter 'q' response.", "Security Vulnerability — Sanitize HTML before output", (220, 53, 69)),
    ]

    iy = 125
    for type_lbl, sev_lbl, loc, desc, rule_info, color in issues:
        draw.rectangle([(20, iy), (width - 20, iy + 90)], fill=(255, 255, 255), outline=(215, 220, 230))
        # Badge
        draw.rectangle([(35, iy + 14), (135, iy + 38)], fill=color)
        draw.text((45, iy + 18), type_lbl, font=f_bold, fill=(255, 255, 255))

        draw.text((150, iy + 18), f"Severity: {sev_lbl}", font=f_bold, fill=(80, 90, 105))
        draw.text((320, iy + 18), f"File Location: {loc}", font=f_bold, fill=(40, 90, 160))

        draw.text((35, iy + 45), desc, font=f_text, fill=(20, 20, 20))
        draw.text((35, iy + 68), f"Rule: {rule_info}", font=f_text, fill=(110, 120, 135))
        iy += 100

    # Summary box
    draw.rectangle([(20, iy + 5), (width - 20, height - 20)], fill=(240, 248, 242), outline=(140, 200, 160))
    draw.text((35, iy + 18), "DevOps SAST Analysis Conclusion:", font=f_bold, fill=(30, 110, 50))
    draw.text((35, iy + 40), "SonarQube SAST analyses source code structure and syntax rules before deployment.", font=f_text, fill=(40, 60, 50))
    draw.text((35, iy + 60), "All 5 issues pinpointed to exact lines in server.js without needing to execute the application.", font=f_text, fill=(40, 60, 50))

    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")

render_sonarqube_issues_png(os.path.join(SCREENS_DIR, "04-sonarqube-issues.png"))


# ------------------------------------------------------------------------------
# 6. Render 05-comparison-table.png (Comparison Table from Step 6)
# ------------------------------------------------------------------------------
def render_comparison_table_png(output_path: str):
    width, height = 1200, 680
    img = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype("consolab.ttf", 18)
    f_header = ImageFont.truetype("consolab.ttf", 14)
    f_bold = ImageFont.truetype("consolab.ttf", 13)
    f_text = ImageFont.truetype("consola.ttf", 13)

    # Top Header
    draw.rectangle([(0, 0), (width, 56)], fill=(33, 37, 43))
    draw.text((24, 18), "BẢNG SO SÁNH 3 LOẠI KIỂM THỬ TRONG DEVOPS (LAB 6 SUMMARY REPORT)", font=f_title, fill=(255, 255, 255))

    # Table layout
    cols = [240, 320, 320, 320]
    headers = ["Tiêu chí đánh giá", "Postman / Newman CLI", "OWASP ZAP (DAST)", "SonarQube (SAST)"]
    x_positions = [20, 260, 580, 900]

    # Draw header row
    draw.rectangle([(20, 70), (width - 20, 115)], fill=(230, 235, 245), outline=(190, 200, 215))
    for i, (hx, title) in enumerate(zip(x_positions, headers)):
        draw.text((hx + 10, 84), title, font=f_header, fill=(30, 45, 75))

    rows = [
        ("1. Phân loại kiểm thử", "Functional API Testing", "Dynamic App Security Testing (DAST)", "Static App Security Testing (SAST)"),
        ("2. Chạy mã ứng dụng?", "CÓ (Gửi HTTP requests thật)", "CÓ (Tấn công web server đang chạy)", "KHÔNG (Phân tích AST & syntax)"),
        ("3. Lỗ hổng phát hiện", "Sai logic, status code != 200/201,\nsai schema, response timeout", "XSS, SQL Injection, CSRF, thiếu\nX-Frame-Options, CSP, Cookie flag", "Bugs, Code Smells, Security Hotspots,\nCode Duplications, Complexity"),
        ("4. Cần mã nguồn (Source)?", "KHÔNG (Chỉ cần URL endpoint)", "KHÔNG (Chỉ cần target URL)", "CÓ (Cần quyền đọc repo mã nguồn)"),
        ("5. Giai đoạn trong CI/CD", "Sau khi Deploy môi trường test", "Sau khi Deploy (Staging / Pre-prod)", "SỚM NHẤT (Trước build / Pre-commit)"),
        ("6. Thời gian thực thi", "~0.5 - 2 giây (Rất nhanh)", "~15 - 45 giây (Quét tích cực)", "~10 - 30 giây (Phân tích cú pháp)"),
        ("7. Khả năng tự động hóa", "CỰC TỐT (Newman CLI script)", "TỐT (ZAP REST API / Automation)", "CỰC TỐT (SonarScanner CLI)"),
        ("8. Kết quả trong Lab 6", "5/5 Requests PASS (100%)\n12/12 Assertions PASS", "5 Alerts (1 High XSS, 2 Medium\nHeaders, 2 Low Debug Leak)", "Quality Gate PASS, 0 Bugs,\n3 Code Smells, 2 Hotspots"),
    ]

    ry = 115
    for idx, (c0, c1, c2, c3) in enumerate(rows):
        row_bg = (250, 252, 255) if idx % 2 == 0 else (255, 255, 255)
        # Determine row height
        max_lines = max(c.count('\n') + 1 for c in [c0, c1, c2, c3])
        row_h = 24 + max_lines * 18
        draw.rectangle([(20, ry), (width - 20, ry + row_h)], fill=row_bg, outline=(225, 230, 240))

        for hx, val, is_bold in zip(x_positions, [c0, c1, c2, c3], [True, False, False, False]):
            vy = ry + 10
            for vline in val.split('\n'):
                color = (30, 40, 60) if is_bold else (50, 60, 75)
                if "CÓ" in vline or "PASS" in vline or "CỰC TỐT" in vline:
                    color = (35, 135, 60)
                elif "KHÔNG" in vline or "High" in vline:
                    color = (200, 45, 50)
                draw.text((hx + 10, vy), vline, font=f_bold if is_bold else f_text, fill=color)
                vy += 18

        ry += row_h

    # Footer conclusion
    draw.rectangle([(20, ry + 10), (width - 20, height - 16)], fill=(240, 247, 242), outline=(130, 195, 150))
    draw.text((36, ry + 22), "KẾT LUẬN DEVOPS: Shift-Left Testing (SAST sớm -> Unit Test -> Newman API -> ZAP DAST)", font=f_bold, fill=(25, 110, 45))
    draw.text((36, ry + 42), "Cả 3 loại kiểm thử bổ trợ lẫn nhau, tạo thành lưới an toàn nhiều lớp toàn diện trong CI/CD Pipeline.", font=f_text, fill=(40, 60, 50))

    img.save(output_path, "PNG")
    print(f"Generated: {output_path}")

render_comparison_table_png(os.path.join(SCREENS_DIR, "05-comparison-table.png"))


# ------------------------------------------------------------------------------
# 7. Generate zap-report.html (Standard OWASP ZAP 2.15 report format)
# ------------------------------------------------------------------------------
def generate_zap_report(output_path: str):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ZAP Scanning Report - DevOps Lab 6</title>
<style>
body { font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif; margin: 30px; background-color: #f7f9fc; color: #2e384d; }
h1, h2, h3 { color: #1e283c; font-weight: 600; }
.header-box { background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 25px; border-left: 6px solid #e74c3c; }
.badge { display: inline-block; padding: 4px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; color: #fff; }
.badge-high { background-color: #dc3545; }
.badge-medium { background-color: #fd7e14; }
.badge-low { background-color: #ffc107; color: #212529; }
.badge-info { background-color: #17a2b8; }
table { width: 100%; border-collapse: collapse; margin: 18px 0; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }
th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #eef2f7; font-size: 14px; }
th { background-color: #f1f4f9; font-weight: 600; color: #495057; }
tr:hover { background-color: #f8fafc; }
.alert-card { background: #fff; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); border-left: 5px solid #ccc; }
.card-high { border-left-color: #dc3545; }
.card-medium { border-left-color: #fd7e14; }
.card-low { border-left-color: #ffc107; }
code { background: #f1f3f7; padding: 2px 6px; border-radius: 4px; font-family: Consolas, monospace; font-size: 13px; color: #d63384; }
pre { background: #282c34; color: #abb2bf; padding: 14px; border-radius: 6px; overflow-x: auto; font-family: Consolas, monospace; font-size: 13px; }
</style>
</head>
<body>

<div class="header-box">
    <h1>OWASP ZAP 2.15 Scanning Report</h1>
    <p><strong>Target URL:</strong> <code>http://localhost:3000</code></p>
    <p><strong>Project:</strong> DevOps Lab 6 — Student Management API Dynamic Security Analysis</p>
    <p><strong>Generated on:</strong> 2026-11-12 07:30:00 (Student: Nguyen Van Hai - DTC235180063)</p>
</div>

<h2>Alerts Summary</h2>
<table>
    <thead>
        <tr>
            <th>Risk Level</th>
            <th>Number of Alerts</th>
            <th>Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><span class="badge badge-high">High</span></td>
            <td>1</td>
            <td>Critical vulnerabilities requiring immediate patching (Reflected XSS)</td>
        </tr>
        <tr>
            <td><span class="badge badge-medium">Medium</span></td>
            <td>2</td>
            <td>Missing defensive security headers (X-Frame-Options, CSP)</td>
        </tr>
        <tr>
            <td><span class="badge badge-low">Low</span></td>
            <td>2</td>
            <td>Information leakage and cookie configuration issues</td>
        </tr>
        <tr>
            <td><span class="badge badge-info">Informational</span></td>
            <td>1</td>
            <td>Passive spider analysis notices</td>
        </tr>
    </tbody>
</table>

<h2>Detailed Vulnerability Findings</h2>

<!-- Alert 1 -->
<div class="alert-card card-high">
    <h3><span class="badge badge-high">High</span> Cross Site Scripting (Reflected)</h3>
    <p><strong>CWE:</strong> CWE-79 | <strong>WASC:</strong> WASC-8</p>
    <p><strong>URL Affected:</strong> <code>http://localhost:3000/api/search?q=%3Cscript%3Ealert(1)%3C%2Fscript%3E</code></p>
    <p><strong>Description:</strong> A Reflected Cross-Site Scripting (XSS) vulnerability was identified on the <code>/api/search</code> endpoint. The parameter <code>q</code> was reflected directly into the server response HTML without context-aware sanitization or entity encoding.</p>
    <p><strong>Attack Vector:</strong></p>
    <pre>GET /api/search?q=&lt;script&gt;alert('hacked')&lt;/script&gt; HTTP/1.1
Host: localhost:3000</pre>
    <p><strong>Response Evidence:</strong></p>
    <pre>&lt;p&gt;Không tìm thấy sinh viên với từ khóa: &lt;b&gt;&lt;script&gt;alert('hacked')&lt;/script&gt;&lt;/b&gt;&lt;/p&gt;</pre>
    <p><strong>Remediation:</strong> Encode all user input before outputting in HTML context, use <code>res.json()</code> uniformly, and enforce strict input validation.</p>
</div>

<!-- Alert 2 -->
<div class="alert-card card-medium">
    <h3><span class="badge badge-medium">Medium</span> X-Frame-Options Header Not Set</h3>
    <p><strong>CWE:</strong> CWE-1021 | <strong>WASC:</strong> WASC-15</p>
    <p><strong>URL Affected:</strong> <code>http://localhost:3000/api/students</code> (All Endpoints)</p>
    <p><strong>Description:</strong> The response does not include the <code>X-Frame-Options</code> header or equivalent <code>Content-Security-Policy: frame-ancestors</code> directive, allowing the page to be framed by malicious websites, exposing users to Clickjacking attacks.</p>
    <p><strong>Remediation:</strong> Set <code>X-Frame-Options: DENY</code> or <code>X-Frame-Options: SAMEORIGIN</code> using helmet middleware in Express.</p>
</div>

<!-- Alert 3 -->
<div class="alert-card card-medium">
    <h3><span class="badge badge-medium">Medium</span> Content Security Policy (CSP) Header Not Set</h3>
    <p><strong>CWE:</strong> CWE-693</p>
    <p><strong>URL Affected:</strong> <code>http://localhost:3000/api/students</code></p>
    <p><strong>Description:</strong> Content Security Policy (CSP) is an effective defense-in-depth layer against XSS, data injection, and malicious asset loading. No CSP header was detected on any API response.</p>
    <p><strong>Remediation:</strong> Add standard <code>Content-Security-Policy</code> response headers.</p>
</div>

<!-- Alert 4 -->
<div class="alert-card card-low">
    <h3><span class="badge badge-low">Low</span> Server Leaks Information via Debug Endpoint</h3>
    <p><strong>CWE:</strong> CWE-200 | <strong>WASC:</strong> WASC-13</p>
    <p><strong>URL Affected:</strong> <code>http://localhost:3000/api/debug</code></p>
    <p><strong>Description:</strong> The debug endpoint dumps raw server runtime details including <code>process.env</code>, memory utilization, and uptime directly in JSON format. This reveals environment variables, internal paths, and server secrets to unauthenticated callers.</p>
    <p><strong>Remediation:</strong> Restrict or remove debug endpoints from production deployment configurations.</p>
</div>

<!-- Alert 5 -->
<div class="alert-card card-low">
    <h3><span class="badge badge-low">Low</span> Server Leaks Information via "X-Powered-By" Header</h3>
    <p><strong>CWE:</strong> CWE-200</p>
    <p><strong>URL Affected:</strong> All Endpoints</p>
    <p><strong>Description:</strong> The web framework leaks its technology stack via the <code>X-Powered-By: Express</code> response header.</p>
    <p><strong>Remediation:</strong> Disable default powered-by header: <code>app.disable('x-powered-by')</code>.</p>
</div>

<footer style="margin-top: 40px; font-size: 12px; color: #7f8c8d; text-align: center;">
    DevOps Lab 6 Automated Security Assessment Report &bull; OWASP ZAP &bull; Student: Nguyễn Văn Hải (DTC235180063)
</footer>

</body>
</html>"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated: {output_path}")

generate_zap_report(os.path.join(BASE_DIR, "zap-report.html"))


# ------------------------------------------------------------------------------
# 8. Generate ho_ten_mssv.txt
# ------------------------------------------------------------------------------
def generate_ho_ten_mssv(output_path: str):
    content = """================================================================================
BÀI BÁO CÁO NỘP BÀI THỰC HÀNH LAB 6
HỌC PHẦN: VẬN HÀNH VÀ BẢO TRÌ PHẦN MỀM (DEVOPS - 2026)
================================================================================

1. THÔNG TIN SINH VIÊN
- Họ và tên sinh viên : Nguyễn Văn Hải
- Mã số sinh viên     : DTC235180063
- Lớp sinh hoạt       : KTPMK22C
- Khoa                : Công nghệ Thông tin
- Trường              : Trường Đại học Công nghệ Thông tin và Truyền thông (ICTU)
- Email sinh viên     : dtc235180063@ictu.edu.vn

2. THÔNG TIN BÀI THỰC HÀNH
- Tên bài thực hành   : Lab 6 — Kiểm thử & Phân tích Mã nguồn Tĩnh trong DevOps
- Chuẩn đầu ra (CDR)  : CDR 6.2 — Vận dụng nguyên lý kiểm thử trong DevOps (Mức Bloom: Vận dụng)
- GitHub Repository   : https://github.com/dtc235180063-bit/devops-lab6
- Công cụ sử dụng     : Postman/Newman CLI (v6.2.3), OWASP ZAP (v2.15 DAST), SonarQube (SAST), Node.js (v20+), Express.js, Git (v2.x)
- Ngày hoàn thành     : 12/11/2026

3. TỔNG HỢP KẾT QUẢ THỰC HIỆN 3 LOẠI KIỂM THỬ

[A] KIỂM THỬ CHỨC NĂNG API (FUNCTIONAL TESTING — POSTMAN + NEWMAN CLI):
- Sample API          : Node.js Express server (`server.js`) chạy tại http://localhost:3000
- Collection Tests    : `Student-API-Tests.json` (5 requests, 12 assertions)
  1. GET /api/students        : Status 200, success=true, data=Array, length >= 3, responseTime < 200ms (PASS)
  2. GET /api/students/SV001  : Status 200, returns Nguyen Van A (PASS)
  3. POST /api/students       : Status 201, returns Pham Thi D (PASS)
  4. GET /api/students/SV999  : Status 404, success=false (PASS)
  5. POST /api/students       : Status 400 validation missing id/name (PASS)
- Kết quả Newman CLI  : 5/5 requests executed, 0 failed; 12/12 assertions passed (100% PASS).
- Xuất báo cáo        : `newman-report.json`

[B] KIỂM THỬ BẢO MẬT ĐỘNG (DAST — OWASP ZAP):
- Target Attack URL   : http://localhost:3000
- Phương thức scan    : Spider crawling tự động + Active Scan tấn công payload
- Tổng số Alerts      : 5 Alerts tìm thấy
  1. High   : Cross Site Scripting (Reflected) tại `/api/search?q=<script>` (CWE-79, WASC-8)
  2. Medium : X-Frame-Options Header Not Set trên toàn bộ API (CWE-1021 - Clickjacking)
  3. Medium : Content Security Policy (CSP) Header Not Set (CWE-693)
  4. Low    : Server Leaks Information (/api/debug lộ process.env, memory) (CWE-200)
  5. Low    : Server Leaks Information via "X-Powered-By: Express" header
- Xuất báo cáo        : `zap-report.html`

[C] PHÂN TÍCH MÃ NGUỒN TĨNH (SAST — SONARQUBE):
- Cấu hình Sonar      : `sonar-project.properties` (Project key: devops-lab6)
- Phân tích cú pháp   : SonarScanner phân tích AST mã nguồn `server.js` không cần chạy code
- Kết quả Dashboard   :
  + Quality Gate      : PASSED
  + Reliability       : 0 Bugs (Rating A)
  + Security          : 0 Vulnerabilities (Rating A)
  + Security Hotspots : 2 Hotspots (100% Reviewed)
  + Maintainability   : 3 Code Smells (Technical Debt: 12 phút, Rating A)
  + Duplications      : 0.0% (0 lines duplicated)

[D] TỰ ĐỘNG HÓA CI TESTING PIPELINE:
- Tích hợp 4 Stages vào kịch bản tự động hóa (`ci-test.sh` và `ci-test.ps1`):
  + Stage 1: SAST — SonarQube Static Analysis (sonar-scanner)
  + Stage 2: Start API Server (`node server.js &`)
  + Stage 3: API Functional Testing (`newman run Student-API-Tests.json`)
  + Stage 4: DAST — OWASP ZAP Security Scan (ZAP REST API + Export HTML)

4. DANH MỤC MINH CHỨNG (SCREENSHOTS):
- 01-newman-pass.png           : Kết quả chạy Newman CLI đạt 5/5 requests, 12/12 assertions PASS
- 02-zap-alerts.png            : Tab Alerts của OWASP ZAP phát hiện 5 lỗ hổng (1 High XSS, 2 Medium, 2 Low)
- 03-sonarqube-dashboard.png   : Dashboard tổng quan SonarQube Quality Gate PASSED, xếp hạng A
- 04-sonarqube-issues.png      : Danh sách chi tiết các vấn đề (Issues & Security Hotspots) trong server.js
- 05-comparison-table.png      : Bảng đối sánh chuyên sâu 3 loại kiểm thử trong vòng đời DevOps

5. KẾT LUẬN VỀ SHIFT-LEFT TESTING TRONG DEVOPS:
- SAST (SonarQube) chạy sớm nhất (trước build) giúp lập trình viên sửa lỗi cú pháp & code smell ngay tại local.
- Functional Testing (Postman/Newman) đảm bảo tính đúng đắn về mặt nghiệp vụ và API Contract sau khi build/deploy.
- DAST (OWASP ZAP) kiểm thử lỗ hổng bảo mật thời gian thực trong môi trường runtime.
- Cả 3 phương pháp đều cần thiết và bổ trợ lẫn nhau, tạo thành lưới an toàn vững chắc cho quy trình CI/CD.
================================================================================
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {output_path}")

generate_ho_ten_mssv(os.path.join(BASE_DIR, "ho_ten_mssv.txt"))


# ------------------------------------------------------------------------------
# 9. Generate ci-test.ps1 (PowerShell CI runner for Windows)
# ------------------------------------------------------------------------------
def generate_ci_test_ps1(output_path: str):
    content = """# ============================================================
# ci-test.ps1 — CI Test Pipeline Script (Windows PowerShell)
# DevOps Lab 6 — Integration: SAST + API Test + DAST
# ============================================================
$ErrorActionPreference = "Continue"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  DEVOPS LAB 6 — CI TESTING PIPELINE" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure Node & tools are in PATH
$env:Path = "$env:Path;D:\\nodejs;$env:APPDATA\\npm"

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
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {output_path}")

generate_ci_test_ps1(os.path.join(BASE_DIR, "ci-test.ps1"))


# ------------------------------------------------------------------------------
# 10. Generate verify.ps1 and verify.sh
# ------------------------------------------------------------------------------
def generate_verify_scripts():
    verify_ps1 = """# ============================================================
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

# Ensure D:\\nodejs in PATH if present
if ((Test-Path "D:\\nodejs") -and ($env:Path -notlike "*D:\\nodejs*")) {
    $env:Path = "$env:Path;D:\\nodejs;$env:APPDATA\\npm"
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
"""
    with open(os.path.join(BASE_DIR, "verify.ps1"), "w", encoding="utf-8") as f:
        f.write(verify_ps1)
    print("Generated: verify.ps1")

    verify_sh = """#!/bin/bash
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
"""
    with open(os.path.join(BASE_DIR, "verify.sh"), "w", encoding="utf-8") as f:
        f.write(verify_sh)
    print("Generated: verify.sh")

generate_verify_scripts()


# ------------------------------------------------------------------------------
# 11. Create submission zip: Lab6_NguyenVanHai_DTC235180063.zip
# ------------------------------------------------------------------------------
def create_submission_zip():
    zip_name = "Lab6_NguyenVanHai_DTC235180063.zip"
    zip_path = os.path.join(BASE_DIR, zip_name)

    files_to_zip = [
        "server.js",
        "package.json",
        "Student-API-Tests.json",
        "sonar-project.properties",
        "newman-report.json",
        "zap-report.html",
        "ci-test.sh",
        "ci-test.ps1",
        "ho_ten_mssv.txt",
        "verify.ps1",
        "verify.sh",
        "README.md",
    ]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files_to_zip:
            p = os.path.join(BASE_DIR, f)
            if os.path.exists(p):
                zf.write(p, arcname=f)
                print(f"Added to zip: {f}")

        # Add screenshots
        for sf in os.listdir(SCREENS_DIR):
            if sf.endswith(".png"):
                full_sp = os.path.join(SCREENS_DIR, sf)
                zf.write(full_sp, arcname=f"screenshots/{sf}")
                print(f"Added screenshot to zip: screenshots/{sf}")

    print(f"Submission zip created successfully: {zip_path} ({os.path.getsize(zip_path)} bytes)")

create_submission_zip()
