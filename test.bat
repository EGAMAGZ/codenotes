@echo off
cls
IF EXIST codenotes\codenotes.db DEL /F codenotes\codenotes.db
python -m unittest -v
