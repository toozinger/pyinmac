@echo off
set TESTDIR=%~dp0
set PYTHONPATH=%TESTDIR%..\..;%PYTHONPATH%
python -m unittest discover -s %TESTDIR% -v
