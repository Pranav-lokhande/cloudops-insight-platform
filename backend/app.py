import os
import time
from datetime import datetime, timezone
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

def db_config():
    return {"host": os.getenv("DB_HOST","db"), "port": int(os.getenv("DB_PORT","3306")),
            "database": os.getenv("DB_NAME","cloudops"), "user": os.getenv("DB_USER","cloudops_app"),
            "password": os.getenv("DB_PASSWORD","change_this_app_password"), "connection_timeout": 4}

def connect_db(retries=8, delay=2):
    last_error = None
    for _ in range(retries):
        try: return mysql.connector.connect(**db_config())
        except Error as exc:
            last_error = exc
            time.sleep(delay)
    raise last_error

def initialize_table():
    conn=connect_db()
    try:
        cur=conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS services (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, category VARCHAR(40) NOT NULL, environment VARCHAR(30) NOT NULL, description VARCHAR(500) NOT NULL DEFAULT '', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        conn.commit(); cur.close()
    finally: conn.close()

@app.get("/api/health")
def health():
    try:
        conn=mysql.connector.connect(**db_config()); cur=conn.cursor()
        cur.execute("SELECT 1"); cur.fetchone(); cur.close(); conn.close()
        return jsonify(status="healthy",database="connected",timestamp=datetime.now(timezone.utc).isoformat())
    except Error:
        return jsonify(status="degraded",database="disconnected"),503

@app.get("/api/services")
def list_services():
    try:
        conn=connect_db(); cur=conn.cursor(dictionary=True)
        cur.execute("SELECT id,name,category,environment,description,DATE_FORMAT(created_at,'%Y-%m-%d %H:%i UTC') AS created_at FROM services ORDER BY id DESC LIMIT 100")
        rows=cur.fetchall(); cur.close(); conn.close()
        return jsonify(services=rows,count=len(rows))
    except Error:
        app.logger.exception("Unable to list services")
        return jsonify(error="Database unavailable. Please try again."),503

@app.post("/api/services")
def create_service():
    data=request.get_json(silent=True) or {}
    name=str(data.get("name","")).strip()
    category=str(data.get("category","Application")).strip()
    environment=str(data.get("environment","Development")).strip()
    description=str(data.get("description","")).strip()
    if not name or len(name)>100: return jsonify(error="Service name is required (maximum 100 characters)."),400
    if category not in {"Application","Database","Infrastructure","Monitoring","CI/CD","Security"}: return jsonify(error="Choose a valid category."),400
    if environment not in {"Development","Testing","Staging","Production"}: return jsonify(error="Choose a valid environment."),400
    if len(description)>500: return jsonify(error="Description must be 500 characters or fewer."),400
    try:
        conn=connect_db(); cur=conn.cursor()
        cur.execute("INSERT INTO services (name,category,environment,description) VALUES (%s,%s,%s,%s)",(name,category,environment,description))
        conn.commit(); new_id=cur.lastrowid; cur.close(); conn.close()
        return jsonify(message="Service created",id=new_id),201
    except Error:
        app.logger.exception("Unable to create service")
        return jsonify(error="Database unavailable. Your record was not saved."),503

@app.get("/metrics")
def metrics():
    try:
        conn=connect_db(); cur=conn.cursor(); cur.execute("SELECT COUNT(*) FROM services")
        count=cur.fetchone()[0]; cur.close(); conn.close()
        return ("# HELP cloudops_services_total Number of registered services\n# TYPE cloudops_services_total gauge\ncloudops_services_total %s\n"%count,200,{"Content-Type":"text/plain; version=0.0.4; charset=utf-8"})
    except Error:
        return ("cloudops_database_up 0\n",503,{"Content-Type":"text/plain; version=0.0.4; charset=utf-8"})

@app.get("/api")
def api_root():
    return jsonify(name="CloudOps Insight API",endpoints=["/api/health","/api/services","/metrics"])

try: initialize_table()
except Exception: app.logger.warning("Database initialization not ready at import; API requests will retry.")
