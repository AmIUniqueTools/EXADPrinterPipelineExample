import time
import pytest

APP_ID = "com.amiunique.exadprinterimplementationexample"
@pytest.mark.usefixtures('setWebdriver')
class TestAPP:
    def test_exploration(self):
        import time

        def wait_foreground(driver, duration):
            interval = 30  # must be < 90 seconds
            steps = duration // interval

            for _ in range(int(steps)):
                time.sleep(interval)
                driver.current_package   # lightweight command
        # First run
        wait_foreground(self.driver, 180)

        # Close the app
        self.driver.terminate_app(APP_ID)
        print("First Run done")
        # Small pause
        time.sleep(5)

        # Reopen the app
        self.driver.activate_app(APP_ID)

        # Second run
        wait_foreground(self.driver, 180)
        print("Second Run done")
        assert True