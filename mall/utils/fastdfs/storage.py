# 运营:确保网站的运营,如数据的变动
# 运维:确保网站的维护

from django.core.files.storage import Storage
from django.conf import settings
from django.utils.deconstruct import deconstructible
from fdfs_client.client import Fdfs_client
from mall import settings


# 1.您的自定义存储系统必须是以下子类:django.core.files.storage.Storage：
# 2.Django必须能够在没有任何参数的情况下实例化您的存储系统。这意味着任何设置都应该来自django.conf.settings：
# 3.您的存储类必须实现_open()和_save() 方法以及适用于您的存储类的任何其他方法。有关这些方法的更多信息，请参见下此外，如果您的类提供本地文件存储，则它必须覆盖该path()方法。
# 4.您的存储类必须是可解构的， 以便在迁移中的字段上使用时可以对其进行序列化。只要您的字段具有可自行序列化的参数，就 可以使用 django.utils.deconstruct.deconstructible类装饰器（这就是Django在FileSystemStorage上使用的）。

@deconstructible
class MyStorage(Storage):
    # 2.Django必须能够在没有任何参数的情况下实例化您的存储系统。
    # 这意味着任何设置都应该来自django.conf.settings：

    def __init__(self, path=None, ip=None):
        if not path:
            path = settings.FDFS_CLIENT_CONF
            self.path = path
        if not ip:
            ip = settings.FDFS_URL
            self.ip = ip

    # 打开我们的资源,我们采用 fastdfs 实现文件的上传和下载,所以不需要实现里边的逻辑
    def _open(self, name, mode='rb'):

        pass

    # save 保存
    # 使用FastDFS 默认会保存到文件中,我们需要实现里边的业务逻辑来保存到fdfs
    def _save(self, name, content, max_length=None):

        # 1.创建 fdfs_client 客户端,加载 FDFS的配置信息
        # client = Fdfs_client('utils/fastdfs/client.conf')
        # client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        client = Fdfs_client(self.path)

        # 2.获取图片内容并上传
        # 注意点:content是图片二进制内容
        file_data = content.read()
        # buffer 上传二进制
        result = client.upload_appender_by_buffer((file_data))
        """
        {'Group name': 'group1',
        'Remote file_id': 'group1/M00/00/00/wKiOllvGHF6AS5ckAADIlkvVtHw058.jpg',
        'Status': 'Upload successed.',
        'Local file name': '/home/python/Desktop/images/timg.jpg',
        'Uploaded size': '50.00KB',
        'Storage IP': '192.168.142.150'}

        """
        # 3.判断返回结果 返回 图片路径
        if result.get('Status') == 'Upload successed.':
            # 返回上传的字符串
            return result.get('Remote file_id')
        else:
            raise Exception('上传失败')

    # 判断是否存在
    # 上传图片不会出现覆盖的情况,直接返回False
    # 不需要判断
    def exists(self, name):
        # 判断文件是否存在，FastDFS可以自行解决文件的重名问题
        # 所以此处返回False，告诉Django上传的都是新文件
        return False

    def url(self, name):
        # 返回文件的完整URL路径
        # 默认只会把name返回回去,
        # return 'http://192.168.140.150:8888' + name
        # return settings.FDFS_URL + name
        return self.ip + name