from datetime import datetime

from tasks.celery_app import celery_app


@celery_app.task(name="tasks.script_task.generate_script")
def generate_script(topic: str):
    return {"topic": topic, "script": f"Starter script for {topic}", "generated_at": datetime.utcnow().isoformat()}
