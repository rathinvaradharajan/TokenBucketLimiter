from datetime import datetime


class TokenBucketLimiter:
    def __init__(self, bucket_size, refill_rate):
        """
        A token bucket rate limiter that can be used to determine if a request has exceeded the limits.

        :param bucket_size: The max requests allowed.
        :param refill_rate: The request refresh rate in seconds.
        """
        if bucket_size is None or refill_rate is None:
            raise TypeError("bucket_size and refill_rate can't be null")
        if bucket_size < 1 or refill_rate <= 0:
            raise ValueError("bucket_size and refill rate must be greater than 0.")
        self.bucket_size = bucket_size
        self.refill_rate = refill_rate
        self.currently_allowed = bucket_size
        self.last_refill = datetime.utcnow()

    def __refill(self):
        # refill the bucket from the last refill time.
        now = datetime.utcnow()
        diff = (now - self.last_refill).total_seconds()
        self.currently_allowed = max(self.bucket_size, self.currently_allowed + diff * self.refill_rate)
        self.last_refill = now

    def allow_request(self, tokens: int) -> bool:
        """
        Check if the request can be processed.

        :param tokens: The resource estimated the request would use.
        :return: True if the request can be processed, False if it exceeds its limits.
        """
        self.__refill()
        if self.currently_allowed > tokens:
            self.currently_allowed -= tokens
            return True
        return False
