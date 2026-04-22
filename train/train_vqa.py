import json
import os
import torch # type: ignore
from PIL import Image
from transformers import ViltProcessor, ViltForQuestionAnswering # type: ignore
from torch.utils.data import Dataset, DataLoader # type: ignore
from tqdm import tqdm

# =========================
# PATHS
# =========================
DATA_PATH = r"E:\visual_question_answering\data\my_vqa.json"
IMAGE_DIR = r"E:\visual_question_answering\data\image"
SAVE_PATH = r"E:\visual_question_answering\model\trained_vqa"

DEVICE = "cpu"

# =========================
# DATASET (FLATTENED)
# =========================
class VQADataset(Dataset):
    def __init__(self, json_path, image_dir):
        with open(json_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        self.image_dir = image_dir
        self.samples = []

        # 🔥 Flatten questions
        for item in raw_data:
            image_name = item["image"]

            all_qas = item.get("questions", []) + item.get("extra_questions", [])

            for qa in all_qas:
                self.samples.append({
                    "image": image_name,
                    "question": qa["question"],
                    "answer": qa["answer"]
                })

        # Label mapping
        answers = sorted(set(s["answer"] for s in self.samples))
        self.label2id = {a: i for i, a in enumerate(answers)}
        self.id2label = {i: a for a, i in self.label2id.items()}

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]

        image = Image.open(
            os.path.join(self.image_dir, item["image"])
        ).convert("RGB")

        return {
            "image": image,
            "question": item["question"],
            "label": self.label2id[item["answer"]]
        }

# =========================
# COLLATE FUNCTION (FIXED)
# =========================
def collate_fn(batch):
    images = [item["image"] for item in batch]
    questions = [item["question"] for item in batch]
    labels = torch.tensor([item["label"] for item in batch], dtype=torch.long)

    encoding = processor(
        images=images,
        text=questions,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    encoding["labels"] = labels
    return encoding

# =========================
# TRAINING
# =========================
def main():
    global processor

    print("🔹 Loading processor")
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-mlm")

    print("🔹 Loading dataset")
    dataset = VQADataset(DATA_PATH, IMAGE_DIR)
    NUM_LABELS = len(dataset.label2id)

    dataloader = DataLoader(
        dataset,
        batch_size=4,
        shuffle=True,
        collate_fn=collate_fn
    )

    print("🔹 Loading model")
    model = ViltForQuestionAnswering.from_pretrained(
        "dandelin/vilt-b32-mlm",
        num_labels=NUM_LABELS,
        id2label=dataset.id2label,
        label2id=dataset.label2id
    )

    model.to(DEVICE)
    model.train()

    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

    EPOCHS = 10  # 🔥 Increase epochs

    for epoch in range(EPOCHS):
        loop = tqdm(dataloader, desc=f"Epoch {epoch+1}/{EPOCHS}")

        for batch in loop:
            batch = {k: v.to(DEVICE) for k, v in batch.items()}

            outputs = model(**batch)
            loss = outputs.loss

            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

            loop.set_postfix(loss=f"{loss.item():.4f}")

    print("🔹 Saving model")
    os.makedirs(SAVE_PATH, exist_ok=True)
    model.save_pretrained(SAVE_PATH)
    processor.save_pretrained(SAVE_PATH)

    print("✅ TRAINING COMPLETE")
    print("📁 Model saved to:", SAVE_PATH)

# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()
