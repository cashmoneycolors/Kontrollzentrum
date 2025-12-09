from cx_Freeze import setup, Executable

setup(
    name="ROBOTER_KI_APP",
    version="5.0",
    description="Kontrollzentrum v5.0 - Production Grade System",
    executables=[
        Executable(
            "roboter_ki_gui.py",
            base="Win32GUI",
            target_name="ROBOTER_KI_APP.exe"
        )
    ],
    options={
        "build_exe": {
            "packages": ["tkinter", "subprocess", "sys", "os"],
            "include_files": [
                "main.py",
                "RUN_NOW.py",
                "WEEK_1_EXECUTION.py",
                "WEEK_2_EXECUTION.py",
                "WEEK_3_EXECUTION.py",
                "WEEK_4_EXECUTION.py",
                "core/",
                "modules/",
                "requirements.txt"
            ]
        }
    }
)
