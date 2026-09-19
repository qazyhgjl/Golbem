"""
Command Executor linking parsed Persian NLP commands to Scene, Viewport, and Animation Controller.
"""

from command.parser import CommandParser
from command.validator import CommandValidator

class CommandExecutor:
    def __init__(self, scene, animation_controller):
        self.scene = scene
        self.animation_controller = animation_controller
        self.parser = CommandParser()
        self.validator = CommandValidator()
        self.last_parsed_result = None

    def execute_text_command(self, user_text: str) -> dict:
        parsed = self.parser.parse(user_text)

        if parsed["status"] == "mode_change":
            mode_name = parsed["mode"]
            self.scene.set_display_mode(mode_name)
            return {
                "success": True,
                "message": f"حالت نمایش به '{mode_name}' تغییر یافت.",
                "type": "mode_change",
                "mode": mode_name
            }

        if parsed["status"] == "anatomy_select":
            item_name = parsed["item"]
            self.scene.select_item(item_name)
            return {
                "success": True,
                "message": f"بخش '{item_name}' انتخاب شد.",
                "type": "anatomy_select",
                "item": item_name
            }

        if parsed["status"] == "control":
            ctrl = parsed["control_type"]
            if ctrl == "stop":
                self.animation_controller.stop()
                return {"success": True, "message": "تمام حرکات متوقف شدند.", "type": "stop"}
            elif ctrl == "repeat":
                if self.last_parsed_result and self.last_parsed_result.get("motion_objects"):
                    actions = self.last_parsed_result["motion_objects"]
                    self.animation_controller.set_sequence(actions)
                    return {"success": True, "message": "حرکت قبلی دوباره اجرا شد.", "type": "repeat"}
                else:
                    return {"success": False, "message": "حرکت قبلی برای تکرار یافت نشد.", "type": "repeat"}
            elif ctrl == "clear":
                return {"success": True, "message": "تاریخچه چت پاک شد.", "type": "clear"}

        if parsed["status"] == "error":
            return {"success": False, "message": parsed["message"], "type": "error"}

        is_valid, err_msg = self.validator.validate(parsed)
        if not is_valid:
            return {"success": False, "message": err_msg, "type": "error"}

        self.last_parsed_result = parsed
        motion_objects = parsed["motion_objects"]

        self.animation_controller.set_sequence(motion_objects)

        actions_desc = ", ".join([f"{a.action_type} (duration={a.duration}, reps={a.repetitions})" for a in motion_objects])
        return {
            "success": True,
            "message": f"دستور حرکتی اجرا شد: {actions_desc}",
            "type": "motion",
            "actions": parsed["actions"]
        }
