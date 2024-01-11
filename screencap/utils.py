def keyboard_interrupt(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt as e:
            raise SystemExit(e) from e

    return inner
