# process_manager.py

This is a single-file application that will manage a command by restarting it and ensuring that it is producing some stderr within the hold down timer duration.  I'm happy to expand this to look for liveliness via some other methods as long as it's similar to stderr.  

My original use case is to manage ffmpeg when receiving RTSP, as it will, at least with my feeds, fail to remain connected sometimes but keeps running, so the only way one can notice that it's not connected is that it's not outputting anything.  This also coninides with an end to the stderr output, so that's why I'm writing this to watch that stderr stream.


Copyright 2022 James Delancey

Use of this source code is governed by an MIT-style
license that can be found in the LICENSE file or at
https://opensource.org/licenses/MIT.


```
PS C:\Users\jd\cam_reusable> python process_manager.py --hold_down 6 --sleep_time 2 --max_restarts 2 --debug --cmd  "python process_manager_test.py --init_tempo 1 --linear_backoff 1"
starting 'python process_manager_test.py --init_tempo 1 --linear_backoff 1'
the holddown is: 6
the max_restarts is: 2
stderr from child proc: sample log line with init_tempo: 1 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 2 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 3 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 4 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 5 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 6 and linear_backoff: 1
killed child proc due to ctrl not working
hold_down of 6 is expired, terminating python process_manager_test.py --init_tempo 1 --linear_backoff 1
stderr from child proc: sample log line with init_tempo: 7 and linear_backoff: 1
stderr from child proc: None
waiting 5 seconds before starting subprocess again. restarts this hour 0.
starting 'python process_manager_test.py --init_tempo 1 --linear_backoff 1'
the holddown is: 6
the max_restarts is: 2
stderr from child proc: sample log line with init_tempo: 1 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 2 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 3 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 4 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 5 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 6 and linear_backoff: 1
killed child proc due to ctrl not working
hold_down of 6 is expired, terminating python process_manager_test.py --init_tempo 1 --linear_backoff 1
stderr from child proc: sample log line with init_tempo: 7 and linear_backoff: 1
stderr from child proc: None
waiting 5 seconds before starting subprocess again. restarts this hour 1.
starting 'python process_manager_test.py --init_tempo 1 --linear_backoff 1'
the holddown is: 6
the max_restarts is: 2
stderr from child proc: sample log line with init_tempo: 1 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 2 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 3 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 4 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 5 and linear_backoff: 1
stderr from child proc: sample log line with init_tempo: 6 and linear_backoff: 1
killed child proc due to ctrl not working
hold_down of 6 is expired, terminating python process_manager_test.py --init_tempo 1 --linear_backoff 1
stderr from child proc: sample log line with init_tempo: 7 and linear_backoff: 1
stderr from child proc: None
waiting 5 seconds before starting subprocess again. restarts this hour 2.
max restarts met, closing process_manager.py.
PS C:\Users\jd\cam_reusable> 
```
