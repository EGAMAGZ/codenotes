@echo off
cls
IF EXIST codenotes.log DEL /F codenotes.log
IF EXIST codenotes\codenotes.db DEL /F codenotes\codenotes.db
python -m unittest -v
