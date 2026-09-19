"""
Persian NLP Command Parser extracting action types, durations, repetitions, and sequence ordering.
"""

import re
from command.normalizer import normalize_text, PERSIAN_WORD_NUMBERS
from command.vocabulary import ACTION_VOCABULARY, CONTROL_VOCABULARY
from animation.motion_sequence import MotionAction

class CommandParser:
    def parse(self, user_input: str) -> dict:
        """Parses user Persian string into standard action structure."""
        normalized = normalize_text(user_input)

        if not normalized:
            return {"status": "error", "message": "متن ورودی خالی است.", "actions": []}

        # Check control commands (stop, repeat, clear)
        for ctrl_type, keywords in CONTROL_VOCABULARY.items():
            for kw in keywords:
                if kw in normalized:
                    return {"status": "control", "control_type": ctrl_type, "actions": []}

        # Split compound commands separated by 'بعد', 'سپس', ',', 'و بعد'
        sub_commands = re.split(r'بعد\s*از\s*آن|و\s*بعد|سپس|بعد|،|,', normalized)

        actions = []
        for sub_cmd in sub_commands:
            sub_cmd = sub_cmd.strip()
            if not sub_cmd:
                continue

            action = self._parse_single_command(sub_cmd)
            if action:
                actions.append(action)

        if not actions:
            return {
                "status": "error",
                "message": f"دستور شناسایی نشد: '{user_input}'. لطفاً دستور را به زبان فارسی واضح وارد کنید.",
                "actions": []
            }

        return {
            "status": "success",
            "message": "دستور با موفقیت تفسیر شد.",
            "actions": [
                {"type": a.action_type, "duration": a.duration, "repetitions": a.repetitions}
                for a in actions
            ],
            "motion_objects": actions
        }

    def _parse_single_command(self, text: str) -> MotionAction:
        action_type = self._detect_action_type(text)
        if not action_type:
            return None

        duration = self._extract_duration(text)
        repetitions = self._extract_repetitions(text)

        return MotionAction(action_type=action_type, duration=duration, repetitions=repetitions)

    def _detect_action_type(self, text: str) -> str:
        for act_key, keywords in ACTION_VOCABULARY.items():
            for kw in keywords:
                if kw in text:
                    return act_key
        return None

    def _extract_duration(self, text: str) -> float:
        """Extracts time in seconds from text like '۳۰ ثانیه' or '20 ثانیه'."""
        match = re.search(r'(\d+)\s*(ثانیه|دقیقه)', text)
        if match:
            num = int(match.group(1))
            unit = match.group(2)
            if unit == 'دقیقه':
                num *= 60
            return float(num)

        # Check for word numbers
        for word, val in PERSIAN_WORD_NUMBERS.items():
            if f"{word} ثانیه" in text:
                return float(val)
            if f"{word} دقیقه" in text:
                return float(val * 60)

        return None

    def _extract_repetitions(self, text: str) -> int:
        """Extracts repetitions from text like '۱۰ تا' or '۵ بار'."""
        match = re.search(r'(\d+)\s*(بار|تا|مرتبه|تکرار)', text)
        if match:
            return int(match.group(1))

        for word, val in PERSIAN_WORD_NUMBERS.items():
            if f"{word} بار" in text or f"{word} تا" in text or f"{word} مرتبه" in text:
                return val

        return 1
