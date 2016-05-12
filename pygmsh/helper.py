# -*- coding: utf-8 -*-
#
import numpy


def rotation_matrix(u, theta):
    '''Return matrix that implements the rotation around the vector :math:`u`
    by the angle :math:`\\theta`, cf.
    https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle.

    :param u: rotation vector
    :param theta: rotation angle
    '''
    # Cross-product matrix.
    cpm = numpy.array([
        [0.0,   -u[2],  u[1]],
        [u[2],    0.0, -u[0]],
        [-u[1],  u[0],  0.0]
        ])
    c = numpy.cos(theta)
    s = numpy.sin(theta)
    R = numpy.eye(3) * c \
        + s * cpm \
        + (1.0 - c) * numpy.outer(u, u)
    return R


#def generate_mesh(geo_object, optimize=True):
#    import meshio
#    import os
#    import subprocess
#    import tempfile
#
#    handle, filename = tempfile.mkstemp(suffix='.geo')
#    os.write(handle, geo_object.get_code())
#    os.close(handle)
#
#    handle, outname = tempfile.mkstemp(suffix='.msh')
#
#    cmd = ['gmsh', '-3', filename, '-o', outname]
#    if optimize:
#        cmd += ['-optimize']
#    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
#    print(out)
#
#    points, cells, _, _, _ = meshio.read(outname)
#
#    return points, cells

# Originally from: pygmsh/helper.py
def generate_mesh(geo_object, optimize=True, return_msh_fh=False, verbose=False):
    import meshio
    import os
    import subprocess
    import tempfile

    geo_handle = tempfile.NamedTemporaryFile(suffix='.geo', delete=True)
    geo_handle.write(geo_object.get_code())
    geo_handle.flush()

    msh_handle  = tempfile.NamedTemporaryFile(suffix='.msh', delete=True)

    cmd = ['gmsh', '-3', geo_handle.name, '-o', msh_handle.name]
    if optimize:
        cmd += ['-optimize']
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    if verbose:
        print(out)
    
    if return_msh_fh:
        return msh_handle

    points, cells, _, _, _ = meshio.read(msh_handle.name)

    return points, cells
