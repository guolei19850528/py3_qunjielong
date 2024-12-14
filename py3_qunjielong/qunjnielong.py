#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/py3_qunjielong
=================================================
"""
from datetime import timedelta
from typing import Union

import diskcache
import py3_requests
import redis
import requests
from addict import Dict
from jsonschema.validators import Draft202012Validator
from requests import Response


class RequestUrl(py3_requests.RequestUrl):
    BASE = "https://openapi.qunjielong.com/"
    OPEN_API_GHOME_GETGHOMEINFO = "/open/api/ghome/getGhomeInfo"
    OPEN_AUTH_TOKEN = "/open/auth/token"
    OPEN_API_ACT_LIST_ACT_INFO = "/open/api/act/list_act_info"
    OPEN_API_ACT_GOODS_QUERY_ACT_GOODS = "/open/api/act_goods/query_act_goods"
    OPEN_API_GOODS_GET_GOODS_DETAIL = "/open/api/goods/get_goods_detail"
    OPEN_API_ORDER_FORWARD_QUERY_ORDER_LIST = "/open/api/order/forward/query_order_list"
    OPEN_API_ORDER_REVERSE_QUERY_ORDER_LIST = "/open/api/order/reverse/query_order_list"
    OPEN_API_ORDER_ALL_QUERY_ORDER_LIST = "/open/api/order/all/query_order_list"
    OPEN_API_ORDER_SINGLE_QUERY_ORDER_INFO = "/open/api/order/single/query_order_info"


class ValidatorJsonSchemas(py3_requests.ValidatorJsonSchema):
    SUCCESS = Dict({
        "type": "object",
        "properties": {
            "code": {
                "oneOf": [
                    {"type": "integer", "const": 200},
                    {"type": "string", "const": 200},
                ],
            }
        },
        "required": ["code"],
    })

    GETGHOMEINFO = Dict({
        "type": "object",
        "properties": {
            "ghId": {"type": "integer", "minimum": 1},
        },
        "required": ["ghId"]
    })


class ResponseHandler(py3_requests.ResponseHandler):
    @staticmethod
    def success(response: Response = None):
        json_addict = ResponseHandler.status_code_200_json_addict(response=response)
        if Draft202012Validator(ValidatorJsonSchemas.SUCCESS).is_valid(instance=json_addict):
            return json_addict.get("data", None)
        return None


class Qunjielong(object):
    """
    Qunjielong Class

    @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/
    """

    def __init__(
            self,
            base_url: str = RequestUrl.BASE,
            secret: str = "",
            cache: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None,
    ):
        """
        Qunjielong Class

        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/
        :param base_url:
        :param secret:
        :param cache:
        """
        self.base_url = base_url[:-1] if base_url.endswith("/") else base_url
        self.secret = secret
        self.cache = cache
        self.access_token = ""

    def request_with_token(self, **kwargs):
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.success)
        kwargs.setdefault("method", py3_requests.RequestMethod.GET)
        kwargs.setdefault("url", "")
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("params", Dict())
        kwargs.params.setdefault("accessToken", self.access_token)
        return py3_requests.request(**kwargs.to_dict())

    def getGhomeInfo(
            self,
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=09b80879-ddcb-49bf-b1e9-33181913924d
        :param method:
        :param url:
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", py3_requests.RequestMethod.GET)
        kwargs.setdefault("url", RequestUrl.OPEN_API_GHOME_GETGHOMEINFO)
        return self.request_with_token(**kwargs.to_dict())

    def token_with_cache(
            self,
            expire: Union[float, int, timedelta] = None,
            token_kwargs: dict = {},
            getGhomeInfo_kwargs: dict = {}
    ):
        """
        access token with cache
        :param expire: expire time default 7100 seconds
        :param token_kwargs: self.token kwargs
        :param get_ghome_info_kwargs: self.get_ghome_info kwargs
        :return:
        """
        cache_key = f"py3_qunjielong_access_token_{self.secret}"
        if isinstance(self.cache, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            self.access_token = self.cache.get(cache_key)

        if not Draft202012Validator(ValidatorJsonSchemas.GETGHOMEINFO).is_valid(
                self.getGhomeInfo(**Dict(getGhomeInfo_kwargs).to_dict())
        ):
            self.token(**token_kwargs)
            if isinstance(self.access_token, str) and len(self.access_token):
                if isinstance(self.cache, diskcache.Cache):
                    self.cache.set(
                        key=cache_key,
                        value=self.access_token,
                        expire=expire or timedelta(seconds=7100).total_seconds()
                    )
                if isinstance(self.cache, (redis.Redis, redis.StrictRedis)):
                    self.cache.setex(
                        name=cache_key,
                        value=self.access_token,
                        time=expire or timedelta(seconds=7100),
                    )

        return self

    def token(
            self,
            **kwargs
    ):
        """
        @see https://console-docs.apipost.cn/preview/b4e4577f34cac87a/1b45a97352d07e60/?target_id=71e7934a-afce-4fd3-a897-e2248502cc94
        :param kwargs:
        :return:
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("response_handler", ResponseHandler.success)
        kwargs.setdefault("method", py3_requests.RequestMethod.GET)
        kwargs.setdefault("url", RequestUrl.OPEN_AUTH_TOKEN)
        if not kwargs.get("url", "").startswith("http"):
            kwargs["url"] = self.base_url + kwargs["url"]
        kwargs.setdefault("params", Dict())
        kwargs.params.setdefault("secret", self.secret)
        result = py3_requests.request(**kwargs.to_dict())
        if Draft202012Validator({"type": "string", "minLength": 1}).is_valid(result):
            self.access_token = result
        return self
