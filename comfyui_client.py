import json
import urllib
from urllib import request
import base64
import random
import websocket
import threading
import time
import struct
import os
from datetime import datetime
prompt_text = r"""
{
  "3": {
    "inputs": {
      "seed": 718737532262803,
      "steps": 40,
      "cfg": 12,
      "sampler_name": "euler_ancestral",
      "scheduler": "karras",
      "denoise": 0.8,
      "model": [
        "39",
        0
      ],
      "positive": [
        "52",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "latent_image": [
        "49",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "Base KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "sd_xl_base_1.0.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Base Safetensors"
    }
  },
  "6": {
    "inputs": {
      "text": [
        "51",
        0
      ],
      "clip": [
        "39",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "Prompt Positive"
    }
  },
  "7": {
    "inputs": {
      "text": "low quality, blurry, deformed, watermark, text, signature, depth of field, photoreal, realistic, closed_eyes, old, wrinkles, red lips",
      "clip": [
        "39",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "Prompt Negative"
    }
  },
  "25": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "26": {
    "inputs": {
      "images": [
        "25",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Raw Image"
    }
  },
  "38": {
    "inputs": {
      "filename_prefix": "pixelbuildings128-v1-raw-",
      "images": [
        "79",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  },
  "39": {
    "inputs": {
      "lora_name": "pixel-art-xl-v1.1.safetensors",
      "strength_model": 1,
      "strength_clip": 1,
      "model": [
        "4",
        0
      ],
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "LoraLoader",
    "_meta": {
      "title": "Load LoRA"
    }
  },
  "49": {
    "inputs": {
      "pixels": [
        "68",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEEncode",
    "_meta": {
      "title": "VAE Encode"
    }
  },
  "50": {
    "inputs": {
      "model": "wd-v1-4-moat-tagger-v2",
      "threshold": 0.3,
      "character_threshold": 0.8,
      "replace_underscore": false,
      "trailing_comma": false,
      "exclude_tags": "realistic, lips",
      "tags": "solo, looking_at_viewer, short_hair, shirt, black_hair, 1boy, closed_mouth, white_shirt, male_focus, black_eyes, shadow, letterboxed, portrait, nose",
      "image": [
        "68",
        0
      ]
    },
    "class_type": "WD14Tagger|pysssss",
    "_meta": {
      "title": "WD14 Tagger 🐍"
    }
  },
  "51": {
    "inputs": {
      "action": "append",
      "tidy_tags": "yes",
      "text_a": [
        "50",
        0
      ],
      "text_b": "solo, face_focus, clean_lines, symmetrical_features, no_textures, no_gradients, retro_style, sharp_edges, high_contrast_shading, flat_colors, young, small lips",
      "text_c": "",
      "result": "solo, looking_at_viewer, short_hair, shirt, black_hair, 1boy, closed_mouth, white_shirt, male_focus, black_eyes, shadow, letterboxed, portrait, nose, solo, face_focus, clean_lines, symmetrical_features, no_textures, no_gradients, retro_style, sharp_edges, high_contrast_shading, flat_colors, young, small lips"
    },
    "class_type": "StringFunction|pysssss",
    "_meta": {
      "title": "String Function 🐍"
    }
  },
  "52": {
    "inputs": {
      "strength": 1,
      "conditioning": [
        "6",
        0
      ],
      "control_net": [
        "54",
        0
      ],
      "image": [
        "68",
        0
      ]
    },
    "class_type": "ControlNetApply",
    "_meta": {
      "title": "Apply ControlNet (OLD)"
    }
  },
  "54": {
    "inputs": {
      "control_net_name": "diffusion_pytorch_model.safetensors"
    },
    "class_type": "ControlNetLoader",
    "_meta": {
      "title": "Load ControlNet Model"
    }
  },
  "65": {
    "inputs": {
      "images": [
        "68",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "68": {
    "inputs": {
      "upscale_method": "nearest-exact",
      "crop": "disabled",
      "image": [
        "76",
        0
      ]
    },
    "class_type": "Resize Image for SDXL",
    "_meta": {
      "title": "Resize Image for SDXL (Mikey)"
    }
  },
  "76": {
    "inputs": {
      "crop_padding_factor": 0.47000000000000003,
      "cascade_xml": "lbpcascade_animeface.xml",
      "image": [
        "80",
        0
      ]
    },
    "class_type": "Image Crop Face",
    "_meta": {
      "title": "Image Crop Face"
    }
  },
  "78": {
    "inputs": {
      "images": [
        "79",
        0
      ]
    },
    "class_type": "PreviewImage",
    "_meta": {
      "title": "Preview Image"
    }
  },
  "79": {
    "inputs": {
      "image": [
        "25",
        0
      ]
    },
    "class_type": "Image Remove Background (rembg)",
    "_meta": {
      "title": "Image Remove Background (rembg)"
    }
  },
  "80": {
    "inputs": {
      "image": ""
    },
    "class_type": "ETN_LoadImageBase64",
    "_meta": {
      "title": "Load Image (Base64)"
    }
  },
  "81": {
    "inputs": {
      "format": "PNG",
      "images": [
        "79",
        0
      ]
    },
    "class_type": "ETN_SendImageWebSocket",
    "_meta": {
      "title": "Send Image (WebSocket)"
    }
  }
}
"""

class ComfyUIClient:
    def __init__(self, server_address, client_id, output_path):
        self.server_address = server_address
        self.client_id = client_id
        self.output_path = output_path
        self.ws = None
        self.is_connected = False
        self.output_dir = "output_images"
        self.received_images = 0
        self.expected_images = 0
        self.completion_event = threading.Event()

    def on_message(self, ws, message):
        """Handle incoming WebSocket messages"""
        if isinstance(message, bytes):
            try:
                if len(message) < 8:
                    print("Binary message too short")
                    return
                
                ints = struct.unpack('>II', message[:8])
                print(f"Received binary message with header values: {ints}")
                
                png_data = message[8:]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.output_path}"
                filepath = os.path.join(filename)
                
                with open(filepath, 'wb') as f:
                    f.write(png_data)
                print(f"Saved image to: {filepath}")
                
                self.received_images += 1
                
            except Exception as e:
                print(f"Error processing binary message: {e}")
        else:
            try:
                data = json.loads(message)
                print("Received JSON message:", json.dumps(data, indent=2))
                
                if isinstance(data, dict) and data.get('type') == 'executed':
                    output_data = data.get('data', {}).get('output', {})
                    if 'images' in output_data:
                        self.expected_images = len(output_data['images'])
                        print(f"Image generation completed. Expected images: {self.expected_images}")
                        
                        # If we've received all expected images, signal completion
                        if self.received_images >= self.expected_images:
                            print("All images received. Closing connection...")
                            self.completion_event.set()
                
            except json.JSONDecodeError:
                print("Received non-JSON message:", message)

    def on_error(self, ws, error):
        """Handle WebSocket errors"""
        print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection closing"""
        print(f"WebSocket connection closed: {close_status_code} - {close_msg}")
        self.is_connected = False

    def on_open(self, ws):
        """Handle WebSocket connection opening"""
        print("WebSocket connection established")
        self.is_connected = True

    def connect(self):
        """Establish WebSocket connection"""
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            f"ws://{self.server_address}/ws?clientId={self.client_id}",
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        
        # Start WebSocket connection in a separate thread
        self.ws_thread = threading.Thread(target=self.ws.run_forever)
        self.ws_thread.daemon = True
        self.ws_thread.start()
        
        # Wait for connection to establish
        timeout = 10
        start_time = time.time()
        while not self.is_connected and time.time() - start_time < timeout:
            time.sleep(0.1)
        
        if not self.is_connected:
            raise ConnectionError("Failed to establish WebSocket connection")

    def queue_prompt(self, prompt):
        """Queue a prompt via HTTP and monitor progress via WebSocket"""
        # Send HTTP request to queue the prompt
        p = {"prompt": prompt, "client_id": self.client_id}
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(
            f"http://{self.server_address}/prompt",
            data=data,
            headers=headers
        )
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))

def main(image_path,output_path):
    # Initialize client
    client_id = "client_123"  # replace with actual client ID
    server_address = "overflow.orangegroup.systems:8188"  # replace with the server address
    client = ComfyUIClient(server_address, client_id, output_path)
    
    try:
        client.connect()
        
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        prompt = json.loads(prompt_text)
        prompt["7"]["inputs"]["text"] = "low quality, blurry, deformed, watermark, text, signature, depth of field, photoreal, realistic, closed_eyes, old, wrinkles"
        prompt["3"]["inputs"]["seed"] = random.randint(0, 2**32 - 1)
        prompt["80"]["inputs"]["image"] = encoded_string

        response = client.queue_prompt(prompt)
        print("Prompt queued:", json.dumps(response, indent=2))

        # Wait for completion or timeout
        if client.completion_event.wait(timeout=300):  # 5 minute timeout
            print("Process completed successfully")
        else:
            print("Timeout waiting for images")

    finally:
        # Clean up WebSocket connection
        if client.ws:
            client.ws.close()
        if client.ws_thread:
            client.ws_thread.join()
    return response