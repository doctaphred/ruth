def truncate(s, max_length, continuation='...'):
    effective_max_length = max_length - len(continuation)
    if len(s) > effective_max_length:
        return s[:effective_max_length] + continuation
    else:
        return s
