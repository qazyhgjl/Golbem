"""
Command Validator checking motion constraints and limits.
"""

MAX_DURATION_SECONDS = 3600 # 1 hour max
MAX_REPETITIONS = 500

class CommandValidator:
    def validate(self, parsed_result: dict) -> tuple[bool, str]:
        if parsed_result.get("status") != "success":
            return False, parsed_result.get("message", "خطای تفسیر دستور.")

        actions = parsed_result.get("actions", [])
        if not actions:
            return False, "هیچ حرکتی شناسایی نشد."

        for act in actions:
            dur = act.get("duration")
            reps = act.get("repetitions", 1)

            if dur is not None and (dur <= 0 or dur > MAX_DURATION_SECONDS):
                return False, f"مدت زمان نامعتبر است ({dur} ثانیه). باید بین ۱ تا ۳۶۰۰ ثانیه باشد."

            if reps is not None and (reps <= 0 or reps > MAX_REPETITIONS):
                return False, f"تعداد تکرار نامعتبر است ({reps}). باید بین ۱ تا ۵۰۰ بار باشد."

        return True, ""
