# AndroidProjectRenamer

# How to use
1. [Download](https://github.com/PrincessYork/AndroidProjectRenamer/archive/master.zip)
2. Unarchive
3. Make backup of target project
4. Run with Python3.*
5. Follow the instructions
6. Clean and rebuild project

### Usage sample

```
host:~ username$ python3 /Users/user/Downloads/AndroidProjectRenamer-master/app.py
AndroidProjectRenamer script 1.0
Developed by PrincessYork 2018

Follow the instruction to change your's project package.
!!!DON'T FORGET TO MAKE A BACKUP BEFORE DOING IT!!!

Project path: /Users/user/Development/AndroidStudioProjects/Test
New package name: test.sample
Old package: sample.test.sample
Will be changed to
New package: test.sample
Press enter to continue...
[LOG]: File MainActivity.java has new package path
[LOG]: remove directory: /Users/princessyork/Development/Android/AndroidStudioProjects/Test/app/src/androidTest/java/princess
[LOG]: remove directory: /Users/princessyork/Development/Android/AndroidStudioProjects/Test/app/src/test/java/princess
[LOG]: remove directory: /Users/princessyork/Development/Android/AndroidStudioProjects/Test/app/src/main/java/princess

Well done! Finally, you should make 'Build/Clean Project' and rebuild project.
P.S. I hope that the result will satisfy you =)
```
