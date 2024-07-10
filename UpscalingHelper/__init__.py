import unrealsdk # type: ignore

from typing import Any, Dict, List, Tuple
from Mods import ModMenu # type: ignore


DEBUG: bool = False


def log(mod: ModMenu.SDKMod, *args: Any) -> None:
    unrealsdk.Log(f"[{mod.Name}]", *args)


def get_pc() -> unrealsdk.UObject:
    return unrealsdk.GetEngine().GamePlayers[0].Actor


def font_color(text: str, color: str) -> str:
    return f"<font color='{color}'>{text}</font>"


class Color:
    SKILL: str  = "#ffdead"
    HEALTH: str = "#e96464"


class Resolution:
    DATA: Dict[str, Tuple[int, int]] = {
        "1920 x 1080": (1920, 1080), # 16:9
        "1920 x 1200": (1920, 1200), # 16:10
        "2560 x 1080": (2560, 1080), # 21:9
        "2560 x 1440": (2560, 1440), # 16:9
        "2560 x 1600": (2560, 1600), # 16:10
        "3440 x 1440": (3440, 1440), # 21:9
        "3840 x 1600": (3840, 1600), # 21:9
        "3840 x 2160": (3840, 2160), # 16:9
        "3840 x 2400": (3840, 2400), # 16:10
        "5120 x 2160": (5120, 2160), # 21:9
        "5120 x 2880": (5120, 2880), # 16:9
        "6144 x 3456": (6144, 3456), # 16:9
        "7680 x 4320": (7680, 4320), # 16:9
    }

    CHOICES: Tuple[str, ...] = tuple(DATA.keys())
    DEFAULT: str = CHOICES[0]


class UpscalingHelper(ModMenu.SDKMod):
    Name = "Upscaling Helper"
    Author = "Neumatic"
    Version = "1.0"
    Description = (
        f"Change the in-game {font_color('resolution', Color.SKILL)} to a lower or non-supported"
        f" {font_color('resolution', Color.SKILL)} for use with an {font_color('upscaler', Color.SKILL)}."
    )

    Types = ModMenu.ModTypes.Utility
    SaveEnabledState = ModMenu.EnabledSaveType.LoadWithSettings

    def __init__(self) -> None:
        self.update_resolution = False
        self.output_resolution_option = ModMenu.Options.Spinner(
            Caption = "Output Resolution",
            Description = f"The {font_color('resolution', Color.SKILL)} to upscale to.",
            StartingValue = Resolution.DEFAULT,
            Choices = Resolution.CHOICES,
        )
        self.resolution_scale_option = ModMenu.Options.Slider(
            Caption = "Resolution Scale",
            Description = (
                f"The scaling size of the output {font_color('resolution', Color.SKILL)}.\n"
                f"({font_color('Output Resolution', Color.SKILL)} {font_color('*', Color.HEALTH)}"
                f" {font_color('Resolution Scale', Color.SKILL)}) {font_color('/', Color.HEALTH)} 100"
            ),
            StartingValue = 100,
            MinValue = 50,
            MaxValue = 100,
            Increment = 1,
        )
        self.apply_scaling_button = ModMenu.Options.Spinner(
            Caption = "APPLY",
            Description = f"Apply the selected {font_color('resolution', Color.SKILL)} scale.",
            StartingValue = "Yes",
            Choices = ("Yes", "Yes"),
        )
        self.Options: List[ModMenu.Options.Base] = [
            self.output_resolution_option,
            self.resolution_scale_option,
            self.apply_scaling_button,
        ]

    def ModOptionChanged(self, option: ModMenu.Options.Base, new_value: Any) -> None:
        if option == self.apply_scaling_button:
            if not self.update_resolution:
                return
            res_x, res_y = Resolution.DATA[self.output_resolution_option.CurrentValue]
            res_scale: int = self.resolution_scale_option.CurrentValue
            new_res_x = int((res_x * res_scale) / 100)
            new_res_y = int((res_y * res_scale) / 100)
            if not DEBUG:
                pc = get_pc()
                pc.ConsoleCommand(f"SetRes {new_res_x}x{new_res_y}")
                pc.ConsoleCommand(f"SCALE SET ResX {new_res_x}")
                pc.ConsoleCommand(f"SCALE SET ResY {new_res_y}")
            else:
                log(
                    self,
                    f"Output Resolution: {res_x} x {res_y},",
                    f"Resolution Scale: {res_scale},",
                    f"Input Resolution: {new_res_x} x {new_res_y}",
                )
            self.update_resolution = False
        else:
            self.update_resolution = True


mod_instance = UpscalingHelper()

if __name__ == "__main__":
    for mod in ModMenu.Mods:
        if mod.Name != mod_instance.Name:
            continue
        if mod.IsEnabled:
            mod.Disable()
        ModMenu.Mods.remove(mod)
        mod_instance.__class__.__module__ = mod.__class__.__module__
        break

ModMenu.RegisterMod(mod_instance)
