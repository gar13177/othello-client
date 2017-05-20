import md5

m = md5.new()
m2 = md5.new()

a = '1'*(65)

m.update(a)
m2.update(a)
val = m.hexdigest()
print val
print m2.hexdigest()