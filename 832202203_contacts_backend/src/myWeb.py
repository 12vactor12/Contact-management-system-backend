import json
import pymysql
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'mystring'



#logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    print(f"清空session")
    return redirect(url_for('sign'))

#--------------------------------------------------登录界面---------------------------------------------------------

@app.route('/sign', methods=['GET', "POST"])
def sign():
    if request.method == 'GET':
        print(f"/sign的GET请求")
        return render_template("sign.html")
    #前端点击注册或登录按钮时，执行以下操作
    if request.method == 'POST':
        print(f"/sign的POST请求{request.args.get('action')}")
        action = request.args.get('action')
        #注册
        if action == "Signup":
            username = request.args.get('username')
            email = request.args.get('email')
            password = request.args.get('password')
            # 检查用户名或邮箱是否已存在，存在返回True，否则返回False
            if not check_user_signuped(username, email):
                # 添加新用户到数据库
                add_user(username, email, password)
                # 直接登录
                user = get_user_by_username(username)
                session['user_id'] = user['id']
                return jsonify({"status": "success", "redirect_url": "/myweb"})
            else:
                # 假用户名或邮箱已存在
                return jsonify({"status": "error", "message": "用户名或邮箱已存在"})

        #登录
        elif action == "Signin":
            print(f"/sign的POST请求{request.args.get('action')}")
            username = request.args.get('username')
            password = request.args.get('password')
            # 验证用户名和密码是否正确
            exist = signin_check(username, password)
            if exist:
                # 登录成功，将用户ID存入session
                session['user_id'] = get_user_by_username(username)['id']
                # 如果登录成功，返回成功状态和主页URL
                return jsonify({"status": "success", "redirect_url": "/myweb"})
            else:
                # 假设用户名或密码错误
                return jsonify({"status": "error", "message": "用户名或密码错误"})



#--------------------------------------------------联系人管理界面---------------------------------------------------------



# 初始界面，get请求得到原始页面，post请求添加数据到数据库
@app.route('/myweb', methods=['GET', "POST", "PUT"])
def start_add():
    if request.method == 'GET':
        #初始页面
        if 'user_id' in session:
            # 用户已登录，渲染主页
            user_id = session['user_id']
            user = get_user_by_id(user_id)
            username = user['username']
            datalist = show(user_id)
            print(f"user_id:{user_id}的联系人{datalist}")
            return render_template('backmanage.html', datalist=datalist, user_id=user_id, username=username)
        else:
            # 未登录则重定向到登录页面
            print(f"未登录，重定向到登录页面")
            return redirect(url_for('sign'))

    #添加数据
    if request.method == 'POST':
        user_id = session['user_id']
        ContactName = request.args.get('ContactName')
        ContactPhone = request.args.get('ContactPhone')
        add_contact2db(user_id, ContactName, ContactPhone)
        datalist = show(user_id)
        print(f"添加数据后的联系人信息{datalist}")
        return jsonify(datalist)

    #修改数据
    if request.method == 'PUT':
        id = request.args.get('id')
        ContactName = request.args.get('ContactName')
        ContactPhone = request.args.get('ContactPhone')
        update_contact(id, ContactName, ContactPhone)
        return jsonify({'message': 'contact modify successfully'}), 200


# 删除数据，通过id删除数据库中的数据
@app.route('/myweb/<int:contact_id>', methods=['DELETE'])
def delete_user(contact_id):
    delete_contact(contact_id)
    print(f"删除id为{contact_id}的联系人信息")
    return jsonify({'message': 'User deleted successfully'}), 200


# 更新数据
@app.route('/myweb/<int:contact_id>', methods=['PUT'])
def update_user(contact_id):
    data = request.get_json()
    name = data.get('name')
    telNumber = data.get('telNumber')
    update_contact(contact_id, name, telNumber)
    return jsonify({'message': 'User updated successfully'}), 200




#-------------------------------------------------用户数据库操作--------------------------------------------------------
# 检查用户名或邮箱是否已注册，未被注册返回False
def check_user_signuped(username, email):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset="utf8", db="admin")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from users where username=%s or email=%s"
    cursor.execute(sql, [username, email])
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return False if len(result) == 0 else True



# 添加新用户到数据库
def add_user(username, email, password):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset="utf8", db="admin")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
    cursor.execute(sql, [username, email, password])
    conn.commit()
    cursor.close()
    conn.close()

# 根据用户名获取用户信息
def get_user_by_username(username):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset="utf8", db="admin")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE username=%s"
    cursor.execute(sql, [username])
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


# 根据id获得用户信息
def get_user_by_id(id):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset="utf8", db="admin")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE id=%s"
    cursor.execute(sql, [id])
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

#查询用户名与密码是否正确，正确返回True，否则返回False
def signin_check(username, password):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset="utf8", db="admin")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(sql, [username, password])
    result = cursor.fetchone()
    # 关闭连接
    cursor.close()
    conn.close()
    return False if result is None else True





#----------------------------------------------数据库联系人操作------------------------------------------------------



# 更新指定id联系人的数据
def update_contact(contact_id, contact_name, contact_phone):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset="utf8", db="admin")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "UPDATE contacts SET contact_name=%s, contact_phone=%s WHERE id=%s"
    cursor.execute(sql, (contact_name, contact_phone, contact_id))
    conn.commit()
    cursor.close()
    conn.close()


# 删除指定联系人id的数据
def delete_contact(contact_id):
    # 链接数据库
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset="utf8", db="admin")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 根据id删除数据
    sql = "delete from contacts where id=%s"
    cursor.execute(sql, [contact_id])
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()


# 查询指定用户的联系人信息
def show(user_id):
    # 链接数据库
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset="utf8", db="admin")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 插入数据
    sql = "select c.id, c.contact_name, c.contact_phone from users u join contacts c on u.id = c.user_id where u.id=%s"
    cursor.execute(sql, user_id)
    datalist = cursor.fetchall()
    # 关闭连接
    cursor.close()
    conn.close()
    return datalist


# 添加新联系人数据到数据库
def add_contact2db(user_id, contact_name, contact_phone):
    # 链接数据库
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', charset="utf8", db="admin")
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 插入数据
    sql = "INSERT INTO contacts (user_id, contact_name, contact_phone) VALUES (%s, %s, %s)"
    cursor.execute(sql, [user_id, contact_name, contact_phone])
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()


if __name__ == '__main__':
    app.run()
