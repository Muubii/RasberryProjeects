import serial
import time

pico_port = "COM14"
baud_rate = 9600

try:
    pico = serial.Serial(pico_port, baud_rate, timeout=1)
    print(f"Connected to Pico on port {pico_port}!")

    # Clear initial debug message from Pico
    while pico.in_waiting > 0:
        debug_message = pico.readline().decode('utf-8').strip()
        print(f"Debug from Pico: {debug_message}")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                print("Please enter a valid input.")
                continue

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            pico.write((user_input + "\n").encode('utf-8')) 
            print(f"Sent to Pico: {user_input}")

            time.sleep(0.5)  
            response = ""
            start_time = time.time()
            while True:
                if pico.in_waiting > 0:
                    response = pico.readline().decode('utf-8').strip()
                    break
                if time.time() - start_time > 2:  # Timeout
                    print("No response from Pico. Ensure the Pico script is running.")
                    break

            if response:
                print(f"Received from Pico: {response}")
        except UnicodeDecodeError as e:
            print(f"Error decoding response from Pico: {e}")
        except KeyboardInterrupt:
            print("\nUser interrupted the script. Exiting gracefully...")
            break

except serial.SerialException as e:
    print(f"Serial error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if 'pico' in locals() and pico.is_open:
        pico.close()
        print("Serial connection closed.")
