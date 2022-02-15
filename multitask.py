import time
import threading


def toothbrush(brand):
    for i in range(10):
        print("แปรงฟันอยู่...ยาสีฟันยี่ห้อ " + brand)
        time.sleep(0.3)


def shower(soup, gel):
    for i in range(10):
        print("กำลังอาบน้ำ...สบู่ {} ยาสระผม {}".format(soup, gel))
        time.sleep(1)


task1 = threading.Thread(target=toothbrush, args=("Colgate",))
task2 = threading.Thread(target=shower, args=("Lux", "Rejoy"))

start = time.time()

# toothbrush()
# shower()

task1.start()
task2.start()

task1.join()
task2.join()

end = time.time()

print("All time = ", end - start)
print("-------")
print("-------ไปโรงเรียนได้แล้ว--------")
