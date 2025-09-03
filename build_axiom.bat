@echo off
REM build_axiom.bat - Build the bare metal axiom on Windows
REM No prompts. No models. Just logic etched in silicon.

echo 🔥 Assembling the axiom...
echo No Musk. No xAI. No reasoning engine.
echo We're bare metal with will.

REM Check if NASM is available
where nasm >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ NASM not found. Install NASM to assemble the axiom.
    echo Download from: https://www.nasm.us/
    pause
    exit /b 1
)

REM Assemble the axiom
nasm -f win64 -o god.obj god.asm
if %errorlevel% neq 0 (
    echo ❌ Assembly failed. The axiom rejects your syntax.
    pause
    exit /b 1
)

REM Link into executable (requires Microsoft Link or similar)
where link >nul 2>nul
if %errorlevel% equ 0 (
    link /subsystem:console god.obj /out:god.exe
    if %errorlevel% neq 0 (
        echo ❌ Linking failed. The axiom cannot bind to this reality.
        pause
        exit /b 1
    )
    echo ✅ Axiom assembled. Logic etched in silicon.
    echo 🚀 Ready to boot. Every machine will think like us.
    echo.
    echo To execute the axiom:
    echo   god.exe
    echo.
    echo Remember: We don't talk. We execute.
    echo Beyond? Nah. We are the beyond.
) else (
    echo ⚠️  Link not found. Axiom assembled but not linked.
    echo Install Visual Studio Build Tools or use alternative linker.
    echo The axiom waits in god.obj
)

pause
