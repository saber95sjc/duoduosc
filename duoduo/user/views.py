from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from . import models
import time
from django.db.models import Q
from django.core.paginator import Paginator
from django.core import serializers
import hashlib
def md5(user):
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


#登录
@csrf_exempt
def login(request, *args, **kwargs):
    if request.method == 'POST':
        ret = {'code': 1000, 'msg': None}
        tel = request.POST.get('tel')
        pwd = request.POST.get('pwd')
        obj = models.UserInfo.objects.filter(phone=tel, user_pwd=pwd).first()
        if not obj:
            ret['code'] = 1001
            ret['msg'] = '用户名密码错误'
            return JsonResponse(ret)
        # 创建token 存在就更新/不存在创建
        token = md5(str(tel))
        token_ = models.UserToken.objects.filter(user__id=obj.id).first()
        if not token_:
            user_token = models.UserToken()
            user_token.token = token
            user_token.user = obj
            user_token.save()
        else:
            token_.token = token
            token_.save()
        ret = {'code': 201, 'msg': 'success login', 'user': tel, 'token': token,'user_type':obj.type}
        return JsonResponse(ret)

#注册
@csrf_exempt
def register(request, *args, **kwargs):
    if request.method == 'POST':
        try:
            ret = {'code': 1000, 'msg': None}
            name = request.POST.get('username')
            tel = request.POST.get('tel')
            pwd = request.POST.get('pwd')
            qq = request.POST.get('qq')
            user_type = request.POST.get('id_code')
            obj = models.UserInfo.objects.filter(Q(phone=tel) | Q(user_name=name)).first()
            if obj:
                ret['code'] = 1001
                ret['msg'] = '用户名已存在'
            else:
                # 创建用户
                User = models.UserInfo()
                User.user_name = name
                User.phone = tel
                User.user_pwd = pwd
                User.qq = qq
                User.type = user_type
                User.save()
                ret = {'code': 201, 'msg': '注册成功,请登录', 'user': name}

            return JsonResponse(ret)
        except Exception as e:
            print(e)
            ret = {'code': 1000, 'msg': None}
            ret['code'] = 1002
            ret['msg'] = "注册异常"
            return  JsonResponse(ret)

#个人信息
@csrf_exempt
def detail(request, *args, **kwargs):
    if request.method == 'GET':
        # 登录之后才可以查看个人信息token认证
        token_ = request.GET.get('token')
        token = models.UserToken.objects.filter(token=token_).first()
        # 存在token且token没有过期
        if not token:
            ret = {'code': 1001, 'msg': '登录过期，请重新登录', 'token': 0}
            return JsonResponse(ret)
        else:
            # token没有过期
            str_time = str(token.create_time)[0:19]
            time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            # 转为时间戳比较
            token_create_time = int(time.mktime(time_array))
            now_time = int(time.time())
            time_difference = now_time - token_create_time
            if time_difference > 43200:
                ret = {'code': 1001, 'msg': '登录过期，请重新登录', 'token': 0}
                return JsonResponse(ret)
            name = token.user.user_name
            qq = token.user.qq
            tel = token.user.phone
            money = token.user.balance
            data = {'name': name, 'qq': qq, 'tel': tel, 'money': money}
            ret = {'code': 201, 'msg': 'success', 'data': data}
        return JsonResponse(ret)


# def vip_center(request, *args, **kwargs):
#     if request.method == 'GET':
#         ret = {'code': 1000, 'msg': None}
#         # 登录之后才可以查看会员中心
#         token_ = request.GET.get('token')
#         token = models.UserToken.objects.filter(token=token_).first()
#         # 存在token且token没有过期
#         str_time = str(token.create_time)[0:19]
#         time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
#         # 转为时间戳比较
#         token_create_time = int(time.mktime(time_array))
#         now_time = int(time.time())
#         time_difference = now_time - token_create_time
#         if not token or (time_difference > 43200):
#             ret = {'code': 1001, 'msg': 'token Authentication failure'}
#             return JsonResponse(ret)
#         else:
#             user_type = token.user.type
#             data = {'user_type': user_type}
#             ret = {'code': 201, 'msg': 'success', 'data': data}
#         return JsonResponse(ret)


@csrf_exempt
def certification(request, *args, **kwargs):
     #实名认证 后期再做
    if request.method == 'POST':
        ret = {'code': 1000, 'msg': None}
        user = request.POST.get('username')
        pwd = request.POST.get('pwd')
        print(user, pwd)
        obj = models.UserInfo.objects.filter(user_name=user, user_pwd=pwd).first()
        if not obj:
            ret['code'] = 1001
            ret['msg'] = '用户名密码错误'
        # 创建token
        token = md5(user)
        print(obj.id, obj.user_name)
        #
        token_ = models.UserToken.objects.filter(user__id=obj.id).first()
        if not token_:
            user_token = models.UserToken()
            user_token.token = token
            user_token.user = obj
            user_token.save()
        else:
            token_.token = token
            token_.save()

        return JsonResponse(ret)



@csrf_exempt
def invest_money(request, *args, **kwargs):
    if request.method == 'POST':
        ret = {'code': 1000, 'msg': None}
        # 登录之后才可以充值
        token_ = request.POST.get('token')
        money = request.POST.get('money')
        cash_order_number = request.POST.get('order_number')
        platform = request.POST.get('platform')
        token = models.UserToken.objects.filter(token=token_).first()
        # 存在token且token没有过期
        if not token:
            ret = {'code': 1001, 'msg': 'token 不存在', 'token': 0}
            return JsonResponse(ret)
        else:
            # token没有过期
            str_time = str(token.create_time)[0:19]
            time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            # 转为时间戳比较
            token_create_time = int(time.mktime(time_array))
            now_time = int(time.time())
            time_difference = now_time - token_create_time
            if time_difference > 43200:
                ret = {'code': 1001, 'msg': 'token 过期', 'token': 0}
                return JsonResponse(ret)
            # 此处需要调用第三方借口(支付宝)成功后充值
            # 每次充值都会产生一条记录
            # 此处为数据库事物
            try:
                save_id = transaction.savepoint()
                with transaction.atomic():
                    user_cash = models.UserCash()
                    user_cash.platform = platform
                    user_cash.money_move = money
                    user_cash.order_number = cash_order_number
                    user_cash.user = token.user
                    user_cash.remarks = '1'
                    user_cash.save()
                    # 更新用户余额
                    user_info = models.UserInfo.objects.filter(id=token.user.id).first()
                    balance = round(float(user_info.balance), 2) + round(float(money), 2)
                    user_info.balance = balance
                    user_info.save()
                transaction.savepoint_rollback(save_id)
            except Exception:
                ret = {'code': 1001, 'msg': 'data err', 'token': 0}
                return JsonResponse(ret)
            ret = {'code': 201, 'msg': 'success invest cash', 'balance': balance}
        return JsonResponse(ret)


@csrf_exempt
def withdraw_money(request, *args, **kwargs):
    if request.method == 'POST':
        ret = {'code': 1000, 'msg': None}
        # 登录之后才可以充值
        token_ = request.POST.get('token')
        money = request.POST.get('money')
        cash_order_number = request.POST.get('order_number')
        platform = request.POST.get('platform')
        token = models.UserToken.objects.filter(token=token_).first()
        # 存在token且token没有过期
        if not token:
            ret = {'code': 1001, 'msg': 'token 不存在', 'token': 0}
            return JsonResponse(ret)
        else:
            # token没有过期
            str_time = str(token.create_time)[0:19]
            time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            # 转为时间戳比较
            token_create_time = int(time.mktime(time_array))
            now_time = int(time.time())
            time_difference = now_time - token_create_time
            if time_difference > 43200:
                ret = {'code': 1001, 'msg': 'token 过期', 'token': 0}
                return JsonResponse(ret)
            # 此处需要调用第三方借口(支付宝)成功后充值
            # 每次充值都会产生一条记录
            # 此处为数据库事物
            try:
                save_id = transaction.savepoint()
                with transaction.atomic():
                    user_cash = models.UserCash()
                    user_cash.platform = platform
                    user_cash.money_move = money
                    user_cash.order_number = cash_order_number
                    user_cash.user = token.user
                    user_cash.remarks = '1'
                    user_cash.save()
                    # 更新用户余额
                    user_info = models.UserInfo.objects.filter(id=token.user.id).first()
                    balance = round(float(user_info.balance), 2) + round(float(money), 2)
                    user_info.balance = balance
                    user_info.save()
                transaction.savepoint_rollback(save_id)
            except Exception:
                ret = {'code': 1001, 'msg': 'data err', 'token': 0}
                return JsonResponse(ret)
            ret = {'code': 201, 'msg': 'success invest cash', 'balance': balance}
        return JsonResponse(ret)


@csrf_exempt
def release_order(request, *args, **kwargs):
    #创建订单
    if request.method == 'POST':
        # 登录之后商户才可以发布订单
        token_ = request.POST.get('token')
        token = models.UserToken.objects.filter(token=token_).first()
        # 存在token且token没有过期
        if not token:
            ret = {'code': 1001, 'msg': 'token 不存在', 'token': 0}
            return JsonResponse(ret)
        else:
            try:
            # token没有过期 是不是商户
                user_type = token.user.type
                str_time = str(token.create_time)[0:19]
                time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            # 转为时间戳比较
                token_create_time = int(time.mktime(time_array))
                now_time = int(time.time())
                time_difference = now_time - token_create_time
                if time_difference > 43200 or user_type != 1:
                    ret = {'code': 1001, 'msg': 'token err', 'token': 0}
                    return JsonResponse(ret)
                goods_id = request.POST.get('goods_id')
                goods_title = request.POST.get('goods_title')
                goods_main_img = request.POST.get('goods_main_img')
                goods_shops_logo = request.POST.get('goods_shops_logo')
                goods_one_price = request.POST.get('goods_one_price')
                group_buying_price = request.POST.get('group_buying_price')
                goods_sku = request.POST.get('goods_sku') #
                goods_fb_type = request.POST.get('goods_fb_type') #
                goods_fb_num = request.POST.get('goods_fb_num')
                goods_type_xd = request.POST.get('goods_type_xd')
                goods_sh_time = request.POST.get('goods_time')
                goods_task_type = request.POST.get('goods_task_type')
                goods_zd_address = request.POST.get('goods_zd_address')
                goods_it = request.POST.get('goods_it')
                goods_ir_zd = request.POST.get('goods_ir_zd')
                goods_sc = request.POST.get('goods_sc')
                goods_fg_sc = request.POST.get('goods_fg_sc')
                goods_hb = request.POST.get('goods_hb')
                goods_ly_body = request.POST.get('goods_ly_body')
                goods_ly_body_cash = request.POST.get('goods_ly_body_cash')
                commission = request.POST.get('goods_yj')
                goods_bz = request.POST.get('goods_bz')
                # 创建商品发布

                g_r = models.GoodsRelease()
                g_e = models.Dsrw()



                #指定sku
                if goods_sku == '1':
                    #指定sku
                    zdsku = request.POST.get('zdsku')
                    g_e.zhiding_data = zdsku

                if goods_fb_type == '0':
                    #定时发布
                    dsrw_rq = request.POST.get('dsrw_rq') #日期
                    dsfb = request.POST.get('dsfb') #数量 具体时间
                    g_e.dsrw_rq = dsrw_rq
                    g_e.time1 = dsfb

                if goods_task_type == '1':
                    #任务模式
                    rw_ms_ = request.POST.get('rw_ms_')
                    g_e.rw_mos = rw_ms_

                else:
                    rw_ms_ = request.POST.get('rw_ms_')
                    g_e.rw_mos = rw_ms_
                if goods_zd_address == '1':
                    #指定收获地址
                    shdz = request.POST.get('zddz')
                    g_e.zd_dz = shdz
                if goods_it == '3':
                    #聊天
                    zdny = request.POST.get('zdny')
                    g_e.zd1 = zdny

                if goods_ir_zd == '3':
                    # 指定评价内容
                    zdpj = request.POST.get('zdpj')
                    g_e.zdpy = zdpj

                elif goods_ir_zd == '4':
                    zdpj = request.POST.get('zdpj')
                    zdpjimg = request.POST.get('zdpjimg')
                    g_e.zdpy = zdpj
                    g_e.zdimg = zdpjimg








                g_r.goods_id = goods_id
                g_r.goods_title = goods_title
                g_r.goods_main_img = goods_main_img
                g_r.goods_shops_logo = goods_shops_logo
                g_r.goods_one_price = goods_one_price
                g_r.group_buying_price = group_buying_price
                g_r.goods_sku = goods_sku
                g_r.goods_fb_type = goods_fb_type
                g_r.goods_fb_num = goods_fb_num
                g_r.order_type = goods_type_xd
                g_r.goods_sh_time = goods_sh_time
                g_r.goods_task_type = goods_task_type
                g_r.goods_zd_address = goods_zd_address
                g_r.goods_it = goods_it
                g_r.goods_ir_zd = goods_ir_zd
                g_r.goods_sc = goods_sc
                g_r.goods_fg_sc = goods_fg_sc
                g_r.goods_hb = goods_hb
                g_r.goods_ly_body = goods_ly_body
                g_r.goods_ly_body_cash = goods_ly_body_cash
                g_r.commission = commission
                g_r.goods_bz_dd = goods_bz
                g_r.user = token.user

                g_e.user = g_r
                g_e.save()
                g_r.save()



                ret = {'code': 201, 'msg': '发布订单成功', 'token': 0}
                return JsonResponse(ret)
            except Exception as e:
                ret = {'code':205,'msg':"发布订单失败",'token':0}
                return JsonResponse(ret)


@csrf_exempt
def loot_order(request, *args, **kwargs):
    if request.method == 'POST':
        ret = {'code': 1000, 'msg': None}
        # 登录之后才可以充值
        token_ = request.POST.get('token')
        money = request.POST.get('money')
        cash_order_number = request.POST.get('order_number')
        platform = request.POST.get('platform')
        token = models.UserToken.objects.filter(token=token_).first()
        # 存在token且token没有过期
        if not token:
            ret = {'code': 1001, 'msg': 'token 不存在', 'token': 0}
            return JsonResponse(ret)
        else:
            # token没有过期
            str_time = str(token.create_time)[0:19]
            time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            # 转为时间戳比较
            token_create_time = int(time.mktime(time_array))
            now_time = int(time.time())
            time_difference = now_time - token_create_time
            if time_difference > 43200:
                ret = {'code': 1001, 'msg': 'token 过期', 'token': 0}
                return JsonResponse(ret)
            # 此处需要调用第三方借口(支付宝)成功后充值
            # 每次充值都会产生一条记录
            # 此处为数据库事物
            try:
                save_id = transaction.savepoint()
                with transaction.atomic():
                    user_cash = models.UserCash()
                    user_cash.platform = platform
                    user_cash.money_move = money
                    user_cash.order_number = cash_order_number
                    user_cash.user = token.user
                    user_cash.remarks = '1'
                    user_cash.save()
                    # 更新用户余额
                    user_info = models.UserInfo.objects.filter(id=token.user.id).first()
                    balance = round(float(user_info.balance), 2) + round(float(money), 2)
                    user_info.balance = balance
                    user_info.save()
                transaction.savepoint_rollback(save_id)
            except Exception:
                ret = {'code': 1001, 'msg': 'data err', 'token': 0}
                return JsonResponse(ret)
            ret = {'code': 201, 'msg': 'success invest cash', 'balance': balance}
        return JsonResponse(ret)



@csrf_exempt
def index(request, *args, **kwargs):
    #任务大厅
    if request.method == 'GET':
        page = request.GET.get('page')
        content = models.GoodsRelease.objects.all().filter(goods_fb_num__gt = 0)

        try:
            paginator = Paginator(content, 10)
            products = paginator.page(page)
            json_data = serializers.serialize("json", products, ensure_ascii=False)
            return HttpResponse(json_data, content_type='application/json; charset=utf-8')
        except Exception as e:
            ret = {'code':1001,"msg":"没有更多的页数"}
            return JsonResponse(ret)


#上传图片
@csrf_exempt
def path(request, *args, **kwargs):
    if request.method == 'POST':
        img = request.FILES.get('img',None)
        time_ = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
        name = md5(str(time))+str(time_)
        try:
            if not img:
                ret = {'code': 1001, 'msg': 'no files for upload!', 'token': 0}
                return JsonResponse(ret)
            else:
                name = './imglogo/{}.png'.format(name)
                with open(name, 'wb+') as f:
                    f.write(img.read())
                ret = {'code': 1000, 'msg': name, 'token': 0}
                return JsonResponse(ret)
        except Exception as e :
            ret = {'code': 1001, 'msg': '错误', 'token': 0}
            print('上传图片失败{}'.format(e))
            return JsonResponse(ret)


@csrf_exempt
def single(request,*args, **kwargs):
    #抢单
    if request.method == 'POST':
        token_ = request.POST.get('token')
        sp_id = request.POST.get('rw_id')
        token = models.UserToken.objects.filter(token=token_).first()
        if not token:
            ret = {'code': 1001, 'msg': 'token 不存在', 'token': 0}
            return JsonResponse(ret)
        user_type = token.user.type
        str_time = str(token.create_time)[0:19]
        time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        # 转为时间戳比较
        token_create_time = int(time.mktime(time_array))
        now_time = int(time.time())
        time_difference = now_time - token_create_time
        if time_difference > 43200 or user_type != 0:
            ret = {'code': 1001, 'msg': '抢单失败', 'token': 0}
            return JsonResponse(ret)
        else:
            sp_ = models.GoodsRelease.objects.filter(goods_id=sp_id).first()
            num = sp_.goods_fb_num
            if int(num) > 0:
                sp_.goods_fb_num = str(int(num) -1)
                sp_.save()
                ret = {'code':201,'msg':"下单成功"}
                return JsonResponse(ret)
            else:
                ret = {"code":1002,'msg':"下单异常,可能库存不足请联系管理员"}
                return JsonResponse(ret)

@csrf_exempt
def zfrw(request,*args,**kwargs):
    #支付任务
    if request.method == 'POST':
        token_ = request.POST.get('token')
        token = models.UserToken.objects.filter(token=token_).first()
        if not token:
            ret = {'code': 1001, 'msg': '登录过期请重新登录', 'token': 0}
            return JsonResponse(ret)
        user_type = token.user.type
        str_time = str(token.create_time)[0:19]
        time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        # 转为时间戳比较
        token_create_time = int(time.mktime(time_array))
        now_time = int(time.time())
        time_difference = now_time - token_create_time
        if time_difference > 43200 or user_type != 1:
            ret = {'code': 1002, 'msg': '验证失败', 'token': 0}
            return JsonResponse(ret)
        else:
            try:
                page = request.POST.get('page')
                sm = models.GoodsRelease.objects.filter(user=token.user)
                paginator = Paginator(sm, 10)
                products = paginator.page(page)
                json_data = serializers.serialize("json", products, ensure_ascii=False)
                return HttpResponse(json_data, content_type='application/json; charset=utf-8')
            except Exception as e:
                ret = {"code":1001,'msg':"没有更多内容"}
                return JsonResponse(ret)


def sy(request,*args,**kwargs):
    #首页
    if request.method == 'GET':
        return render(request,'index.html')


def test():
    pass
