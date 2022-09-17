import hashlib

str = "clve"
result = (hashlib.sha1(str.encode()))

print("The hexadecimal equivalent of SHA1 is : ")
hexa = result.hexdigest()
#hexa = "0x"+hexa
print(int(hexa, 16))