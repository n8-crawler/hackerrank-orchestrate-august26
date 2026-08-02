from transformers import AutoModelForMultimodalLM, AutoModelForSpeechSeq2Seq, AutoProcessor, Mistral3ForConditionalGeneration,MistralCommonBackend
import torch
import librosa
from utils.image_encode import img_to_base64

class LLMservice:
    def __init__(self):
        self.load_reasoning_model()
        self.load_vision_model()
        self.load_audio_model()

    def load_reasoning_model(self):
        model_name = "mistralai/Ministral-3-8B-Reasoning-2512"
        self.reason_device = torch.device("mps")
        self.reasoning_tokenizer = MistralCommonBackend.from_pretrained(model_name)
        self.reasoning_model = Mistral3ForConditionalGeneration.from_pretrained(model_name, torch_dtype=torch.bfloat16).to(self.reason_device)
        
    def load_vision_model(self):
        model_name="Qwen/Qwen3-VL-2B-Instruct"
        self.vision_device = torch.device("mps")
        self.vision_processor = AutoProcessor.from_pretrained(model_name)
        self.vision_model = AutoModelForMultimodalLM.from_pretrained(model_name, dtype=torch.bfloat16).to(self.vision_device)

    def load_audio_model(self):
        model_name="openai/whisper-large-v3-turbo"
        self.audio_device = torch.device("cpu")
        self.audio_processor = AutoProcessor.from_pretrained(model_name)
        self.audio_model = AutoModelForSpeechSeq2Seq.from_pretrained(model_name, dtype=torch.bfloat16).to(self.audio_device)

    def reason(self,prompt:str)->str:
        messages = [{
            "role": "user",
            "content": prompt
        }]
        inputs = self.reasoning_tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(self.reason_device)
        outputs = self.reasoning_model.generate(**inputs,max_new_tokens=1024,do_sample=False,temperature=0.0)
        prompt_length = inputs["input_ids"].shape[1]
        generated_ids = outputs[:, prompt_length:]

        response = self.reasoning_tokenizer.decode(generated_ids[0],skip_special_tokens=True,)
        print('>>>>>reason>>>>>>',response.strip())
        return response.strip()
        
    def analyse_image(self,image_path:str)->str:
        local_prompt = """
            Analyze this WhatsApp image.
            Extract every important detail.
            Include:

            - Text visible
            - Dates
            - Times
            - People
            - Objects
            - Event names
            - Deadlines
            - Payment requests
            - QR codes
            - Phone numbers
            - URLs
            - Severity/Urgency

            Return plain English.
            Do not summarize.
            Be exhaustive.
            """

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image":img_to_base64(img_path=image_path)},
                    {"type": "text", "text": local_prompt}
                ]
            },
        ]

        inputs = self.vision_processor.apply_chat_template(
            messages,
            add_generation_prompt=False,
            tokenize=True,
            return_dict = True,
            return_tensors="pt",
        )
        inputs = {k: v.to(self.vision_device)for k, v in inputs.items()} 
        # moving tensor values to  gpu instead of processing in cpu 

        generate_ids = self.model.generate(**inputs,max_new_tokens=512)
        # below gets the input_ids of token generated since genrate_id is prompt_token + Ai response_token
        prompt_length = inputs["input_ids"].shape[1]
        generated_ids = generate_ids[:, prompt_length:]
        answer = self.processor.batch_decode(generated_ids, skip_special_tokens=True,clean_up_tokenization_spaces=False,)[0]
        print('>>>>>vision>>>>>>',answer.strip())
        return answer

    def voice_transcript(self,audio_path:str)->str:
        audio, sampling_rate = librosa.load(audio_path,sr=16000)
        inputs = self.audio_processor(audio,sampling_rate=sampling_rate,return_tensors="pt",language="en",task="transcribe")
        inputs = {
        k: v.to(self.audio_device)
        for k, v in inputs.items()
        }
        generated_ids = self.audio_model.generate(
        inputs["input_features"],
        max_new_tokens=256
    )
        transcript = self.audio_processor.batch_decode(generated_ids,skip_special_tokens=True)[0]
        print(type(transcript))
        print('>>>>>>audio>>>>>>>',transcript)
        return transcript.strip()