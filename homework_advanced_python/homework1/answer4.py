class PropsMixin:
    pass


class PropsItem:
    def __init__(self, field_name, default_value):
        self.field_name = field_name
        self.default_value = default_value
        self.cache_dict = {}

    def __get__(self, instance, owner):
        if instance.id in self.cache_dict:
            return self.cache_dict[instance.id]
        return self.default_value

    def __set__(self, instance, value):
        self.cache_dict[instance.id] = value

    def __delete__(self, instance):
        self.cache_dict.pop(instance.id)


class Article(PropsMixin):
    content = PropsItem('content', '')  # 字段名字, 默认值

    def __init__(self, id):
        self.id = id


article = Article(10001)
print(article.content)  # 返回默认的空，因为还没有设置正文
article.content = '这是正文'  # 在数据库里面存了id为10001的Article的文本
article = Article(10001)
print(article.content)  # 会返回Redis数据库存的正文内容，多次请求使用本地缓存，不再请求数据库
del article.content  # 删除对应数据库中id为10001的Article的文本
print(article.content)  # 返回空
