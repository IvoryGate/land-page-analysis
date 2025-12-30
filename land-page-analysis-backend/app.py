import pymysql

# 数据库配置
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'xxxxxxxxxx',
    'database': 'landing_page_db',
    'charset': 'utf8mb4'
}

try:
    # 1. 尝试建立连接
    connection = pymysql.connect(**config)
    print("成功：MySQL 连接已建立！")

    with connection.cursor() as cursor:
        # 2. 检查数据库版本
        cursor.execute("SELECT VERSION();")
        version = cursor.fetchone()
        print(f"数据库版本: {version[0]}")

        # 3. 检查字符集（确保是 utf8mb4）
        cursor.execute("SHOW VARIABLES LIKE 'character_set_database';")
        charset = cursor.fetchone()
        print(f"当前数据库字符集: {charset[1]}")

    connection.close()
    print("测试完成，连接已安全关闭。")

except Exception as e:
    print(f"失败：无法连接到 MySQL。错误信息：\n{e}")