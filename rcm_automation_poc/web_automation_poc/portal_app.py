from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Very simple login page and dashboard
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head><title>Insurance Portal Login</title></head>
<body>
    <h2>Login to Claims Portal</h2>
    <form method="post" action="/login">
        <input type="text" name="username" placeholder="Username" id="user"><br>
        <input type="password" name="password" placeholder="Password" id="pass"><br>
        <button type="submit" id="login-btn">Login</button>
    </form>
    {% if error %}<p style="color:red;" id="error">{{ error }}</p>{% endif %}
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head><title>Claims Dashboard</title></head>
<body>
    <h2>Claims Status Table</h2>
    <table border="1" id="claims-table">
        <tr><th>Claim ID</th><th>Patient</th><th>Status</th></tr>
        <tr><td>98765</td><td>John Doe</td><td>Paid</td></tr>
        <tr><td>12345</td><td>Jane Smith</td><td>Processing</td></tr>
        <tr><td>55555</td><td>Bob Brown</td><td>Denied</td></tr>
    </table>
</body>
</html>
"""

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "password123":
            return redirect(url_for("dashboard"))
        return render_template_string(LOGIN_HTML, error="Invalid Credentials")
    return render_template_string(LOGIN_HTML)

@app.route("/dashboard")
def dashboard():
    return render_template_string(DASHBOARD_HTML)

if __name__ == "__main__":
    app.run(port=5000)
