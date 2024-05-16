import csv
import requests
from PIL import Image
import requests
from transformers import AutoProcessor, LlavaForConditionalGeneration
import os

# Model and processor initialization
model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf").to("cuda")
processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")


# Correct way to open one file for reading and another for writing
with open('output.csv', mode='w', encoding='utf-8', newline='') as outfile:
        
    # Create a CSV writer object to write to the output file
    writer = csv.writer(outfile)

    # Example: Writing headers from the input file to the output file
    writer.writerow(['image_filename', 'composition'])

    for image_filename in os.listdir("./images"):

        image_path = os.path.join("./images", image_filename)

        try:
            image = Image.open(image_path)

            prompts = [
                "<image>\nUSER: Give a short detailed description of this paintings composition. In this description include answers to each of the following questions: How are all the elements, objects, parts positioned in the whole picture and relative to eachother; Give a description of each of the elements; Is there unity between the elements, colors or overall arrangement; Is there balance between the elements and colors, or in how the parts are laid out in the space; Describe the different colors that are used and how they are used; Is there movement visualized in the painting; Is there rhythm in the visualization of elements, is this rhythm regular, random, flowing, alternating or progressive; Describe the focus point of the painting and how this focus is obtained; Did the artist use contrast in this work, describe uses of light and dark intensities, oposite color uses, contrasting elements; Is there a pattern within the elements, think of circular, triangular or s curve arrangements; Is there use of different proportions and for what purpose? Your answer should be a well structured short paragraph (about 150 words), without repeating concepts. Do not describe what you do not see in the painting.\nASSISTANT:",
            ]
            answers = []

            for prompt in prompts:
                inputs = processor(text=prompt, images=image, return_tensors="pt").to("cuda")

                # Generate
                generate_ids = model.generate(**inputs, max_length=600)
                result = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

                result_split = result.split('ASSISTANT: ')
                if len(result_split) > 1:
                    answers.append(result_split[1])
                else:
                    answers.append("")

                writer.writerow([image_filename] + answers)

        except Exception as e:
            print(f"Error processing {image_filename}: {str(e)}")




  
