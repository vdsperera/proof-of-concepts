class Counter:
	class_count = 0

	def __init__(self):
		self.obj_count = 0
		Counter.class_count = 0

	def increment(self):
		self.obj_count += 1
		Counter.class_count += 1

	def get_obj_count(self):
		return f"Object count: {self.obj_count}"

	def get_class_count(self):
		return f"Class count: {Counter.class_count}"

counter1 = Counter()
counter2 = Counter()

counter1.increment()
print(counter1.get_obj_count()) #1
print(counter1.get_class_count()) #1
print(counter2.get_obj_count()) #0
print(counter2.get_class_count()) #1

print("==================================")

counter1.increment()
# counter2.increment()
print(counter1.get_obj_count()) #2
print(counter1.get_class_count()) #2
print(counter2.get_obj_count()) #0
print(counter2.get_class_count()) #2

print("==================================")

counter2.increment()
print(counter1.get_obj_count()) #2
print(counter1.get_class_count()) #3
print(counter2.get_obj_count()) #1
print(counter2.get_class_count()) #3

