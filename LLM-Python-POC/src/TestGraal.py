import java.util.ArrayList
from java.util import ArrayList
assert java.util.ArrayList == ArrayList

Math = java.type('org.cornell.Math')

print(Math.abs(-4))

al = ArrayList()
al.add(1)
al.add(12)
print(al)
assert list(al) == [1, 12]


# Access Java's System class
System = java.type("java.lang.System")

# Call Java methods
System.out.println("Hello from Java!")

# Create a Java object
arrayList = java.type("java.util.ArrayList")()
arrayList.add("Python")
arrayList.add("Java")

# Access the list from Python
print(arrayList.get(0))