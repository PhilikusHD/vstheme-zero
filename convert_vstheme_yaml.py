import xml.etree.ElementTree as ET
from typing import Dict, Any
import yaml
import os

def argb_to_rgb(color: str) -> str:
    """Convert ARGB integer to hexadecimal color string."""
    if not color or len(color) != 8:
        return None
    return "#" + color[2:].lower()

def parse_vstheme(file_path: str) -> Dict[str, Any]:
    """Parse a .vstheme XML file and extract theme information."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    theme_info = {
        "Name": "",
        "Identity": "",
        "Version": "1.0.0.2026",
        "GUID": "",
        "BaseGUID": "",
        "Author": "PhilikusHD",
        "Description": "A Visual Studio 2026 theme.",
        "Tags": "Dark",
        "Icon": "vszero-_mini.png",
        "Sections": {}
    }
    
    for theme in root.findall("Theme"):
        theme_info["Name"] = theme.get("Name") + " 2026"
        theme_info["Identity"] = theme.get("Name").strip().replace(" ", "_") + "_2026"
        theme_info["GUID"] = theme.get("GUID").strip()[1:-1]
        theme_info["BaseGUID"] = theme.get("BaseGUID").strip()[1:-1]
        for category in theme.findall("Category"):
            cat_name: str = category.get("Name")
            cat_guid: str = category.get("GUID").strip()[1:-1]
 
            cat_entry = {"GUID": cat_guid}

            for color in category.findall("Color"):
                color_name: str = color.get("Name")
                bg, fg = None, None

                bg_elem = color.find("Background")
                fg_elem = color.find("Foreground")

                if bg_elem is not None and bg_elem.get("Source"):
                    bg = argb_to_rgb(bg_elem.get("Source"))
                if fg_elem is not None and fg_elem.get("Source"):
                    fg = argb_to_rgb(fg_elem.get("Source"))
                
                cat_entry[color_name] = [bg, fg]

            theme_info["Sections"][cat_name] = cat_entry

    extra_sections = {
        "Shell": {
            "GUID": "73708ded-2d56-4aad-b8eb-73b20d3f4bff",
            "AccentFillDefault": ["#39404f", None],
            "AccentFillSecondary": ["#39404fe5", None],
            "AccentFillTertiary": ["#39404fcc", None],
            "SolidBackgroundFillTertiary": ["#282c34", None],
            "SolidBackgroundFillQuaternary": ["#2e323a", None],
            "TextFillSecondary": ["#ffffffcc", None],
            "SystemFillAttention": ["#588295", None],
            "SystemFillSolidAttentionBackground": ["#2e323a", None],
            "SystemFillSolidNeutralBackground": ["#2e323a", None]
        },
        "ShellInternal": {
            "GUID": "5af241b7-5627-4d12-bfb1-2b67d11127d7",
            "EnvironmentBackground": ["#101216", None],
            "EnvironmentBorder": ["#39404f", None],
            "EnvironmentBorderInactive": ["#39404f", None],
            "EnvironmentIndicator": ["#ffffff60", None],
            "EnvironmentLogo": ["#80119f", None],
            "EnvironmentLayeredBackground": ["#0000004d", None],
            "StatusBarBackgroundFillSolutionLoading": ["#0000004d", None]
        }
    }

    theme_info["Sections"].update(extra_sections)
    return theme_info

def flow_list_representer(dumper, seq):
    return dumper.represent_sequence("tag:yaml.org,2002:seq", seq, flow_style=True)

def convert_to_yaml(data, output_path):
    yaml.add_representer(list, flow_list_representer)

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(
            data,
            f,
            sort_keys=False,
            allow_unicode=True
        )

if __name__ == "__main__":
    for os_file in os.listdir("src"):
        if os_file.endswith(".vstheme"):
            vstheme_data = parse_vstheme(os.path.join("src", os_file))
            convert_to_yaml(vstheme_data, os.path.join("themes", f"{vstheme_data['Identity']}.yaml"))