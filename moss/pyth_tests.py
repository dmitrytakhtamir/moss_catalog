import sys
import re

list1 = [i for i in range(1, 10)]
print(list1[6::-2])
tup = (1,2,3,4,5,6,7,8,9)
list2 = {1,2,3,4,5,6,7,8,9}
list3 = list(lambda: i for i in range(1, 10))
print(len(list2))
for i in range(1, 10):
	i -= -5
name = '111'
print(type(list1), type(tup), type(list2))
print(sys.getsizeof(list1), sys.getsizeof(tup), sys.getsizeof(list2))
lst = (f'\'{name}\', ', f', \'{name}\'')
print(list(map(lambda x: x*2, list2)))
new_images = str(['111', 'Ptilium Crista-Castrensis','Andreaeidae', 'Bryum Argentum'])
new_list = list(lambda i: re.sub(i, "", new_images) for i in lst)
#new_list = re.sub('\'\'', '', new_list)
print(new_images)
print(new_list)	
match = re.search('111', new_images)
print(match)

for i in lst:
	res = re.sub(i, "", new_images)
	test = re.search('111', res)
	print(test)
	print(res)
	if test == None:
		print(res, end='ITS WORKING')