from pathlib import Path

import cv2


class Camera:
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index

    def capture(self, output_path: str | Path) -> Path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        camera = cv2.VideoCapture(self.camera_index)

        if not camera.isOpened():
            raise RuntimeError(
                f"Kunne ikke åpne kamera med indeks {self.camera_index}"
            )

        try:
            # Kameraet kan trenge noen bilder før eksponeringen stabiliseres.
            frame = None

            for _ in range(5):
                success, frame = camera.read()

                if not success:
                    frame = None

            if frame is None:
                raise RuntimeError("Kameraet returnerte ikke noe bilde")

            success = cv2.imwrite(str(output_path), frame)

            if not success:
                raise RuntimeError(f"Kunne ikke lagre bildet som {output_path}")

            return output_path
        finally:
            camera.release()