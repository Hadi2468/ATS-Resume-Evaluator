from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    format="{time} | {level} | {message}"
)

logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="10 days"
)

logger.info("🚀 Application Started")

logger.info("📄 Resume uploaded")

logger.info("📋 Job Description uploaded")

logger.info("⭕ Running Zero-Shot Evaluation")

logger.info("👉 Running One-Shot Evaluation")

logger.info("👊 Running Few-Shot Evaluation")

logger.info("🧠 Running Chain-of-Thought Evaluation")

logger.success("✅ Evaluation completed successfully")

logger.error("❌ OpenAI API error")

logger.warning("⚠️ Missing resume content")