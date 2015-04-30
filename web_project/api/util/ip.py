def ip2long(ip):
    """convert string ip to integer"""
    try:
        ip_arr = ip.split('.')
        seg1 = long(ip_arr[0])
        seg2 = long(ip_arr[1])
        seg3 = long(ip_arr[2])
        seg4 = long(ip_arr[3])

        return seg1 << 24 | seg2 << 16 | seg3 << 8 | seg4
    except:
        return ip2long('127.0.0.1')