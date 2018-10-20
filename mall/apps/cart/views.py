import base64
import pickle
from django_redis import get_redis_connection

from goods.models import SKU
from .serializers import CartSerializer
from rest_framework.views import APIView
from rest_framework.views import Response
# Create your views here.

# 购物车
class CartView(APIView):
    """
    购物车
    POST  /cart/  添加商品到购物车
    """

    # 因为我们的请求中可能携带了 Authorization
    # 视图会首先调用 perform_authentication 进行身份认证 401
    def perform_authentication(self, request):
        """
        重写父类的用户验证方法,不在进入视图就检查JWT
        """

        pass

    # 添加到购物车
    def post(self, request):
        """
        思路:
            获取数据进行验证
            获取商品id, count 和是否选中信息
                选中状态 默认为True, 同时 前端 是否选中的字段 可传可不穿
            判断用户是否为登录用户
                如果为登录用户,则将数据保存到redis中
                    连接数据库redis
                    将商品放到redis中, 同时记录状态(把选中的记录一下)
                    返回响应
                如果为非登录用户,则保存到cookie中
                    先读取cookie的数据, 判断有没有数据
                    如果有数据, 我们需要将数据 解析出来
                    跟新数据
                        如果没有  直接保存数据
                        如果有     需要把count 进行累加
                    把数据加密
        """

        # 获取数据,进行校验
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 获取商品id, count 和 是否选中
        sku_id = serializer.data.get('sku_id')
        count = serializer.data.get('count')
        selected = serializer.data.get('selected')

        # 判断用户是否登陆
        try:
            user = request.user
        except Exception:
            # 验证失败,用户为登陆
            user = None
        # 判断是否为登录用户
        if user is not None and user.is_authenticated:
            # 如果为登陆状态,则将数据保存至redis中
            redis_count = get_redis_connection('cart')
            pl = redis_count.pipeline()
            # 勾选
            if selected:
                pl.sadd('cart_selected_%s' % user.id, sku_id)
            pl.execute(serializer.data)
        else:
            # 如果为非登陆用户,保存至cookie中
            cart_str = request.COOKIES.get('cart')
            # 先获取cookie信息, 判断是否存在购物车信息
            if cart_str is None:
                cart_dict = pickle.loads(base64.b64decode(cart_str .encode))
            else:
                cart_dict = {}
            # 获取购物车数量
            # 如果有相同的商品,求和
            if sku_id in cart_dict:
                origin_count = cart_dict[sku_id]['count']
                count += origin_count

            cart_dict[sku_id]:{
                'count': count,
                'selected': selected,
            }

            # 设置 cookie数据
            response = Response(serializer.data)
            # 将二进制转换为字符串
            cookie_cart = base64.b64encode(pickle.dumps(cart_dict).decode())
            response.set_cookie('cart', cookie_cart)
            # 返回响应
            return response

    # 查询购物车数据
    def get(self, request):
        """
        request.user
        判断用户登录状态
        登录用户的数据保存在Redis中
            链接redis
            获取所有的商品id和数量,以及是否选中
        未登录的数据存储在cookie中
            获取cookie中的数据,并判断
        根据id获取商品信息
        我们需要将sku的对象添加 count 和 select
        将模型列表转换为JSON
        返回响应
        :param request:
        :return:
        """
        try:
            user = request.user
        except Exception as e:
            user = None

        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('cart')
            redis_ids = redis_conn.hgetall('cart_%s'% user.id)
            redis_selected_ids = redis_conn.smembers('cart_selected_%s'% user.id)

            cart = {}

            for sku_id in redis_ids.keys():
                cart[sku_id] = {
                    'count': redis_ids[sku_id],
                    'selected': sku_id in redis_selected_ids,
                }
        else:
            cookie_str = request.COOKIES.get('cart')
            if cookie_str is not None:
                b64decode = base64.b16decode(cookie_str)
                cart = pickle.loads(b64decode)
            else:
                cart = {}
        ids = cart.keys()
        skus = SKU.objects.get()

    # 修改购物车数据
    def put(self, request):
        """
        接受前端提交上的数据
        校验
        获取数据
        request.user
        判断用户的登陆状态
        登录用户的数据 保存在redis中
            连接
            修改数据
            返回数据
        未登录的数据 保存在cookie中
            获取数据并判断
            更新
            设置cookie返回响应
        """

        """
        修改购物车数据
        思路:
        # 创建序列化,校验数据
        #获取数据
        #获取用户
        #判断用户是否为登录用户
             #登录用户,从redis中获取数据
            #非登录用户,从cookie中获取数据
        """
        # 创建序列化,校验数据
        serializer = CartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sku_id = serializer.data.get('sku_id')
        count = serializer.data.get('count')
        selected = serializer.data.get('selected')
        # 获取用户
        try:
            user = request.user
        except Exception:
            user = None
        # 判断用户是否为登录用户
        if user is not None and user.is_authenticated:
            # 登录用户,从redis中获取数据
            redis_conn = get_redis_connection('cart')
            pl = redis_conn.pipeline()

            # 更新数据
            pl.hset('cart_%s' % user.id, sku_id, count)
            # 更改状态
            if selected:
                pl.sadd('cart_selected_%s' % user.id, sku_id)
            else:
                pl.srem('cart_selected_%s' % user.id, sku_id)
            pl.execute()
            return Response(serializer.data)
        else:
            # 非登录用户,从cookie中获取数据
            cart_str = request.COOKIES.get('cart')
            if cart_cookie is not None:
                cart = pickle.loads(base64.b64decode(cart_str.encode()))
            else:
                cart = {}

            if sku_id in cart:
                cart[sku_id] = {
                    'count': count,
                    'selected': selected
                }

            cookie_str = base64.b64encode(pickle.dumps(cart)).decode()

            response = Response(serializer.data)
            response.set_cookie('cart', cookie_str)

            return response


    # 删除购物车数据
    def delete(self, request):
        """
        前端提交 sku_id
        验证数据
        获取数据
        request.user
        判断用户登陆状态
        未登录的数据
        登陆的数据
        :param request:
        :return:
        """
