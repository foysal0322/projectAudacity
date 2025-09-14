import sys
import threading
import subprocess
import signal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QCheckBox, QTextEdit, QLineEdit, QGroupBox, QRadioButton, QGridLayout, QSpinBox
)
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QFont
import os
import glob

class TestRunnerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automated Test Runner")
        self.setGeometry(100, 100, 1100, 700)
        self.process = None
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("QWidget { background-color: #23272e; color: #eaeaea; } QLabel { font-weight: bold; } QComboBox, QSpinBox, QLineEdit { background: #2c313c; color: #eaeaea; border-radius: 4px; } QPushButton { background: #3a3f4b; color: #eaeaea; border-radius: 4px; padding: 6px 16px; font-weight: bold; } QPushButton:disabled { background: #444950; color: #888; } QCheckBox { font-weight: normal; } QTextEdit { border-radius: 6px; }")
        main_layout = QVBoxLayout()
        controls_layout = QGridLayout()
        controls_layout.setSpacing(18)

        # Test suite selection (by pytest mark)
        self.suite_label = QLabel("Test Suite (.mark):")
        self.suite_combo = QComboBox()
        self.suite_combo.addItem("All")
        self.suite_combo.addItems(self.get_all_marks())
        controls_layout.addWidget(self.suite_label, 0, 0)
        controls_layout.addWidget(self.suite_combo, 0, 1)

        # Browser selection
        self.browser_label = QLabel("Browser:")
        self.browser_combo = QComboBox()
        self.browser_combo.addItems(["Chrome", "Firefox", "Edge", "Mobile Chrome", "Mobile Safari"])
        controls_layout.addWidget(self.browser_label, 0, 2)
        controls_layout.addWidget(self.browser_combo, 0, 3)

        # Headless checkbox
        self.headless_checkbox = QCheckBox("Headless")
        self.headless_checkbox.setChecked(True)
        controls_layout.addWidget(self.headless_checkbox, 0, 4)

        # Run in parallel checkbox
        self.parallel_checkbox = QCheckBox("Run in Parallel")
        controls_layout.addWidget(self.parallel_checkbox, 0, 5)

        # Rerun on fail
        self.rerun_label = QLabel("Rerun on Fail:")
        self.rerun_spin = QSpinBox()
        self.rerun_spin.setMinimum(0)
        self.rerun_spin.setMaximum(10)
        self.rerun_spin.setValue(0)
        controls_layout.addWidget(self.rerun_label, 1, 0)
        controls_layout.addWidget(self.rerun_spin, 1, 1)

        # Generate report
        self.report_checkbox = QCheckBox("Generate HTML Report")
        controls_layout.addWidget(self.report_checkbox, 1, 2)

        # Run selected suite
        self.run_suite_btn = QPushButton("Run")
        self.run_suite_btn.setMinimumWidth(90)
        self.run_suite_btn.clicked.connect(self.run_selected_suite)
        controls_layout.addWidget(self.run_suite_btn, 1, 3)

        # Kill button (smaller, right-aligned)
        self.kill_btn = QPushButton("Kill")
        self.kill_btn.setFixedWidth(60)
        self.kill_btn.setStyleSheet("background-color: #d9534f; color: white; font-weight: bold; border-radius: 4px; padding: 4px 0px;")
        self.kill_btn.clicked.connect(self.kill_process)
        controls_layout.addWidget(self.kill_btn, 1, 5, alignment=Qt.AlignRight)

        # Terminal output canvas
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setFont(QFont("Consolas", 11))
        self.terminal.setStyleSheet("background-color: #181818; color: #00FF00; border-radius: 6px;")

        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.terminal)
        self.setLayout(main_layout)

    def get_all_marks(self):
        # Parse all test files for pytest marks
        marks = set()
        for file in glob.glob("tests/test_*.py"):
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip().startswith("@pytest.mark."):
                        mark = line.strip().split("@pytest.mark.")[1].split("(")[0].split(" ")[0]
                        if mark:
                            marks.add(mark)
        return sorted(list(marks))

    def build_pytest_command(self, suite, browser, rerun, report, parallel=False, headless=True):
        cmd = [sys.executable, "-m", "pytest"]
        if suite != "All":
            cmd += ["-m", suite]
        if browser in ["Chrome", "Firefox", "Edge"]:
            cmd += [f"--browser={browser.lower()}"]
        elif browser == "Mobile Chrome":
            cmd += ["--browser=chrome", "--mobile"]
        elif browser == "Mobile Safari":
            cmd += ["--browser=safari", "--mobile"]
        if headless:
            cmd += ["--headless"]
        if rerun > 0:
            cmd += [f"--reruns={rerun}"]
        if report:
            cmd += ["--html=reports/report.html", "--self-contained-html"]
        if parallel:
            cmd += ["-n", "auto"]
        cmd += ["tests/"]
        return cmd

    def run_selected_suite(self):
        suite = self.suite_combo.currentText()
        self.set_run_buttons_enabled(False)
        self.run_tests(suite=suite)

    def run_tests(self, suite):
        browser = self.browser_combo.currentText()
        rerun = self.rerun_spin.value()
        report = self.report_checkbox.isChecked()
        parallel = self.parallel_checkbox.isChecked()
        headless = self.headless_checkbox.isChecked()
        cmd = self.build_pytest_command(suite, browser, rerun, report, parallel, headless)
        self.terminal.clear()
        self.terminal.append(f"Running: {' '.join(cmd)}\n")
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stdout)
        self.process.finished.connect(self.process_finished)
        self.process.start(cmd[0], cmd[1:])

    def handle_stdout(self):
        data = self.process.readAllStandardOutput().data().decode()
        self.terminal.moveCursor(self.terminal.textCursor().End)
        self.terminal.insertPlainText(data)
        self.terminal.moveCursor(self.terminal.textCursor().End)

    def process_finished(self):
        self.terminal.append("\nTest run finished.")
        self.set_run_buttons_enabled(True)

    def set_run_buttons_enabled(self, enabled):
        self.run_suite_btn.setEnabled(enabled)
        self.parallel_checkbox.setEnabled(enabled)
        self.headless_checkbox.setEnabled(enabled)

    def kill_process(self):
        if self.process and self.process.state() == QProcess.Running:
            self.process.kill()
            self.terminal.append("\nAll running tests have been killed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TestRunnerGUI()
    gui.show()
    sys.exit(app.exec_())
