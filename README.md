# Kotlin lightweight IDE 
Application is a GUI tool that allows users to enter a Kotlin script, execute it, and see its output side-by-side.

## Instructions to build and run
Application was designed to work on Windows 10 64-bit, but should work fine on other systems too.
##### Requirements:
1. python version at least 3.9.5
2. installed kotlin cli compiler and added to path, so we can execute command: kotlinc -script foo.kts
3. download this repository

##### Run:
To run the application enter folder with main.py file and type in the terminal / cmd / console
```
python main.py
```
IDE should now start and new window should appear in a second. If you have encountered any problems, please let me know.


## Functionalities:
1. Editor pane where user can enter his code or code from opened file appears.
2. Output pane with results of execution.
3. Write the script to a file and run it using `kotlinc -script foo.kts`.
4. Script might run for a long time, without feeling of our app freezed.
5. Output of the script appears live in output pane as it executes.
6. App shows errors from the execution / if the script couldn’t be interpreted.
7. Status bar at the bottom indicates whether the script is currently running. It also informs user whether any other problems were encountered.
8. Status bar also shows an indication whether the exit code of the last run was non-zero.

## Extra functionalities:
1. IDE highlights language keywords in a color different from the rest of the code. IDE can indicate whether some part of the code is commented or is inside of the string. Number of keywords to color is limited to 30 words and 7 different color, but adding other is very easy (file kotlin keywords). Highlighting is done live, as a user edits the code in editor pane.
2. Location descriptions of errors (e.g. “script:2:1: error: cannot find 'foo' in scope”) is clickable, so users can navigate to the exact cursor positions in code. Clicking once, scrolls window to make certain part of the code visible. Double-click does the same but also make cursor blink at the beginning of that error, so user can instantly start fixing the bug.
3. There is also a mechanism to run the script multiple times. After selecting 'Run -> Run Multiple Times' or 'Run -> Save & Run Multiple Times' a progress bar appears as well as an estimate of the time remaining. The estimate is based on the time elapsed for already finished runs of the batch. However more recent runs are weighted more than older ones.

## Screenshots:
I recommend you to try my app locally on your machine. If you have encountered any problems with code execution, please let me know and check out following screenshots :)
#### That's how GUI looks after opening:

![](https://github.com/FogInTheFrog/jetbrainsTask/blob/master/screenshots/newfile.png)

#### Menu bar with File section expanded:

![](https://github.com/FogInTheFrog/jetbrainsTask/blob/master/screenshots/menu-bar-file.png)

#### When we open file, file browser window should appear:

![](https://github.com/FogInTheFrog/jetbrainsTask/blob/master/screenshots/open-file.png)

#### Menu bar with Run section expanded:

![](https://github.com/FogInTheFrog/jetbrainsTask/blob/master/screenshots/menu-bar-run.png)

#### View after running simple loop code without any errors:

![](https://github.com/FogInTheFrog/jetbrainsTask/blob/master/screenshots/simple-loop-execution.png)

#### View after running some code with errors:

![](https://github.com/FogInTheFrog/jetbrainsTask/blob/master/screenshots/run-null-safety.png)

As you can see, null keyword is highlighted in (2), (4), (6) but it is not inside string as it is lines (1), (3), (5). Moreover IDE detected the comment part at the top.
#### Now have a look at output pane:

![](https://github.com/FogInTheFrog/jetbrainsTask/blob/master/screenshots/non-zero-exit-code.png)

Underlined code segments are clickable. Clicking once, scrolls window to make certain part of the code visible. Double-click not only does the same but also make cursor blink at the beginning of that error, so user can instantly start typing.
#### There is also an option to run code multiple times (in this case we want to run it 3 times): 

![](https://github.com/FogInTheFrog/jetbrainsTask/blob/master/screenshots/run-script-n-times.png)

#### As the script executes, we can see live output in the output pane and progress bar in new window moving with estimated time left:

![](https://github.com/FogInTheFrog/jetbrainsTask/blob/master/screenshots/run-script-n-times.png)

#### Any time we can check our application run status in status bar

![](https://github.com/FogInTheFrog/jetbrainsTask/blob/master/screenshots/run-script-n-times-progressbar-state.png)
