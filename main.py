from ratelimiter import TokenBucketLimiter
import time


def test_rate_limiter():
    ratelimiter = TokenBucketLimiter(1, 0.1)
    assert ratelimiter.allow_request(1) is True
    assert ratelimiter.allow_request(2) is False
    time.sleep(10)
    assert ratelimiter.allow_request(3) is False
    assert ratelimiter.allow_request(1) is True

    try:
        TokenBucketLimiter(None, None)
        assert True is False
    except TypeError as err:
        assert True is True

    try:
        TokenBucketLimiter(-1, 1)
        assert True is False
    except ValueError as err:
        assert True is True



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test_rate_limiter()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
