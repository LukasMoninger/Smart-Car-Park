import time
import grovepi

# Port-Definition
LED = 2  # Digital Port D2

def setup():
    # Setzt D2 als Ausgang
    grovepi.pinMode(LED, "OUTPUT")

def blink(on_time=1.0, off_time=1.0, cycles=None):
    """
    Lässt die LED blinken.
    :param on_time: Dauer in Sekunden, wie lange die LED an bleibt
    :param off_time: Dauer in Sekunden, wie lange die LED aus bleibt
    :param cycles: Anzahl der Blinkzyklen (None = endlos)
    """
    count = 0
    try:
        while cycles is None or count < cycles:
            # LED einschalten
            grovepi.digitalWrite(LED, 1)
            time.sleep(on_time)
            # LED ausschalten
            grovepi.digitalWrite(LED, 0)
            time.sleep(off_time)
            count += 1
    except KeyboardInterrupt:
        # Bei Strg-C: LED aus und Beenden
        grovepi.digitalWrite(LED, 0)
        print("\nBlinken durch Benutzer unterbrochen.")
    except IOError as e:
        print(f"I/O-Fehler: {e}")
    finally:
        # Stelle sicher, dass LED aus ist
        grovepi.digitalWrite(LED, 0)

if __name__ == "__main__":
    setup()
    # Beispiel: 0.5 s an, 0.5 s aus, 10 Zyklen
    blink(on_time=0.5, off_time=0.5, cycles=10)
