# coding: utf-8
import os
from datetime import datetime
from collector import settings
import hashlib
from collector.utils.utilities import BloomInstance
import json


def create_dir(folder_name):
    path = os.path.join(settings.WEBPAGE_STORAGE, folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
    webpage_path = os.path.join(path, str(datetime.now().date()))
    if not os.path.exists(webpage_path):
        os.makedirs(webpage_path)
    return webpage_path


def save(response, webpage_path):
    hash_md5 = hashlib.md5()
    hash_md5.update(response.url.encode())
    webpage_name = hash_md5.hexdigest()
    data = dict(
        html=response.text,
        url=response.url
    )
    with open(os.path.join(webpage_path, webpage_name), 'w') as f:
        json.dump(data, f)
    return webpage_name


def save_webpage(response, webpage_path, selectors, use_bloom=settings.USE_BLOOM):
    """
    对传入的对象进行判重，重复的跳过，不重复的保存
    :param response: response 对象
    :param webpage_path: 保存路径
    :param selectors: 判重用的选择器
    :param use_bloom: 是否使用布隆过滤器
    :return: False代表不存在
    """
    if use_bloom:
        bf = BloomInstance
        content = ''
        if selectors:   # 判断是否传入selectors
            for selector in selectors:
                try:
                    cont = str(response.xpath(selector).extract_first())
                except:
                    cont = ''
                content += cont
            if len(content) < 5:
                content_hash = hashlib.md5(response.body).hexdigest()
            else:
                content_hash = hashlib.md5(content.encode()).hexdigest()
        else:           # 如果没有传入selectors则直接用整个html做hash
            content_hash = hashlib.md5(response.body).hexdigest()

        if bf.isContains(content_hash, settings.REDIS_DB):  # 判断content_hash是否存在
            return False
        else:           # 如果不存在则添加并保存
            bf.insert(content_hash, settings.REDIS_DB)
            return save(response, webpage_path)
    else:
        return save(response, webpage_path)

