import ctypes

# 先编译为动态库so文件
# gcc -shared -fPIC -o extend_c.so extend_c.c
extend = ctypes.cdll.LoadLibrary("./extend_c.so")

# 调用普通方法
extend.hello()
print(extend.gcd(36, 48))

# 传入数组
len_nums = 3
Int_Array_3 = ctypes.c_int * len_nums
nums = Int_Array_3()
nums[0] = 4
nums[1] = 5
nums[2] = 8
extend.each(ctypes.byref(nums), len_nums)


class data_t(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
    ]


d = data_t()
extend.test(ctypes.byref(d))
print(d.x, d.y)
