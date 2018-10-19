import base64
import pickle
from django_redis import get_redis_connection
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

    def post(self, request):
        """
        思路:
            获取数据进行验证
            获取商品id, count 和是否选中信息
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
        serializer = CartSerializer(data = request.data)
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
            cookie_cart = base64.b64encode(pickle.dumps(cart_dict).decode())
            response.set_cookie('cart', cookie_cart)
            # 返回响应
            return response