
# http://sonantometry.blogspot.com/


def powersToSonant(powers):
    def code_(c, a):
        if a == 1: return c
        return `a` + c
    def code(c, a):
        if a > 0: return code_(c, a)
        if a < 0: return code_(c.lower(), -a)
        return ""
    codes = "TDMQNRPUVWZ" + "?"*20  # http://www.forumklassika.ru/showthread.php?t=18080&p=1367263&viewfull=1#post1367263
    return ":" + ("".join(code(c,a) for (c,a) in zip(codes, powers)) or "0")


def sonantToPowers(sonant):
    return []  # implement !!!

