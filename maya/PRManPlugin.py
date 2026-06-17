import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds

try:
    import prman
except ImportError:
    prman = None

kPluginCmdName = "rmanTest"


def is_prman_available():
    return prman is not None


def get_prman_api():
    if not is_prman_available():
        raise RuntimeError("RenderMan Python API is not available.")

    if hasattr(prman, "RiBegin") and hasattr(prman, "RiEnd"):
        return "ri"
    if hasattr(prman, "Begin") and hasattr(prman, "End"):
        return "legacy"

    raise RuntimeError("Unsupported RenderMan Python API version.")


def initialize_prman(name="maya_rman", options=None):
    api = get_prman_api()
    if api == "ri":
        prman.RiBegin(name)
    else:
        prman.Begin(name)

    if options:
        for key, value in options.items():
            set_prman_option(key, value)


def end_prman():
    if not is_prman_available():
        return

    api = get_prman_api()
    if api == "ri":
        prman.RiEnd()
    else:
        prman.End()


def set_prman_option(name, value):
    if not is_prman_available():
        raise RuntimeError("RenderMan Python API is not available.")

    if hasattr(prman, "RiOption"):
        prman.RiOption("render", name, value)
    elif hasattr(prman, "Option"):
        prman.Option("render", name, value)
    else:
        raise RuntimeError("RenderMan Python API does not expose RiOption or Option.")


def create_default_camera():
    camera = cmds.camera()[0]
    cmds.setAttr(camera + ".horizontalFilmAperture", 0.962)
    cmds.setAttr(camera + ".verticalFilmAperture", 0.731)
    cmds.setAttr(camera + ".focalLength", 50)
    cmds.setAttr(camera + ".focusDistance", 3)
    cmds.setAttr(camera + ".shutterAngle", 100)
    return camera


def configure_render_globals():
    cmds.setAttr("defaultRenderGlobals.imageFormat", 8)
    cmds.setAttr("defaultRenderGlobals.animation", 1)
    cmds.setAttr("defaultRenderGlobals.startFrame", 1)
    cmds.setAttr("defaultRenderGlobals.endFrame", 10)
    cmds.setAttr("defaultRenderGlobals.byFrameStep", 1)
    cmds.setAttr("defaultRenderGlobals.outFormatControl", 0)
    cmds.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
    cmds.setAttr("defaultRenderGlobals.extensionPadding", 4)
    cmds.setAttr("defaultRenderGlobals.periodInExt", 1)


class RmanTestCommand(ompx.MPxCommand):
    def __init__(self):
        ompx.MPxCommand.__init__(self)

    def doIt(self, args):
        self.report_environment()

    @staticmethod
    def creator():
        return ompx.asMPxPtr(RmanTestCommand())

    def report_environment(self):
        maya_available = True
        render_man_available = is_prman_available()
        api_version = None
        if render_man_available:
            try:
                api_version = get_prman_api()
            except RuntimeError:
                api_version = "unknown"

        om.MGlobal.displayInfo("Maya API available: %s" % maya_available)
        om.MGlobal.displayInfo("RenderMan API available: %s" % render_man_available)
        if render_man_available:
            om.MGlobal.displayInfo("RenderMan backend: %s" % api_version)
            try:
                initialize_prman("maya_rman_plugin")
                set_prman_option("searchpath:shader", ["./shaders"])
                create_default_camera()
                configure_render_globals()
                om.MGlobal.displayInfo("RenderMan initialization and Maya setup completed.")
            except Exception as exc:
                om.MGlobal.displayError("RenderMan initialization failed: %s" % exc)
            finally:
                end_prman()
        else:
            om.MGlobal.displayWarning(
                "RenderMan Python bindings are not loaded. Load a supported RenderMan Python module to use the plugin."
            )


def initializePlugin(obj):
    plugin = ompx.MFnPlugin(obj, "AlembicRenderMan", "1.0", "Any")
    try:
        plugin.registerCommand(kPluginCmdName, RmanTestCommand.creator)
    except Exception as exc:
        om.MGlobal.displayError("Failed to register command '%s': %s" % (kPluginCmdName, exc))
        raise


def uninitializePlugin(obj):
    plugin = ompx.MFnPlugin(obj)
    try:
        plugin.deregisterCommand(kPluginCmdName)
    except Exception as exc:
        om.MGlobal.displayError("Failed to deregister command '%s': %s" % (kPluginCmdName, exc))
        raise
