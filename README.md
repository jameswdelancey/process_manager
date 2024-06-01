# Process Manager

This repository hosts a single-file application designed to manage a command by restarting it and ensuring it produces stderr output within a specified hold down timer duration. Initially created to manage ffmpeg when receiving RTSP streams, the application monitors stderr output to detect connectivity issues.

## Overview

The `process_manager.py` script effectively manages processes by restarting them when necessary and monitoring their stderr output for signs of activity. It offers flexibility in adjusting parameters such as hold down duration, sleep time, and maximum restart attempts.

## Features

- **Process Management**: Automatically restarts processes and monitors their stderr output.
- **Flexible Configuration**: Parameters such as hold down duration, sleep time, and maximum restart attempts can be customized.
- **Error Handling**: Detects unresponsive processes and takes appropriate action to ensure continuous operation.

## Usage

```sh
python process_manager.py --hold_down 6 --sleep_time 2 --max_restarts 2 --debug --cmd  "python process_manager_test.py --init_tempo 1 --linear_backoff 1"
```

- `--hold_down`: Duration in seconds to wait for stderr output from the process.
- `--sleep_time`: Duration in seconds to wait before restarting the process.
- `--max_restarts`: Maximum number of restart attempts before exiting.
- `--debug`: Enable debug mode for verbose output.
- `--cmd`: Command to execute and manage using the process manager.

## Example Output

The script output demonstrates the process management in action, including restarting the process, monitoring stderr output, and terminating when the maximum restart attempts are reached.

## License

This Process Manager application is open-source software licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
