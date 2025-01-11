# 導入redis模組
import redis

# 建立本地連線
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# 資料庫操作


# 設置一個鍵 "name"，其值為 "John Doe"
r.set("name", "John Doe")

# 使用 lpush 方法將數字 1, 2, 3, 4, 5 推入 "mylist" 列表的左邊（相當於將這些數字加到列表的前端）
r.lpush("mylist", 1, 2, 3, 4, 5)

# 使用 lrange 方法查看 "mylist" 列表的內容，0 到 -1 表示查看整個列表
print(r.lrange("mylist", 0, -1))  # 預期輸出：['5', '4', '3', '2', '1']

# 使用 sadd 方法將數字 1, 2, 3, 4, 5 添加到 "myset" 集合中
r.sadd("myset", 1, 2, 3, 4, 5)

# 使用 smembers 方法查看 "myset" 集合中的所有元素，集合中的元素是無序的
print(r.smembers("myset"))  # 預期輸出：{1, 2, 3, 4, 5}
