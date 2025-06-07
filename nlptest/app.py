from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import datasets
import torch
# load model and processor
processor = WhisperProcessor.from_pretrained("mbazaNLP/Whisper-Small-Kinyarwanda")
model = WhisperForConditionalGeneration.from_pretrained("mbazaNLP/Whisper-Small-Kinyarwanda")
ds = load_dataset("common_voice", "rw", split="test", streaming=True)
ds = ds.cast_column("audio", datasets.Audio(sampling_rate=16_000))
input_speech = next(iter(ds))["audio"]["array"]
model.config.forced_decoder_ids = processor.get_decoder_prompt_ids(language = "sw", task = "transcribe")
input_features = processor(input_speech, return_tensors="pt").input_features 
predicted_ids = model.generate(input_features)
transcription = processor.batch_decode(predicted_ids)
transcription = processor.batch_decode(predicted_ids, skip_special_tokens = True)
