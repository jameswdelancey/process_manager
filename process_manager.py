# Copyright 2022 James Delancey
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import queue
import shlex
import signal
import subprocess
import sys
import threading
import time

hold_down = 0
hold_down_start = 0
sleep_time = 0
debug = False
daemoncmd = ""
phandle = None
qu = queue.Queue()
line_buf = ""
t = None
stop_thread = False
max_restarts = 0
num_restarts = 0


def stream_to_queue_thread_worker():
    global hold_down, stop_thread
    while stop_thread is not True:
        try:
            for _line_buf in iter(phandle.stderr.readline, b""):
                _line_buf = _line_buf.rstrip()
                if not len(_line_buf):
                    qu.put(None)
                    time.sleep(1)
                else:
                    qu.put(_line_buf)
                    #
                    hold_down = hold_down_start
        except Exception:
            time.sleep(1)


def check_line_buf():
    try:
        line_buf = qu.get_nowait()
        if debug:
            print(f"stderr from child proc: {line_buf}", flush=True, file=sys.stderr)
    except queue.Empty:
        line_buf = None
    return line_buf


def main(argv):
    global stop_thread, hold_down, phandle, debug, hold_down_start, max_restarts, num_restarts
    result = 1

    try:
        i = 1
        while i < len(argv):
            if i == 0:
                i += 1
            elif argv[i] == "--hold_down":
                i += 1
                hold_down_start = int(argv[i])
                i += 1
            elif argv[i] == "--debug":
                debug = True
                i += 1
            elif argv[i] == "--sleep_time":
                i += 1
                sleep_time = int(argv[i])
                i += 1
            elif argv[i] == "--max_restarts":
                i += 1
                max_restarts = int(argv[i])
                i += 1
            elif argv[i] == "--cmd":
                i += 1
                daemoncmd = argv[i]
                i += 1
            else:
                i += 1

        t = threading.Thread(target=stream_to_queue_thread_worker)
        t.start()
        while num_restarts <= max_restarts:
            hold_down = hold_down_start
            print(f"starting {daemoncmd!r}", flush=True, file=sys.stderr)
            print(f"the holddown is: {hold_down}", flush=True, file=sys.stderr)
            print(f"the max_restarts is: {max_restarts}", flush=True, file=sys.stderr)
            phandle = subprocess.Popen(
                shlex.split(daemoncmd),
                universal_newlines=True,
                bufsize=1,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                if "CREATE_NEW_PROCESS_GROUP" in dir(subprocess)
                else 0,
            )
            while phandle.poll() is None:
                # while the child is alive
                while hold_down > 0:

                    while check_line_buf() is not None:
                        hold_down = hold_down_start
                    # while end: child is not awaiting read

                    time.sleep(sleep_time)
                    hold_down -= sleep_time
                # while end: the hold down expired
                if phandle.poll() is None:
                    phandle.send_signal(
                        signal.CTRL_C_EVENT
                        if "CTRL_C_EVENT" in dir(signal)
                        else signal.SIGINT
                    )
                time.sleep(1)
                if phandle.poll() is None:
                    phandle.kill()
                    print(
                        "killed child proc due to ctrl not working",
                        flush=True,
                        file=sys.stderr,
                    )
                print(
                    f"hold_down of {hold_down_start} is expired, terminating {daemoncmd}",
                    flush=True,
                    file=sys.stderr,
                )

                while check_line_buf() is not None:
                    hold_down = hold_down_start
                # while end: child is not awaiting read

                phandle.wait()
            # while end: child is not alive
            print(
                f"waiting 5 seconds before starting subprocess again. restarts this hour {num_restarts}.",
                flush=True,
                file=sys.stderr,
            )
            num_restarts += 1
            time.sleep(5)

        print(
            f"max restarts met, closing process_manager.py.",
            flush=True,
            file=sys.stderr,
        )
        result = 0
    except (KeyboardInterrupt, SystemExit) as e:
        print(
            f"the process_manager was interrupted by {e!r}, exit_code: {result}",
            flush=True,
            file=sys.stderr,
        )
        result = 0
    except Exception as e:
        print(
            f"the process_manager was interrupted by {e!r}, exit_code: {result}",
            flush=True,
            file=sys.stderr,
        )
    finally:
        if phandle.poll() is None:
            phandle.send_signal(
                signal.CTRL_C_EVENT if "CTRL_C_EVENT" in dir(signal) else signal.SIGINT
            )
        time.sleep(1)
        if phandle.poll() is None:
            phandle.kill()
            print(
                f"killed child proc due to ctrl not working",
                flush=True,
                file=sys.stderr,
            )

        while check_line_buf() is not None:
            hold_down = hold_down_start
        # while end: child is not awaiting read

        phandle.wait()

    return result


if __name__ == "__main__":
    sys.exit(main(sys.argv))
