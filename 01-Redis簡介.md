# Redis 筆記

## 連線到資料庫方式
cmd命令行: redis-cli

## 主要特點
1. 基於內存的，高效能的鍵值資料庫(Key-Value)
2. 非關係型資料庫(noSql)
3. 不能用sql語句

## 支援的數據結構
1. 字符串(String)：可以存儲任何二進制數據（如 JPG、PNG 圖像）。
2. (列表)List：有序的字符串集合，支持從兩端推入和彈出元素。
3. (集合)Set：無序的字符串集合，支持交集、並集等集合運算。
4. (有序集合)Sorted Set：類似於 Set，但每個元素都會有一個分數（score），可以根據分數進行排序。
5. (哈希表)Hash：可以存儲多個鍵值對的數據結構，常用於存儲對象或複雜數據。

## 其他命令
1. select 0~15: 切換資料庫(默認0)

## 鍵(KEY)命令:
1. KEYS *: 查看所有鍵
2. KEYS n*: 查看以n開頭的....以此類推
3. EXISTS key: 判斷該鍵是否存在
4. TYPE key: 查看該鍵的數據類型
5. DEL key1 key2...: 刪除指定的鍵，可以一次多個
6. EXPIRE key seconds: 設置鍵的過期時間。
7. ttl key: 可查看該鍵離過期剩餘的秒數


## String 基本命令
1. SET key value：設置指定鍵的值。
2. GET key：獲取指定鍵的值。
3. SETEX key 秒數 value:設置帶有過期時間的鍵
4. ttl key: 可查看該鍵離過期剩餘的秒數
5. MSET key value ...: 設置多個鍵值對
6. MGET key value ...: 同時獲取多個鍵值
7. INCR key: 將指定的鍵值+1
8. DECR key: 將指定的鍵值-1 

## Hash 基本命令:
# key可理解成類名，field為屬性名，value則是具體值
1. HSET key field1 value1 ...: 設置哈希表中指定欄位的值(可多個)。如果該欄位已經存在，則會覆蓋其原有的值
2. HGET key field : 獲取哈希表中指定欄位的值。
4. HDEl key field: 刪除哈希表中指定的欄位
5. HMGET key field: 一次性獲取多個欄位的值。
6. HKEYS key: 獲取哈希表中所有的欄位名（`field`）
7. HVALS key: 獲取哈希表中所有欄位的值（`value`）

## List 基本命令:
1. LPUSH key value1 value2 ... : 從列表左側插入元素
2. RPUSH key value1 value2 ... : 從列表右側插入元素
3. LRANGE key start end: 獲取從下標 start 到 end 的所有元素(0 -1 即可取到全部)
4. LREM  key count value: 移除指定元素，count 代表匹配到要刪的數量
    - count = 0：移除所有匹配的元素。
    - count > 0：從左側開始移除最多 count 個匹配的元素。
    - count < 0：從右側開始移除最多 count 個匹配的元素。

## Set 基本命令:
# 特性: 1.無序 2.元素都為string類型 3.不能重複 4.集合為不可變類型，增刪操作實際是新集合覆蓋舊的
1. SADD key value1 value2 ...：向集合添加元素。
2. SREM key value：移除集合中的元素。
3. SMEMBERS key：返回集合中所有元素。
4. SSCARD key : 返回集合中的元素數量。
4. SISMEMBER key value：檢查元素是否存在於集合中。
5. SRANDMEMBER key count: 隨機返回集合中 count 個元素
5. SSCAN key cursor [MATCH pattern] [COUNT count]: 分批遍歷集合中的元素，可以使用 MATCH 過濾符合條件的元素，COUNT 設定每次掃描的元素數量。
    - cursor：用於遍歷過程中的位置標記。初次為 0，之後根據返回的游標繼續遍歷。
    - MATCH pattern: 過濾條件，根據模式匹配元素。
    - COUNT count: 返回的元素數量限制，雖然不保證精確數量，但用於調整遍歷的效率

## Zset 基本命令:
# 特性:1. 有序且按分數排序 2.元素是唯一，但分數可以重複 3. 每個元素由 member + score 組成。
1. ZADD key score member1 score member2 ...：向有序集合添加元素，並為每個元素指定分數。如果元素已存在，則更新其分數。
2. ZREM key member1 member2 ...：移除有序集合中的指定元素。
3. ZRANGE key start stop [WITHSCORES]：返回下標 start 到 stop 區間的元素(分數低到高排序)，WITHSCORES 可選，表示是否一同返回分數。
4. ZREVRANGE key start stop [WITHSCORES]: 同上，但返回的順序是score從高到低
5. ZCARD key：返回有序集合中的元素數量。
6. ZSCORE key member：獲取指定元素的分數。
7. ZSCAN key cursor [MATCH pattern] [COUNT count]: 同set的用法



## 在 python 建立 Redis 連線
```python
import redis # 或 from redis import Redis)
r = redis.Redis(host="localhost", port=6379, db=0,  decode_responses=True)  # 或用Redis()

# 設置與獲取鍵值
r.set("name", "Alice")
print(r.get("name"))  # 輸出: Alice
```
## 基本鍵值操作
1. r.set(key, value) - 設置鍵值對
2. r.get(key) - 獲取鍵值
3. r.delete(key) - 刪除鍵

---

## 列表操作
1. r.lpush(key, value) - 在列表左側插入元素
2. r.rpush(key, value) - 在列表右側插入元素
3. r.lpop(key) - 從左側彈出元素
4. r.rpop(key) - 從右側彈出元素
5. r.lrange(key, start, stop) - 獲取列表指定範圍內的元素

---

## 集合操作
1. r.sadd(key, value) - 添加元素到集合
2. r.srem(key, value) - 刪除集合中的元素
3. r.smembers(key) - 獲取集合中的所有元素

---

## 哈希表操作
1. r.hset(key, field, value) - 設置哈希表中的鍵值對
2. r.hget(key, field) - 獲取哈希表中指定欄位的值
3. r.hdel(key, field) - 刪除哈希表中的指定欄位
4. r.hgetall(key) - 獲取整個哈希表

---

## 發佈與訂閱 (Pub/Sub)
1. r.publish(channel, message) - 發佈消息到頻道
2. r.pubsub() - 創建一個訂閱對象
3. r.subscribe(channel) - 訂閱頻道
4. r.unsubscribe(channel) - 取消訂閱頻道

---

