"""Alembic Maya-RenderMan integration test and utility module.

This module provides helper functions for testing Maya and RenderMan integration,
including scene creation, camera setup, and RenderMan initialization.

Usage:
    python consoler_tracktion.py
"""

import logging
import os

try:
    import maya
    import maya.cmds as MayaCmds
    import maya.OpenMaya as OpenMaya
    import maya.standalone
except ImportError:
    MayaCmds = None
    OpenMaya = None
    maya = None

try:
    import prman
    from prman import rmanGettr as prman_rmanGettr
except ImportError:
    prman = None
    prman_rmanGettr = None

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')


def ensure_maya_available():
    """Verify that Maya Python API is available.

    Raises:
        RuntimeError: If Maya API is not loaded.
    """
    if MayaCmds is None:
        raise RuntimeError("Maya Python API is not available in this environment.")


def createCamera():
    """Create a default test camera with RenderMan-friendly settings.

    Returns:
        tuple: Camera transform and shape node names.
    """
    ensure_maya_available()
    name = MayaCmds.camera()
    MayaCmds.setAttr(name[1] + '.horizontalFilmAperture', 0.962)
    MayaCmds.setAttr(name[1] + '.verticalFilmAperture', 0.731)
    MayaCmds.setAttr(name[1] + '.focalLength', 50)
    MayaCmds.setAttr(name[1] + '.focusDistance', 3)
    MayaCmds.setAttr(name[1] + '.shutterAngle', 100)
    LOGGER.info("Camera created: %s", name[0])
    return name


def createMesh():
    ensure_maya_available()
    return MayaCmds.polyCube()


def createLight():
    ensure_maya_available()
    return MayaCmds.directionalLight()


def createLocator():
    ensure_maya_available()
    return MayaCmds.spaceLocator()


def createNurbsCurve():
    ensure_maya_available()
    return MayaCmds.curve(d=1, p=[(-1, 0, 0), (0, 0, 1), (1, 0, 0)])


def createNurbsSurface():
    ensure_maya_available()
    return MayaCmds.nurbsPlane(d=3, p=(0, 0, 0), ax=(0, 1, 0), w=1, lr=1, n='nurbsPlane1')


def createSubdiv():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.setAttr(name[0] + '.subdivisionsWidth', 2)
    MayaCmds.setAttr(name[0] + '.subdivisionsHeight', 2)
    return name


def createParticle():
    ensure_maya_available()
    return MayaCmds.particle()


def createHair():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.select(name[0])
    MayaCmds.CreateHair()
    return name


def createFluid():
    ensure_maya_available()
    return MayaCmds.fluidEmitter()


def createRigidBody():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.rigidBody(name[0], active=True)
    return name


def createSoftBody():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.soft(name[0])
    return name


def createConstraint():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.pointConstraint(name[0], name[0])
    return name


def createDeformer():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.nonLinear(name[0], type='bend')
    return name


def createExpression():
    ensure_maya_available()
    name = MayaCmds.polyCube()
    MayaCmds.expression(s=name[0] + '.translateX = time * 1')
    return name


def createShader():
    ensure_maya_available()
    return MayaCmds.shadingNode('lambert', asShader=True)


def createTexture():
    ensure_maya_available()
    return MayaCmds.shadingNode('file', asTexture=True)


def createMaterial():
    ensure_maya_available()
    material = MayaCmds.shadingNode('lambert', asShader=True)
    shading_group = MayaCmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    MayaCmds.connectAttr(material + '.outColor', shading_group + '.surfaceShader')
    return material


def createRenderLayer():
    ensure_maya_available()
    return MayaCmds.createRenderLayer()


def createRenderPass():
    ensure_maya_available()
    return MayaCmds.createRenderPass()


def createRenderSettings():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderSettings', asUtility=True)


def createRenderGlobals():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderGlobals', asUtility=True)


def createRenderView():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderView', asUtility=True)


def createRenderLayerManager():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderLayerManager', asUtility=True)


def createRenderPassManager():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderPassManager', asUtility=True)


def createRenderSettingsManager():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderSettingsManager', asUtility=True)


def createRenderGlobalsManager():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderGlobalsManager', asUtility=True)


def createRenderViewManager():
    ensure_maya_available()
    return MayaCmds.shadingNode('renderViewManager', asUtility=True)


def configure_render_globals(start_frame=1, end_frame=10):
    """Configure Maya render global settings.

    Args:
        start_frame (int): Animation start frame. Defaults to 1.
        end_frame (int): Animation end frame. Defaults to 10.
    """
    ensure_maya_available()
    MayaCmds.setAttr('defaultRenderGlobals.imageFormat', 8)
    MayaCmds.setAttr('defaultRenderGlobals.animation', 1)
    MayaCmds.setAttr('defaultRenderGlobals.startFrame', start_frame)
    MayaCmds.setAttr('defaultRenderGlobals.endFrame', end_frame)
    MayaCmds.setAttr('defaultRenderGlobals.byFrameStep', 1)
    MayaCmds.setAttr('defaultRenderGlobals.outFormatControl', 0)
    MayaCmds.setAttr('defaultRenderGlobals.putFrameBeforeExt', 1)
    MayaCmds.setAttr('defaultRenderGlobals.extensionPadding', 4)
    MayaCmds.setAttr('defaultRenderGlobals.periodInExt', 1)
    LOGGER.info("Render globals configured: frames %d-%d", start_frame, end_frame)


def list_all_nodes():
    """List all DAG nodes in the scene.

    Returns:
        list: Names of all DAG nodes.
    """
    ensure_maya_available()
    nodes = MayaCmds.ls(dag=True, long=True)
    LOGGER.debug("Listed %d DAG nodes", len(nodes))
    return nodes


def is_prman_available():
    return prman is not None


def get_rman_gettr():
    if prman_rmanGettr is None:
        raise RuntimeError('prman.rmanGettr() is not available.')
    return prman_rmanGettr()


def initialize_prman(name='python', options=None):
    if not is_prman_available():
        raise RuntimeError('RenderMan Python API is not available.')
    if hasattr(prman, 'RiBegin'):
        prman.RiBegin(name)
    elif hasattr(prman, 'Begin'):
        prman.Begin(name)
    else:
        raise RuntimeError('RenderMan API does not expose RiBegin or Begin.')

    if options:
        for key, value in options.items():
            set_prman_option(key, value)


def set_prman_option(name, value):
    if not is_prman_available():
        raise RuntimeError('RenderMan Python API is not available.')
    if hasattr(prman, 'RiOption'):
        prman.RiOption('render', name, value)
    elif hasattr(prman, 'Option'):
        prman.Option('render', name, value)
    else:
        raise RuntimeError('RenderMan API does not expose RiOption or Option.')


def create_prman_display(filename='output.exr', display='rgba', type='string'):
    if not is_prman_available():
        raise RuntimeError('RenderMan Python API is not available.')
    if hasattr(prman, 'RiDisplay'):
        prman.RiDisplay(filename, display, type)
    elif hasattr(prman, 'Display'):
        prman.Display(filename, display, type)
    else:
        raise RuntimeError('RenderMan API does not expose RiDisplay or Display.')


def end_prman():
    if not is_prman_available():
        return
    if hasattr(prman, 'RiEnd'):
        prman.RiEnd()
    elif hasattr(prman, 'End'):
        prman.End()


def backgroundRender():
    ensure_maya_available()
    return MayaCmds.ls(dag=True, long=True)


def bakeSimulation():
    ensure_maya_available()
    return MayaCmds.ls(dag=True, long=True)


def is_running_in_maya():
    return MayaCmds is not None


def initialize_maya_standalone():
    if maya is None:
        raise RuntimeError('Maya standalone module is not available.')
    maya.standalone.initialize(name='python')


def print_environment_status():
    """Log environment status for Maya and RenderMan APIs."""
    maya_avail = is_running_in_maya()
    prman_avail = is_prman_available()

    LOGGER.info('Maya API available: %s', maya_avail)
    LOGGER.info('RenderMan API available: %s', prman_avail)
    if maya_avail:
        LOGGER.info('Maya version: %s', MayaCmds.about(version=True))
    if prman_avail and hasattr(prman, '__version__'):
        LOGGER.info('RenderMan version: %s', prman.__version__)


def main():
    """Main entry point for module testing and initialization."""
    LOGGER.info('Running Alembic Maya-RenderMan integration tests...')
    print_environment_status()

    if is_running_in_maya():
        try:
            configure_render_globals(start_frame=1, end_frame=10)
            nodes = list_all_nodes()
            LOGGER.info('Found %d DAG nodes in scene.', len(nodes))
        except Exception as exc:
            LOGGER.error('Maya setup failed', exc_info=True)

    if is_prman_available():
        try:
            get_rman_gettr()
            LOGGER.info('RenderMan getter is available.')
        except RuntimeError as exc:
            LOGGER.warning('RenderMan helper error: %s', exc)

    if not is_running_in_maya() and not is_prman_available():
        LOGGER.error('Neither Maya nor RenderMan APIs are available. Run this module in a supported environment.')


if __name__ == '__main__':
    main()

