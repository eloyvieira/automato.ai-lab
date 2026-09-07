from openai import OpenAI
from core.config import get_settings

class OpenAIFineTuning:
    def __init__(self):
        self.client = OpenAI(api_key=get_settings().openai_api_key)

    def upload_training_file(self, jsonl_path: str) -> str:
        with open(jsonl_path, 'rb') as f:
            uploaded = self.client.files.create(file=f, purpose='fine-tune')
        return uploaded.id

    def create_job(self, training_file_id: str, base_model: str, suffix: str | None = None):
        kwargs = {'training_file': training_file_id, 'model': base_model}
        if suffix: kwargs['suffix'] = suffix
        return self.client.fine_tuning.jobs.create(**kwargs)

    def get_job(self, job_id: str):
        return self.client.fine_tuning.jobs.retrieve(job_id)

    def list_jobs(self, limit: int = 20):
        return self.client.fine_tuning.jobs.list(limit=limit)
