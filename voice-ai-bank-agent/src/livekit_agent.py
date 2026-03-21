import threading
import time


class LiveKitAgent:
    """
    Lightweight LiveKit-style agent simulation.

    Purpose:
    - Represents real-time voice session handling
    - Keeps architecture aligned with LiveKit-based systems
    - Avoids heavy setup while demonstrating design understanding
    """

    def __init__(self):
        self.is_running = False
        self.session_thread = None

    def start(self):
        """
        Starts a simulated LiveKit session loop.
        """
        if self.is_running:
            print("[LiveKit] Session already running.")
            return

        print("[LiveKit] Initializing agent...")
        self.is_running = True

        # Start background thread to simulate real-time session
        self.session_thread = threading.Thread(target=self._run_session, daemon=True)
        self.session_thread.start()

    def _run_session(self):
        """
        Simulated real-time session loop.
        """
        print("[LiveKit] Session started. Listening for audio streams...")

        while self.is_running:
            # Simulate heartbeat / real-time connection
            time.sleep(2)
            print("[LiveKit] Session active...")

    def stop(self):
        """
        Stops the session cleanly.
        """
        if not self.is_running:
            return

        print("[LiveKit] Stopping session...")
        self.is_running = False

        if self.session_thread:
            self.session_thread.join(timeout=1)

        print("[LiveKit] Session stopped.")
