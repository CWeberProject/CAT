import sys

sys.path.append('OmniParser')

from utils import get_som_labeled_img, check_ocr_box, get_caption_model_processor, get_yolo_model
import torch
from ultralytics import YOLO
from PIL import Image
import base64
import matplotlib.pyplot as plt
import io
import os
import time

from anthropic import Anthropic
import json



def initialize_models(device='cuda'):
    """Initialize the YOLO and caption models."""
    # Initialize YOLO model
    som_model = get_yolo_model(model_path='weights/icon_detect/best.pt')
    som_model.to(device)
    print('model to {}'.format(device))

    # Initialize caption model (choose one of the two options)
    # Option 1: BLIP2
    # caption_model_processor = get_caption_model_processor(
    #     model_name="blip2",
    #     model_name_or_path="weights/icon_caption_blip2",
    #     device=device
    # )

    # Option 2: Florence2
    caption_model_processor = get_caption_model_processor(
        model_name="florence2",
        model_name_or_path="weights/icon_caption_florence",
        device=device
    )

    return som_model, caption_model_processor

def process_image(image_path, som_model, caption_model_processor, box_threshold=0.03):
    """Process an image and return labeled results."""
    # Configuration for drawing bounding boxes
    draw_bbox_config = {
        'text_scale': 0.8,
        'text_thickness': 2,
        'text_padding': 3,
        'thickness': 3,
    }

    # Open and convert image
    image = Image.open(image_path)
    image_rgb = image.convert('RGB')

    # Perform OCR
    ocr_bbox_rslt, is_goal_filtered = check_ocr_box(
        image_path,
        display_img=False,
        output_bb_format='xyxy',
        goal_filtering=None,
        easyocr_args={'paragraph': False, 'text_threshold': 0.9},
        use_paddleocr=True
    )
    text, ocr_bbox = ocr_bbox_rslt

    # Get labeled image and results
    dino_labled_img, label_coordinates, parsed_content_list = get_som_labeled_img(
        image_path,
        som_model,
        BOX_TRESHOLD=box_threshold,
        output_coord_in_ratio=False,
        ocr_bbox=ocr_bbox,
        draw_bbox_config=draw_bbox_config,
        caption_model_processor=caption_model_processor,
        ocr_text=text,
        use_local_semantics=True,
        iou_threshold=0.1
    )

    return dino_labled_img, label_coordinates, parsed_content_list

class TaskAnalyzer:

    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)

    def format_screen_elements(self, elements):
        """Convert the list of elements into a structured string format."""
        return "\n".join(elements)

    def create_system_prompt(self):
        return """You are a task analyzer for a computer automation system. When given a task and a list of screen elements, you should:
                    1. Analyze the available screen elements
                    2. Return one instruction in this exact format for the specific step to execute:
                    {
                        "ACTION": "[click/type/wait]",
                        "ELEMENT": "\"Text Box/Icon Box ID X: [exact element text]\"",
                        "DETAILS": "[text to type or additional info if needed]"
                        }

                    Rules:
                    - You have the obligation to start with the instruction before saying anything else
                    - Only reference elements that exactly match the provided list
                    - Always include the full element ID and text in your reference
                    - Be specific about whether to click or type
                    - If typing is needed, specify the exact text to type
                    - Keep responses focused only on achievable actions with the given elements"""

    def analyze_task(self, task, screen_elements):
        screen_content = self.format_screen_elements(screen_elements)

        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"""Task to complete: {task}

Available screen elements:
{screen_content}

Provide step-by-step instructions using only the available elements. Format each step as specified in your system prompt."""
                }
            ],
            system=self.create_system_prompt()
        )

        return message.content
    

# Initialize device and models
device = 'cuda'

som_model, caption_model_processor = initialize_models(device)
analyzer = TaskAnalyzer(os.getenv('ANTHROPIC_API_KEY'))

# Wait for the task to be available
filepath = 'task.json'
while not os.path.isfile(filepath):
    print("Waiting for task.json to be available...")
    time.sleep(1)  # Wait for 5 seconds before checking again

# Once the file is available, open and read it
with open(filepath, 'r') as file:
    data = json.load(file)
task = data["task"]

i = 0
while True:
    next_image = 'screenshot_'+str(i)+'.png'
    if next_image in os.listdir('imgs'):
        time.sleep(3)
        image_path = 'imgs/'+next_image

        # Process the image
        dino_labled_img, label_coordinates, screen_elements = process_image(image_path,som_model,caption_model_processor)
        Image.open(io.BytesIO(base64.b64decode(dino_labled_img))).save('results/labled_'+next_image)
    
        # Task 
        try:
            result = analyzer.analyze_task(task, screen_elements)
            print(result)

            # Extract the JSON part from the text
            json_text = result[0].text.split('\n')[0:4]
            json_result = json.loads('\n'.join(json_text) + '\n}')
            json_result['COORDINATES'] = label_coordinates[json_result['ELEMENT'].split()[3][:-1]].tolist()
            
            # Define the file path where you want to save the result
            file_path = "results/result_"+str(i)+".json"
            # Write the result to the JSON file
            with open(file_path, 'w') as json_file:
                json.dump(json_result, json_file, indent=4)

            print(f"Result has been saved to {file_path}")
            task = task + 'knowing that in step '+str(i)+' you did this' + str(result)
            
        except Exception as e:
            print(f"Error: {e}")

        i+=1
    
