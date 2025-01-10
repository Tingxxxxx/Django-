# Redis 筆記

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

## Strinn 基本命令
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







