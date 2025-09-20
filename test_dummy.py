def weight(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # print(n,"before weight")
            result = func(*args, **kwargs)
            # print("after weight")
            return result
        return wrapper
    return decorator

def number(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # print(n,"before number")
            result = func(*args, **kwargs)
            # print("after number")
            return result
        return wrapper
    return decorator

if __name__=="__main__":

    @weight(5)
    @number("1")
    def test():
        print("hi")

    test()
