# 受保护的路由
@app.route('/admin/dashboard')
@role_required('admin')
def admin_dashboard():
    return "Admin Area"

# 用户注册（示例）
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201