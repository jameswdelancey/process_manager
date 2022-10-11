# Copyright 2022 James Delancey
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.

import signal
import sys
import time
import os


def slowing_print_loop(init_tempo, linear_backoff):
    while True:
        time.sleep(init_tempo)
        print(
            f"sample log line with init_tempo: {init_tempo} and linear_backoff: {linear_backoff}",
            flush=True,
            file=sys.stderr,
        )
        init_tempo += linear_backoff


def main(argv):
    result = 1

    try:
        i = 1
        while i < len(argv):
            if i == 0:
                i += 1
            elif argv[i] == "--init_tempo":
                i += 1
                init_tempo = int(argv[i])
                i += 1
            elif argv[i] == "--linear_backoff":
                i += 1
                linear_backoff = int(argv[i])
                i += 1
            else:
                i += 1

        slowing_print_loop(init_tempo, linear_backoff)

        result = 0
    except (KeyboardInterrupt, SystemExit) as e:
        print(
            f"the process_manager_test was interrupted by {e!r}, exit_code: {result}",
            flush=True,
            file=sys.stderr,
        )
    except Exception as e:
        print(
            f"the process_manager_test was interrupted by {e!r}, exit_code: {result}",
            flush=True,
            file=sys.stderr,
        )

    return result


if __name__ == "__main__":
    sys.exit(main(sys.argv))
