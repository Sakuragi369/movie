# -*- coding: utf-8 -*-
import logging
import json

from rest_framework.response import Response
from django.conf import settings
from utils.api_util import CodeMsg
from django.contrib.auth import authenticate, login

logger = logging.getLogger(__name__)


def api_serializer_deco(api_msg):
    """
    统一处理接口序列化及返回数据
    :param api_msg:
    :return:
    """

    def _wrapper(func):
        def deco(*args, **kwargs):
            try:
                obj = args[0]
                req = args[1]
                cloud_id = kwargs.get('pk')

                # logger.info('request session: %s' % req.session)
                # logger.info('request session key: %s' % req.session.session_key)
                # logger.info('request COOKIES session: %s' % req.COOKIES.get(settings.SESSION_COOKIE_NAME, ""))
                # logger.info('request CDS_TOKEN_NAME: %s' % req.COOKIES.get(settings.CDS_TOKEN_NAME, ""))
                #
                # token = req.META.get('HTTP_ACCESS_TOKEN')
                # if not token:
                #     token = req.COOKIES.get(settings.CDS_TOKEN_NAME)
                #
                # if req.user.is_authenticated() and req.user.token == token:
                #     logger.info('request user session: %s' % req.user.session_key)
                #     user_id = req.user.id
                #     req = set_req_per(req, user_id)
                # else:
                #     if req.user.is_authenticated():
                #         Token.objects.del_token(req.user.id)
                #
                #     if token:
                #         usr = authenticate(token=token)
                #         logger.info("customer_login_required.token:" + token)
                #
                #         if usr:
                #             login(req, usr)
                #             user_id = req.user.id
                #             logger.info("django login user id <<<<%s>>> is ok" % user_id)
                #             session_key = req.session.session_key
                #             Token.objects.add_token(usr.pk, "console-end", token, session_key)
                #             req.user = usr
                #             req.session["update_cds_token"] = True
                #             set_req_per(req, user_id)
                #         else:
                #             logger.info("Invalid token:" + token)
                #             login_url = settings.LOGIN_URL + "?next="
                #             res = Response({"status": 401, "msg": "not login", "data": {"sso_url": login_url}})
                #             res.status_code = 401
                #             return res
                #     else:
                #         login_url = settings.LOGIN_URL + "?next="
                #         res = Response({"status": 401, "msg": "not login", "data": {"sso_url": login_url}})
                #         res.status_code = 401
                #         return res

                req_dict = {
                    "GET": req.GET.dict(),
                    "POST": req.data,
                    "PUT": req.data
                }

                if cloud_id:
                    req_dict[req.method].update({'id': cloud_id}) if isinstance(req_dict[req.method], dict) else \
                        req_dict[req.method].update(id=cloud_id)

                obj_serializer = None
                if obj.serializer_class:
                    obj_serializer = obj.get_serializer(data=req_dict.get(req.method))
                if not obj_serializer or obj_serializer.is_valid():
                    if obj_serializer:
                        serializer_data = obj_serializer.data
                        kwargs['serializer_data'] = serializer_data
                    order_res = func(*args, **kwargs)
                    if order_res.response:
                        return order_res.response
                    status = 1
                    code = 200
                    if not order_res.is_success():
                        status = 0
                        code = order_res.code
                    res = {
                        'code': code,
                        'msg': order_res.message,
                        'data': order_res.data,
                        'status': status
                    }
                else:
                    res = {
                        'code': CodeMsg.PARAM_ERROR['code'],
                        'msg': obj_serializer.errors,
                        'status': 0
                    }
            except Exception as ex:
                msg = u'%s异常：%s' % (api_msg, ex)
                logger.error(msg, exc_info=True)
                res = {
                    'code': CodeMsg.UNKNOWN_ERROR['code'],
                    'status': 0,
                    'msg': msg
                }
            logger.info(u'%s返回结果:%s' % (api_msg, json.dumps(res)))
            res = json.loads(json.dumps(res))
            return Response(res)

        return deco

    return _wrapper
