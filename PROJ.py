from gpiozero import DistanceSensor, Button, Buzzer, Motor
from time import sleep
from tkgpio import TkCircuit

configuration = {
    "name": "Smart WheelChair",
    "width": 1000,
    "height": 600,
    "motors": [
        {"x": 450, "y": 50, "name": "DC1", "forward_pin": 8, "backward_pin": 9},
        {"x": 450, "y": 250, "name": "DC2", "forward_pin": 10, "backward_pin": 11},
    ],
    "buttons": [
        {"x": 20, "y": 30, "name": "FPB", "pin": 14},
        {"x": 80, "y": 30, "name": "BPB", "pin": 15},
        {"x": 160, "y": 30, "name": "LPB", "pin": 16},
        {"x": 240, "y": 30, "name": "RPB", "pin": 3},
        {"x": 300, "y": 30, "name": "SPB", "pin": 2},
        {"x": 360, "y": 30, "name": "HPB", "pin": 1},
    ],
    "distance_sensors": [
        {"x": 100, "y": 130, "name": "US1", "trigger_pin": 17, "echo_pin": 18, "min_distance": 0, "max_distance": 30},
        {"x": 100, "y": 230, "name": "US2", "trigger_pin": 19, "echo_pin": 22, "min_distance": 0, "max_distance": 30},
        {"x": 100, "y": 330, "name": "US3", "trigger_pin": 20, "echo_pin": 21, "min_distance": 0, "max_distance": 30},
        {"x": 100, "y": 430, "name": "US4", "trigger_pin": 23, "echo_pin": 5, "min_distance": 0, "max_distance": 30},
    ],
    "buzzers": [
        {"x": 550, "y": 50, "name": "buzzer", "pin": 4},
    ]
}
circuit = TkCircuit(configuration)


@circuit.run
def main():
    buzzer = Buzzer(4)
    DC1 = Motor(forward=8, backward=9)
    DC2 = Motor(forward=10, backward=11)
    State = ["Idle", "Forward", "Backward", "Left", "Right", "Obstacle Detected", "Recording", "Help", "Emergency"]

    US1 = DistanceSensor(18, 17)
    US2 = DistanceSensor(22, 19)
    US3 = DistanceSensor(21, 20)
    US4 = DistanceSensor(5, 23)

    FPB = Button(14)
    BPB = Button(15)
    LPB = Button(16)
    RPB = Button(3)
    SPB = Button(2)
    HPB = Button(1)

    def FPB_pressed():
        global current_state
        DC1.forward()
        DC2.forward()
        buzzer.off()
        current_state = "Forward"
        print("FPB is pressed, moving:", current_state)

    def BPB_pressed():
        global current_state
        DC1.backward()
        DC2.backward()
        buzzer.off()
        current_state = "Backward"
        print("BPB is pressed, moving:", current_state)

    def LPB_pressed():
        global current_state
        DC1.backward()
        DC2.forward()
        buzzer.off()
        current_state = "Left"
        print("LPB is pressed, moving:", current_state)

    def RPB_pressed():
        global current_state
        DC1.forward()
        DC2.backward()
        buzzer.off()
        current_state = "Right"
        print("RPB is pressed, moving:", current_state)

    def SPB_pressed():
        global current_state
        DC1.stop()
        DC2.stop()
        buzzer.off()
        current_state = "Idle"
        print("SPB is pressed, Current State:", current_state)

    def HPB_pressed():
        global current_state
        DC1.stop()
        DC2.stop()
        buzzer.off()
        current_state = "Help"
        print("HPB is pressed, Current State:", current_state)

    def stop_motors():
        global current_state
        DC1.stop()
        DC2.stop()
        buzzer.off()
        current_state = "Idle"
        print("Button released. Current State:", current_state)



    FPB.when_pressed = FPB_pressed
    FPB.when_released = stop_motors
    BPB.when_pressed = BPB_pressed
    BPB.when_released = stop_motors
    LPB.when_pressed = LPB_pressed
    LPB.when_released = stop_motors
    RPB.when_pressed = RPB_pressed
    RPB.when_released = stop_motors
    SPB.when_pressed = SPB_pressed
    SPB.when_released = stop_motors
    HPB.when_pressed = HPB_pressed
    HPB.when_released = stop_motors

    obstacle_threshold = 0.05
    current_state = "Idle"

    def get_dist1():
        return US1.distance

    def get_dist2():
        return US2.distance

    def get_dist3():
        return US3.distance

    def get_dist4():
        return US4.distance

    while True:
        d1 = get_dist1()
        d2 = get_dist2()
        d3 = get_dist3()
        d4 = get_dist4()

        if d1 < obstacle_threshold:
            current_state = "Obstacle Detected"
            DC1.stop()
            DC2.stop()
            buzzer.on()
            print("Obstacle Detected Ahead! At: {:.2f} m".format(d1))
        elif d2 < obstacle_threshold:
            current_state = "Obstacle Detected"
            DC1.stop()
            DC2.stop()
            buzzer.on()
            print("Obstacle Detected Behind! At: {:.2f} m".format(d2))
        elif d3 < obstacle_threshold:
            current_state = "Obstacle Detected"
            DC1.stop()
            DC2.stop()
            buzzer.on()
            print("Obstacle Detected on Right! At: {:.2f} m".format(d3))
        elif d4 < obstacle_threshold:
            current_state = "Obstacle Detected"
            DC1.stop()
            DC2.stop()
            buzzer.on()
            print("Obstacle Detected on Left! At: {:.2f} m".format(d4))
        else:
            if current_state == "Obstacle Detected":
                current_state = "Idle"
                DC1.stop()
                DC2.stop()
                buzzer.off()
                print("No Obstacle Detected")

        # Introduce a small delay to avoid excessive loop iteration
        sleep(0.1)
