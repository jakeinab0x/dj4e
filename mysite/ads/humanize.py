
# Really simple naturalsize that is missing from django humanize :(
def naturalsize(count):
    """Returns natural format for reading file sizes:
    >>> naturalsize(12345)
    '12.0KB'
    >>> naturalsize(1234567890)
    '1.1GB'
    >>> naturalsize(100)
    '100B'"""
    fcount = float(count)
    k = 1024
    m = k * k
    g = m * k
    if fcount < k:
        return str(count) + 'B'
    if fcount >= k and fcount < m:
        return str(int(fcount / (k/10.0)) / 10.0) + 'KB'
    if fcount >= m and fcount < g:
        return str(int(fcount / (m/10.0)) / 10.0) + 'MB'
    return str(int(fcount / (g/10.0)) / 10.0) + 'GB'
