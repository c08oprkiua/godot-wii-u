import os
import platform
import sys

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from SCons import Environment

#Godot for Wii U
#Based heavily on the Android port, because that's a prime example of linking external libraries,
#compiling for an arch that is not the host's arch, etc. Also based on SeleDream's port of Godot 4 to 3DS.

def is_active():
    return False #Needs to be true for the platform to be usable, false for convenience

def get_name():
    return "Wii U"

def can_build():
    if not(os.getenv("DEVKITPRO") and os.getenv("DEVKITPPC")):
        print("Either DevKitPro or DevKitPPC were not found, Wii U disabled.")
        return False
    return True


def get_opts():
    from SCons.Variables import BoolVariable, EnumVariable

    return [
        BoolVariable("touch", "Enable touch events", True), #probably the only option here that should stay lol
    ]

def get_doc_classes():
    return [
        "EditorExportPlatformWiiU",
    ]

def get_doc_path():
    return "doc_classes"

def get_flags():
    return [
        ("arch", "ppc32"),
    ]

def configure(env: "Environment"):
    # Validate arch. These are supported COMPILE arches, not supported EXPORT arches.
    supported_arches = ["x86_32", "x86_64", "arm32", "arm64"] #Does devkitppc even work on ARM...???
    if env["arch"] not in supported_arches:
        print(
            'Unsupported CPU architecture "%s" for Wii U. Supported architectures are: %s.'
            % (env["arch"], ", ".join(supported_arches))
        )
        sys.exit()

    ## Build type

    env["bits"] = "32"

    ## Compiler configuration
    devkitpath = env["DEVKITPRO"]
    wutpath = devkitpath + "/wut" 
    wuhbpath = devkitpath + "tools/bin/wuhbtool" #I figure this will be needed to export to wuhb?
    #Link flags
    
    env.Prepend(CPPPATH=["#platform/wiiu"])
    env.Append(LIBS=["wut"])


    
