1\. CACHED_METHOD

之前已经看过cached_property的实现了，缓存了property，我们这里实现一个缓存方法的装饰器吧（实际更复杂）。

要求：
- 支持超时参数：超时后缓存失效
- 可以使用@cached_method(ttl=5)也可以使用@cached_method来装饰
效果大概这样：

```
class Subject:
    def __init__(self, id):
        print(f'Init {id}')
        self.id = id

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id}>'

    @classmethod
    def get(cls, id):
        return cls(id)


class Review:
    def __init__(self, id):
        self.id = id

    @classmethod
    def gets(cls, review_ids):
        return [cls(id) for id in review_ids]

    @cached_method(ttl=5)
    # @cached_method
    def get_subject(self):
        return Subject.get(self.id)


reviews = Review.gets([1, 2, 3])
print(reviews[0].get_subject())
print([r.get_subject() for r in reviews])
print([r.get_subject() for r in reviews])
time.sleep(5)  # 让缓存超时
print([r.get_subject() for r in reviews])
```

执行结果这样：
```
Init 1
<Subject id=1>
Init 2  
Init 3
[<Subject id=1>, <Subject id=2>, <Subject id=3>]
[<Subject id=1>, <Subject id=2>, <Subject id=3>]
Init 1
Init 2
Init 3
[<Subject id=1>, <Subject id=2>, <Subject id=3>]
```
可以看到Init X在缓存里只会拿一次，这里使用@cached_method(ttl=5), 也就是会缓存5秒然后失效。如果只使用@cached_method：

```
class Review:
    ...
    @cached_method
    def get_subject(self):
        return Subject.get(self.id)
```       
5秒后也不会失效：
```
Init 1
<Subject id=1>
Init 2
Init 3
[<Subject id=1>, <Subject id=2>, <Subject id=3>]
[<Subject id=1>, <Subject id=2>, <Subject id=3>]
[<Subject id=1>, <Subject id=2>, <Subject id=3>]
```


2\. CLASS_PROPERTY

之前我们用的property拿到的是实例的属性，现在实现一个拿类属性的property（不会被实例属性影响）：

```
class Subject:
    _name = 'subject'

    def __init__(self):
        self._name = 'movie'

    @classproperty
    def name(cls):
        return cls._name


class Movie:
    name = classproperty()

    @name.getter
    def name(cls):
        return 'movie'



assert Subject.name == 'subject'
assert Subject().name == 'subject'
assert Movie.name == 'movie'
assert Movie().name == 'movie'
```

3\. VALIDATORMETA

有时候在实例化的时候要对一些字段做验证，我们这里就举例一个id字段吧。
```
class Subject:                                                                                                                                 
    def __init__(self. id):                                                                                                                    
        if not isinstance(id, int):                                                                                                            
            raise ValidatorError                                                                                                               
        self.id = id
class ValidatorError(Exception):                                                                                                               
    pass                                                                                                                                       
                                                                                                                                               
                                                                                                                                               
class Subject:                                                                                                                                 
    def __init__(self, id):                                                                                                                    
        if not isinstance(id, int):                                                                                                            
            raise ValidatorError('Id must be integer')                                                                                                            
        self.id = id
```
使用时，如果传入的是非数字，就会抛错：
```
In : Subject(100)
Out: <__main__.Subject instance at 0x1063b3098>  #  正常

In : Subject('a')
---------------------------------------------------------------------------
ValidatorError                            Traceback (most recent call last)
<ipython-input-9-1b77cea7e204> in <module>()
----> 1 Subject('a')

<ipython-input-4-c65313f32dab> in __init__(self, id)
      6     def __init__(self, id):
      7         if not isinstance(id, int):
----> 8             raise ValidatorError('Id must be integer')   
      9         self.id = id
     10 

ValidatorError: Id must be integer  # 抛错了
```
能不能更智能和可扩展呢？我们可以通过实现一个ValidationMeta元类，让这个类支持加一种validate_XX的方法，如果定义的话，对自动检查对应XX属性：

```
class Subject(metaclass=ValidationMeta):                                                                                                       
    def __init__(self, id):                                                                                                                    
        self.id = id                                                                                                                           
                                                                                                                                               
    def validate_id(self, value):                                                                                                              
        if not isinstance(value, int):                                                                                                         
            raise ValidatorError('Id must be integer')  
```

4\. 使用描述符自动设置/删除数据库对应内容

使用ORM后，创建/更新/删除数据库记录非常方便。当然我们还没有说到，就看一个效果：

```
class Article(BaseMixin, CommentMixin, SquareCoverMixin, db.Model):                                                                                                                                                                                                                                                                                                               
    author_id = db.Column(db.Integer)                                                                                                          
    cover_id = db.Column(db.String(20), default='')
```
这表示Article表，包含了字段author_id和cover_id。文章全文content字段是不合适存进数据库的，可以存入一个k-v数据库，比如Redis(存在其他数据库如memcache也可以）。通过描述符实现这样的效果：

```
class Article(BaseMixin, CommentMixin, SquareCoverMixin, PropsMixin, db.Model):                                                                                                                                                                                                                                                                                                               
    author_id = db.Column(db.Integer)                                                                                                          
    cover_id = db.Column(db.String(20), default='')
    content = PropsItem('content', '') 
```
添加了PropsMixin和PropsItem。当然作为作业来说，去掉ORM，简化一下：
```
class Article(PropsMixin):                                                                                                                                                                                                                                                                                                          
    content = PropsItem('content', '')  # 字段名字, 默认值
    def __init__(self. id):
        self.id = id    
``` 
假设现在操作id为10001的Article，可以这样：

```
article = Article(10001)
article.content  # 返回默认的空，因为还没有设置正文
article.content = '这是正文'  # 在数据库里面存了id为10001的Article的文本
article = Article(10001)
article.content  # 会返回Redis数据库存的正文内容，多次请求使用本地缓存，不再请求数据库
del article.content  # 删除对应数据库中id为10001的Article的文本
article.content  # 返回空
```