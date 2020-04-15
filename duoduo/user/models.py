from django.db import models


class UserInfo(models.Model):
    u_type = (
        ('1', '普通用户'),
        ('2', 'vip'),
        ('3', 'svip'),
    )
    vip_type = models.IntegerField(choices=u_type, null=True, default=1)
    user_name = models.CharField(max_length=32, unique=True) #用户名
    user_pwd = models.CharField(max_length=64, null=True) #密码
    phone = models.CharField(max_length=22, null=True) #电话号码
    qq = models.CharField(max_length=22, null=True) #qq
    active = models.IntegerField(null=True, default=0)  # 0代表未激活/1为激活
    type = models.IntegerField(null=True)  # 0/1/2 用户/商户/管理员
    balance = models.FloatField(null=True, default=0) #金额

    id_card_number = models.CharField(max_length=18, null=True) #身份证号码
    id_card_name = models.CharField(max_length=18, null=True) #身份证姓名
    id_card_img_front = models.CharField(max_length=255, null=True) #身份证正面
    id_card_img_back = models.CharField(max_length=255, null=True) #身份证反面
    sc_card_img = models.CharField(max_length=255,null=True) #手持身份证
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    last_modify = models.DateTimeField(auto_now=True, null=True)


class UserToken(models.Model):
    token = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True, null=True)  # 用于过期判断


class UserCash(models.Model):
    p_type = (
        ('1', '支付宝'),
        ('2', '其他'),
    )
    # id = models.IntegerField(primary_key=True)
    platform = models.IntegerField(choices=p_type, null=True, default=1) #充值平台
    zfb_id = models.CharField(max_length=100, null=True) #支付id
    zfb_img = models.CharField(max_length=255, null=True) #收款码
    order_number = models.CharField(max_length=200, null=True) #充值流水号
    option_time = models.DateTimeField(auto_now=True, null=True)  # 充值时间
    money_move = models.CharField(max_length=200, null=True)  # 金额
    remarks = models.CharField(max_length=200, null=True)  # 备注动向1为充值2提现3异常
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    last_modify_at = models.DateTimeField(auto_now=True)


class GoodsRelease(models.Model):
    status_dd = (
        ('1','正常'),
        ('2','异常')
    )
    dd_status = models.IntegerField(choices=status_dd, null=True, default=1)
    goods_id = models.CharField(max_length=255, null=True)  # 商品id
    goods_title = models.CharField(max_length=255, null=True)  # 商品标题
    goods_main_img = models.CharField(max_length=255, null=True)  # 商品主图
    goods_shops_logo = models.CharField(max_length=255, null=True)  # 店铺logo
    goods_one_price = models.CharField(max_length=255, null=True)  # 单购价格
    group_buying_price = models.CharField(max_length=255, null=True)  # 团购价格

    goods_sku = models.CharField(max_length=10, null=True)  # 指定sku   指定1 不指定0

    goods_fb_type = models.CharField(max_length=10, null=True)  # 发布类型 立即发布1 定时任务0
    goods_fb_num = models.CharField(max_length=255, null=True)  # 发布数量

    order_type = models.CharField(max_length=10, null=True)  # 下单类型 0有团参团 1单买 2开团  3必须开团

    goods_sh_time = models.CharField(max_length=255, null=True)  # 收获时间 0随物流收获 1立刻收获

    goods_task_type = models.CharField(max_length=255, null=True)  # 任务模式 二维码1 搜索2

    goods_zd_address = models.CharField(max_length=255, null=True)  # 指定收货地址  指定1  不指定0

    goods_it = models.CharField(max_length=255, null=True)  # 聊天 1.无需假聊 2.内容自己发挥 3.指定聊天内容
    goods_ir_zd = models.CharField(max_length=255, null=True)  # 指定评价内容 1无字好评 2自由发挥 3指定评语 4指定评语与图片
    goods_sc = models.CharField(max_length=255, null=True)  # 收藏  店铺收藏1 商品收藏 店铺+商品收藏1，2 以逗号分隔
    goods_fg_sc = models.CharField(max_length=255, null=True)  # 复购时长 1，1天 2，15天 3，30天
    goods_hb = models.CharField(max_length=255, null=True)  # 是否货比  不货比0 货比1家1 货比2家2 货比3家4
    goods_ly_body = models.CharField(max_length=255, null=True)  # 浏览副宝贝 不浏览0  浏览1 1 浏览2 2 浏览3 3
    goods_ly_body_cash = models.CharField(max_length=50, null=True)  # 浏览副宝贝金额
    goods_bz_dd = models.CharField(max_length=255, null=True)  # 备注
    commission = models.FloatField(null=True)  # 订单佣金
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    last_modify_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    #刷手抢单表
    shang_hu_id = models.IntegerField(null=True)  #抢单的商户
    shua_shou_id = models.IntegerField(null=True) #抢单的刷手
    status = models.IntegerField(null=True)  #任务 提交状态 0/1 正常/停止
    goods_release = models.OneToOneField(to='GoodsRelease', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    last_modify_at = models.DateTimeField(auto_now=True)

class Order_detail(models.Model):
    #刷手任务流程
    user = models.OneToOneField(to='Order', on_delete=models.CASCADE)
    ddh = models.CharField(max_length=100,null=True) #下单订单号
    shr = models.CharField(max_length=20,null=True) #收货人
    shr_jt = models.CharField(max_length=100, null=True)  # 收货截图
    huobi = models.CharField(max_length=100,null=True) #货比截图
    pjjt = models.CharField(max_length=100,null=True) #评价截图
    jljt = models.CharField(max_length=100, null=True) #假聊截图
    fbbjt = models.CharField(max_length=100, null=True) #副宝贝截图




class Dsrw(models.Model):
    #发布类型 定时任务时间表
    user = models.OneToOneField(to='GoodsRelease', on_delete=models.CASCADE)
    zhiding_data = models.CharField(max_length=250, null=True)  # 选择指定 内容以,分隔

    rw_mos = models.CharField(max_length=255,null=True) #关键词以,分割 图片就是图片地址

    zd_dz = models.CharField(max_length=255,null=True) #以逗号分隔 收件姓名,手机号码,详细地址

    zd1 = models.CharField(max_length=500,null=True) #指定聊天语句 以逗号分隔

    dsrw_rq = models.CharField(max_length=500,null=True) #定时任务日期
    time1 = models.CharField(max_length=500,null=True) #定时任务 前面为时间 后面为数量 例1_10 代码 晚上一点10个任务 多个任务以,分隔

    zdpy = models.CharField(max_length=500,null=True)#指定评语
    zdimg = models.CharField(max_length=500,null=True) #指定评语图片地址


