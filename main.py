import json
import os
import uuid
from typing import Optional, Dict
from urllib.parse import urljoin

import qrcode
from PIL import ImageDraw, ImageFont, Image

from m350 import generate_config


def get_default_config() -> Dict:
    """
    Returns the default configuration dictionary for generating the QR code.

    This configuration can be used with `generate_config` to produce
    device-specific data.

    Returns:
        Dict: The default configuration settings as a dictionary.
    """
    return {
        "w_mode": 1,
        "ochannel": 64,
        "nochannel": 64,
        "owifi": 1,
        "de_type": 513,
        "nfc": 1,
        "nfc_identity_card_enable": 0,
        "nfc_card_protocol": 3,
        "st": 1,
        "len": 8,
        "nft": 0,
        "awifi_s": 2,
        "relayd": 1000,
        "awifi_f": 4,
        "haddr": "http://localhost/",
        "houttime": 5
    }


def generate_qrcode(
        text: str,
        file_path: Optional[str] = None,
        version: int = 4,
        error_correction: int = qrcode.constants.ERROR_CORRECT_L,
        box_size: int = 10,
        border: int = 4,
        fill_color: str = "black",
        back_color: str = "white"
) -> Image.Image:
    """
    Generates a QR code from the given text and saves it to a file (optional).

    Args:
        text (str): Textual data to encode in the QR code.
        file_path (Optional[str]): File path to save the QR code image (if given).
        version (int): Controls the size of the QR code matrix. Defaults to 4.
        error_correction (int): Error correction level for QR code. Defaults to `ERROR_CORRECT_L`.
        box_size (int): Size of each pixel in the QR code grid. Defaults to 10.
        border (int): Width of the border in boxes. Defaults to 4.
        fill_color (str): Color for the QR code. Defaults to "black".
        back_color (str): Background color for the QR code. Defaults to "white".

    Returns:
        Image.Image: The generated QR code as a PIL Image object.
    """
    qr = qrcode.QRCode(version=version, error_correction=error_correction, box_size=box_size, border=border)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)

    if file_path:
        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)
        img.save(file_path)

    return img


def main(
        device_name: str = uuid.uuid4().hex,
        url: str = "https://identify.access.networks.stayforge.io/identify/vguang-m350/",
        config: Optional[Dict] = None,
        output_path: str = "./results/",
) -> None:
    """
    Generates device-specific QR codes and saves them as image files.

    Args:
        device_name (str): Device name to include in the QR code. Defaults to a randomly generated UUID.
        url (str): API endpoint for generating the haddr value.
        config (Optional[Dict]): The configuration dictionary. Defaults to using `get_default_config()`.
        output_path (str): Directory where the QR code image will be saved. Defaults to "./results/".
    Raises:
        ValueError: If `device_name` contains non-ASCII characters.
    """
    if not config:
        config = get_default_config()

    # Validate device_name
    if not all(ord(char) < 128 for char in device_name):
        raise ValueError("device_name must contain only ASCII characters")

    # Update configuration with haddr
    config["haddr"] = f'"{urljoin(url, device_name)}"'

    # Generate QR code data
    qr_data = generate_config(config)
    print(f"Generated QR data for {device_name}: {qr_data}")

    # Create QR code image
    save_path = os.path.join(output_path, f"{device_name}.png")
    img = generate_qrcode(qr_data, file_path=save_path)

    # Dynamically calculate font size as 5% of the image height
    font_size = int(img.size[1] * 0.1)  # 高度的 5%
    print(f"Dynamic font size: {font_size}")

    # Annotate QR code image with device_name
    draw = ImageDraw.Draw(img)
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "PTSerif-Italic.ttf")
    font_size = 28

    font = ImageFont.truetype(font_path, font_size)

    draw.text((24, 0)
              , device_name, font=font, fill="black")

    # Save annotated image
    img.save(save_path)
    print(f"QR code saved for {device_name} at: {save_path}")


if __name__ == "__main__":
    try:
        with open("./devices.json", "r") as file:
            device_names = json.load(file)

        for _device_name in device_names:
            main(device_name=_device_name)
    except FileNotFoundError:
        print("Error: File './devices.json' not found.")
