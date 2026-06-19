"""Maya RenderMan Integration Plugin for Alembic.

This module provides a Python-based Maya plugin for RenderMan integration,
including environment detection, initialization, and configuration helpers.
"""

import logging
import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx
import maya.cmds as cmds

try:
    import prman
except ImportError:
    prman = None

kPluginCmdName = "rmanTest"
LOGGER = logging.getLogger(__name__)


def is_prman_available():
    """Check if RenderMan Python API is available.

    Returns:
        bool: True if RenderMan module is loaded, False otherwise.
    """
    return prman is not None


def get_prman_api():
    """Detect and return the RenderMan API version.

    Returns:
        str: "ri" for modern API, "legacy" for older API.

    Raises:
        RuntimeError: If RenderMan is not available or API version is unsupported.
    """
    if not is_prman_available():
        raise RuntimeError("RenderMan Python API is not available.")

    if hasattr(prman, "RiBegin") and hasattr(prman, "RiEnd"):
        return "ri"
    if hasattr(prman, "Begin") and hasattr(prman, "End"):
        return "legacy"

    raise RuntimeError("Unsupported RenderMan Python API version.")


def initialize_prman(name="maya_rman", options=None):
    """Initialize RenderMan with optional configuration.

    Args:
        name (str): RenderMan context name. Defaults to "maya_rman".
        options (dict): Optional configuration key-value pairs.

    Raises:
        RuntimeError: If RenderMan API detection fails.
    """
    api = get_prman_api()
    if api == "ri":
        prman.RiBegin(name)
    else:
        prman.Begin(name)

    if options:
        for key, value in options.items():
            set_prman_option(key, value)

    LOGGER.info("RenderMan initialized with context: %s", name)


def end_prman():
    if not is_prman_available():
        return

    api = get_prman_api()
    if api == "ri":
        prman.RiEnd()
    else:
        prman.End()


def set_prman_option(name, value):
    """Set a RenderMan render option.

    Args:
        name (str): Option name.
        value: Option value (can be string, float, list, etc.).

    Raises:
        RuntimeError: If RenderMan is not available.
    """
    if not is_prman_available():
        raise RuntimeError("RenderMan Python API is not available.")

    if hasattr(prman, "RiOption"):
        prman.RiOption("render", name, value)
    elif hasattr(prman, "Option"):
        prman.Option("render", name, value)
    else:
        raise RuntimeError("RenderMan Python API does not expose RiOption or Option.")

    LOGGER.debug("RenderMan option set: %s = %s", name, value)


def create_default_camera():
    """Create and configure a default Maya camera for RenderMan.

    Returns:
        str: Name of the created camera.
    """
    camera = cmds.camera()[0]
    cmds.setAttr(camera + ".horizontalFilmAperture", 0.962)
    cmds.setAttr(camera + ".verticalFilmAperture", 0.731)
    cmds.setAttr(camera + ".focalLength", 50)
    cmds.setAttr(camera + ".focusDistance", 3)
    cmds.setAttr(camera + ".shutterAngle", 100)
    LOGGER.info("Default camera created: %s", camera)
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
    """Maya command for testing RenderMan integration."""

    def __init__(self):
        ompx.MPxCommand.__init__(self)

    def doIt(self, args):
        """Execute the RenderMan test command.

        Args:
            args (MArgList): Command arguments (not currently used).
        """
        self.report_environment()

    @staticmethod
    def creator():
        return ompx.asMPxPtr(RmanTestCommand())

    def report_environment(self):
        """Report environment status and initialize RenderMan if available."""
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
                # Pass options as dict with proper string values
                initialize_prman("maya_rman_plugin", {"searchpath:shader": "./shaders"})
                create_default_camera()
                configure_render_globals()
                om.MGlobal.displayInfo("RenderMan initialization and Maya setup completed.")
                LOGGER.info("RenderMan plugin initialized successfully.")
            except Exception as exc:
                om.MGlobal.displayError("RenderMan initialization failed: %s" % exc)
                LOGGER.error("RenderMan initialization failed", exc_info=True)
            finally:
                end_prman()
        else:
            om.MGlobal.displayWarning(
                "RenderMan Python bindings are not loaded. Load a supported RenderMan Python module to use the plugin."
            )
            LOGGER.warning("RenderMan Python bindings not available.")


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
