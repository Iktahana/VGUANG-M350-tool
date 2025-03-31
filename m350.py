import base64
import hmac
import os


def generate_config(
        config_params,
        config_pri: bytes = "___VBAR_CONFIG_V1.1.0___".encode('utf-8'),
        password: bytes = os.getenv("PASSWORD", "1234567887654321").encode('utf-8'),

):
    """
    Generates a secure configuration string by combining configuration parameters with
    a cryptographic signature. The method encodes configuration data, computes an HMAC
    digest using a secret password, and generates a base64 encoded signature.

    Args:
        config_params (dict): A dictionary where keys are configuration parameter names
            and values are their corresponding values to be included in the configuration.
        config_pri (bytes, optional): The primary configuration identifier used as a prefix
            for the configuration string. Defaults to a predefined byte string.
        password (bytes, optional): The secret key used to generate the HMAC digest for the
            configuration signature. If not explicitly provided, it defaults to an
            environment variable PASSWORD, or "1234567887654321".

    Returns:
        str: A secure configuration string that includes encoded data and a cryptographic
            signature in the format: `CONFIG_PRI + config_data + CONFIG_POS + base64_signature`.
    """
    # Configuration password for HMAC
    CONFIG_POS = "--"  # Configuration content connector

    # Convert config parameters to string format
    config_str = ",".join(f"{k}={v}" for k, v in config_params.items())
    config_msg = f"{{{config_str}}}".encode('utf-8')  # Main configuration message

    # Generate HMAC and base64 encode
    config_hmac = hmac.new(password, config_pri + config_msg, digestmod="md5").digest()
    config_hmac_b64 = base64.b64encode(config_hmac).decode("utf-8")

    # Combine all parts
    return f"{config_pri.decode('utf-8')}{config_msg.decode('utf-8')}{CONFIG_POS}{config_hmac_b64}"


# Example usage
if __name__ == "__main__":
    # Example configuration parameters
    config = {
        "w_mode": 1,
        "ochannel": 64,
        "nochannel": 64,
        "owifi": 1,
        "de_type": 513,
        "devnum": 114514,
        "nfc": 1,
        "nfc_identity_card_enable": 1,
        "nfc_card_protocol": 3,
        "st": 1,
        "len": 8,
        "nft": 0,
        "awifi_s": 2,
        "relayd": 1000,
        "awifi_f": 4,
        "haddr": "http://192.168.0.174:5025/identify/vguang-m350",
        "houttime": 5
    }

    # Generate and print the configuration string
    qr_data = generate_config(config)
    print(qr_data)
