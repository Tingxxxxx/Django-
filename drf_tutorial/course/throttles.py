from rest_framework.throttling import SimpleRateThrottle
# 自訂義限流類
class Mythrottle(SimpleRateThrottle):
    # cache_format = 'throttle_%(scope)s_%(ident)s' 父類中已經定義好的變量
    scope = 'vip' # 此限流策略的名字
    # rate = '5/min'  # 優先使用類中的rate,如無則讀取settings.py的

    def get_cache_key(self, request, view): 
        """
        取得使用者的 cache key
        1. 如果 request.user 存在，使用 request.user.id 作為 cache key
        2. 如果 request.user 不存在，使用 get_ident() 來取得一個不重複的 ID
        返回值:
        生成一個唯一字符串，會被用作快取中的鍵，用於追蹤用戶的請求次數。
        """
        if request.user and request.user.is_authenticated:
            ident = request.user.id
        else:
            ident = self.get_ident()  # 使用 get_ident() 取得用戶識別ID

        cache_key = self.cache_format % {'scope': self.scope, 'ident': ident}
        
        # 測試用
        print(f"Generated Cache Key: {cache_key}")
        return cache_key