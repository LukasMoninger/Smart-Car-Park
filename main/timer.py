import threading


timer_expired = False

def set_flag():
    global timer_expired
    timer_expired = True
    print("Timer expired!")

timer = threading.Timer(60.0, set_flag)
timer.start()
