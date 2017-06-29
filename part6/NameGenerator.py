def NameGenerator(prefix = ""):
    def next_str(s):
        n = len(s)
        for i in range(n-1, -1, -1):
            if s[i] != 'z':
                return s[:i] + chr(ord(s[i])+1) + s[i+1:]
            else:
                s = s[:i] + 'a' + s[i+1:]
        return 'a' + s

    s = ""
    while True:
        s = next_str(s)
        yield prefix + s
