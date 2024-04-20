import sys
import time

def spinner(seconds: int):
    start_time = time.time()
    elapsed_time = 0
    spinner_symbols = ['-', '\\', '|', '/']
    index = 0

    while elapsed_time < seconds:
        remaining_time = seconds - elapsed_time 
        sys.stdout.write(f"\r{spinner_symbols[index]} Remaining Time: {remaining_time:.1f} seconds")
        sys.stdout.flush()
        time.sleep(0.1)
        elapsed_time = time.time() - start_time
        index = (index + 1) % len(spinner_symbols)
    sys.stdout.flush()
def main():
    spinner(10)


if __name__ == "__main__":
    main()