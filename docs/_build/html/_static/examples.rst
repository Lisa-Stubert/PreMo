Examples
========

starting with a sketch you made
-------------------------------

since model creation might be time intensive by hand you can set your chosen image as background and draw the polygons. At least thats the goal for now - does not work as desired... yet.

.. figure:: https://rawgit.com/frodo4fingers/gimod/dev/screenshots/00_0background.png
    :width: 600px

What works quite fine is the recognition of certain contrasts of the given image. You load it and set the lower and upper threshold via the first two spin boxes.

.. figure:: https://rawgit.com/frodo4fingers/gimod/dev/screenshots/00_1polygon.png
    :width: 600px

If the outcome is satisfactory you can set the point density via the third widget. Since every dot will be a node in the later mesh, it makes sense to reduce the density.

.. figure:: https://rawgit.com/frodo4fingers/gimod/dev/screenshots/00_2polygonDens.png
    :width: 600px

The information in the statusbar on the bottom left points out how many polygons were found by the algorithm OpenCV provides. The fourth widget holds the tool to show more of the found polygons.

.. figure:: https://rawgit.com/frodo4fingers/gimod/dev/screenshots/00_3polygonDens.png
    :width: 600px

If all that is selected you hit the play button and the structure will be converted to a polygon. On the left side the tree view holds information to every polygon made.

.. figure:: https://rawgit.com/frodo4fingers/gimod/dev/screenshots/00_4poly.png
    :width: 600px

.. |polygonize| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_polygonize.svg
    :width: 20px

In GIMLi every polygon or region gets a marker which later specifies where an attribute or parameter belongs. You might see the problem within the x-wings regions or can imagine a shape, where the center may lay out of the polygon itself. So in order not to lose a marker you can check the marker positions with |polygonize|. That option will plot a dot for every polygon in the figure and they're movable.

.. figure:: https://rawgit.com/frodo4fingers/gimod/dev/screenshots/00_5bpoly.png
    :width: 600px

For all polys a dot will be plotted but only for arbitrary shaped polygons moving the marker position makes sense. After shifting the marker dots you accept the changes with clicking the the button again.

.. figure:: https://rawgit.com/frodo4fingers/gimod/dev/screenshots/00_6poly.png
    :width: 600px

Yes, it's upside down... for now.
