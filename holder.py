def write():
    with open("test", "wb") as fl:
        fl.writelines(["root\n", "creawib\n", "192.168.0.1\n"])
        fl.seek(0)

write()
lines = file("test", "rb")
for i in lines:
    print i