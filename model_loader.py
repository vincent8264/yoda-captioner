from transformers import AutoProcessor, BlipForConditionalGeneration
import torch

class ImageCaptionModel:
    def __init__(self):
        self.processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=False)
        self.model = BlipForConditionalGeneration.from_pretrained("vkao8264/blip-yoda-captioning")
        self.model.eval()
        self.default_args = {
            "max_new_tokens": 30,
            "temperature": 0.4,
            "do_sample": True,
            "top_k": 40,
            "top_p": 0.4,                        
        }

    def get_caption(self, image, args):

        inputs = self.processor(image, return_tensors="pt")
        
        generation_args = self.default_args.copy()
        if args["temperature"]:
            generation_args["temperature"] = args["temperature"]
        if args["top_k"]:
            generation_args["top_k"] = args["top_k"]
        if args["top_p"]:
            generation_args["top_p"] = args["top_p"]

        with torch.no_grad():
            output_tokens = self.model.generate(**inputs, **generation_args)
            
        return self.processor.decode(output_tokens[0], skip_special_tokens=True)

class DummyModel:
    def __init__(self):
        print("Dummy model loaded")
        
    def get_caption(self, image, args):
        
        if args["temperature"]:
            temp = args["temperature"]
        if args["top_k"]:
            top_k = args["top_k"]
        if args["top_p"]:
            top_p = args["top_p"]
            
        return f"dummy caption with settings {temp} {top_k} {top_p}"