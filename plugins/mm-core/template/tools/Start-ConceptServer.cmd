@echo off
pwsh -NoProfile -File "%~dp0Start-ConceptServer.ps1" && start "" http://localhost:5090/
