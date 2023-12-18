from threading import Thread

def m():
    while True:
        print("b")

Thread(target=m, daemon=True).start()
while True:
    print("a")