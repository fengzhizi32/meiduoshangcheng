# 导入库
from fdfs_client.client import Fdfs_client
# 创建客户端,需要加载配置文件,配置文件的tracker必须设置正确
client = Fdfs_client('配置文件路径')

# 上传照片
client.upload_by_filename('路径')

# 返回结果
# getting connection
# <fdfs_client.connection.Connection object at 0x7f69cc63c828>
# <fdfs_client.fdfs_protol.Tracker_header object at 0x7f69cc63c7f0>
# {
# 'Group name': 'group1',
# 'Remote file_id': 'group1/M00/00/00/wKiOllvGHF6AS5ckAADIlkvVtHw058.jpg',
# 'Status': 'Upload successed.',
# 'Local file name': '/home/python/Desktop/images/timg.jpg',
# 'Uploaded size': '50.00KB',
# 'Storage IP': '192.168.142.150'
# }
