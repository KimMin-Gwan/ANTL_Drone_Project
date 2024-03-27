

data = "mode 0"
data = "key 0 0 0 0"


s_data = data.split(' ')

print(s_data[1:5])

sample = "10"

e_s = sample.encode()

header = b"k "

btye_sameple = header + e_s
print(btye_sameple)



test_str = b"k data"
head, body = test_str.split(b' ', 1)
if head == b"k":
    print(body)
else:
    print("bye")






