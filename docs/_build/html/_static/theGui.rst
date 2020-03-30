The GUI
=======

The GUI is mainly divided into three parts. The toolbar where to this point GIMLIs polytools and some more functions are stored. Beneath that there is a property table on the left that will hold parameters of the drawn polys - that will happen to the right. Everything that is clickable should have a tool tip. So if hovered over a button it should show whats its use.

The Toolbar
-----------

.. |open| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_image.svg
    :width: 20px

.. |polygonize| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_polygonize.svg
    :width: 20px

.. |marker| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/marker_check.svg
    :width: 20px

.. |magnetPoly| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/magnetize.svg
    :width: 20px

.. |polyWorld| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_spanWorld.svg
    :width: 20px
.. |world| replace:: createWorld
.. _world: http://pygimli.org/pygimliapi/_generated/pygimli.meshtools.html?highlight=createworld#pygimli.meshtools.createWorld>

.. |polyPoly| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_spanPoly.svg
    :width: 20px
.. |poly| replace:: createPolygon
.. _poly: http://pygimli.org/pygimliapi/_generated/pygimli.meshtools.html?highlight=createpolygon#pygimli.meshtools.createPolygon

.. |polyRect| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_spanRectangle.svg
    :width: 20px
.. |rect| replace:: createRectangle
.. _rect: http://pygimli.org/pygimliapi/_generated/pygimli.meshtools.html?highlight=createpolygon#pygimli.meshtools.createRectangle

.. |polyCircle| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_spanCircle.svg
    :width: 20px
.. |circle| replace:: createCircle
.. _circle: http://pygimli.org/pygimliapi/_generated/pygimli.meshtools.html?highlight=createpolygon#pygimli.meshtools.createCircle

.. |polyLine| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_spanLine.png
    :width: 20px
.. |line| replace:: createLine
.. _line: http://pygimli.org/pygimliapi/_generated/pygimli.meshtools.html?highlight=createpolygon#pygimli.meshtools.createLine

+--------------+-------------+--------------------------------------------------------------------+
|    Symbol    | Tool        | | Descritption                                                     |
+==============+=============+====================================================================+
| |open|       | Open        | | Allows to open a picture of a drawing or a scheme so that it can |
|              |             | | be analyzed for contrasts (with OpenCV) and later processed to   |
|              |             | | obtain the polygons. If no OpenCV is installed the loaded        |
|              |             | | picture can only be set as background.                           |
+--------------+-------------+--------------------------------------------------------------------+
| Threshold    | lower       | | First box contains the value (0-254) for the bottom threshold    |
|              |             | | value threshold for the contour detection.                       |
+              +-------------+--------------------------------------------------------------------+
|              | upper       | | Second box contains the value (1-255) for the top threshold value|
|              |             | | threshold for the contour detection.                             |
+--------------+-------------+--------------------------------------------------------------------+
| Density of   | points      | | Defines a step width for every path plotted.                     |
+--------------+-------------+--------------------------------------------------------------------+
| Number of    | paths       | | The algorithm for contour detection (OpenCV) sorts the paths     |
|              |             | | after the area they are enclosing. So the higher the value is set|
|              |             | | the more paths will be plotted/ the more polygons will be        |
|              |             | | obtained. The outcome depends on the contrast and can be bad.    |
+--------------+-------------+--------------------------------------------------------------------+
| |polygonize| | Polygonize  | | After analyzing a given image and extracting paths accordingly   |
|              |             | | to the set contrast and parameters, this tool will convert all   |
|              |             | | received paths into a polygon. Only enabled with OpenCV.         |
+--------------+-------------+--------------------------------------------------------------------+
| | GIMLi's **PolyTools** are integrated in a matter that if a polygon is finished the whole      |
| | figure will be rebuilt.                                                                       |
+--------------+-------------+--------------------------------------------------------------------+
| |polyWorld|  | |world|_    | | polygon will be built. To create the modelling world simply      |
|              |             | | activate the function and span a rectangle on the plotting area. |
+--------------+-------------+--------------------------------------------------------------------+
| |polyPoly|   | |poly|_     | | This action enables you to create a polygon by clicking around in|
|              |             | | the plotting area. To finish and **close the polygon** just      |
|              |             | | double click.                                                    |
+--------------+-------------+--------------------------------------------------------------------+
| |polyRect|   | |rect|_     | | Functioning the same as |world|_ this will create a polygon      |
|              |             | | rectangle.                                                       |
+--------------+-------------+--------------------------------------------------------------------+
| |polyCircle| | |circle|_   | | By clicking and dragging the cursor a circle is spanned.         |
+--------------+-------------+--------------------------------------------------------------------+
| |polyLine|   | |line|_     | | Creating a polyLine is simply done by clicking. No dragging or   |
|              |             | | whatsoever.                                                      |
+--------------+-------------+--------------------------------------------------------------------+
| | Marker handling                                                                               |
+--------------+-------------+--------------------------------------------------------------------+
| |marker|     | check marker| | Since it is possible that some irregular polygons will be created|
|              |             | | this tool might come in handy. Activated, each polygon gets a red|
|              |             | | dot which will be draggable. By deactivating (clicking again) the|
|              |             | | action the changes will be adopted.                              |
+--------------+-------------+--------------------------------------------------------------------+
| | Magnetize... (since it might be necessary to snap to specific points)                         |
+--------------+-------------+--------------------------------------------------------------------+
| |magnetPoly| | ...Polygon  | | This feature allows to magnetize the nodes of a polygon. After   |
|              |             | | its activation hovering near to or over the nodes will color them|
|              |             | | red. If a polyTool is active a clicking when a node is red will  |
|              |             | | catch the coordinates of that node.                              |
+--------------+-------------+--------------------------------------------------------------------+


Property Table
--------------
The first tab on the left mainly holds the property table. On the bottom are a few more buttons to handle the model creation. The table stores the parameters for every polygon shown on the right. GIMLi's polygons are holding various arguments which are adjustable in that table. The functions on the bottom are working as follows.

.. |undo| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_undo_black_18px.svg
    :width: 20px

.. |redo| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_redo_black_18px.svg
    :width: 20px

.. |refresh| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_refresh_black_24px.svg
    :width: 20px

.. |save| image:: https://rawgit.com/frodo4fingers/gimod/master/icons/ic_save_black_24px.svg
    :width: 20px

+--------------+-------------+--------------------------------------------------------------------+
|    Symbol    | Function    | Descritption                                                       |
+==============+=============+====================================================================+
| |undo|       | Undo        | Undo the last polygon made.                                        |
+--------------+-------------+--------------------------------------------------------------------+
| |redo|       | Redo        | Redo the undone polygons.                                          |
+--------------+-------------+--------------------------------------------------------------------+
| *regions*    | Plot        | Will plot the figure colored after a polygons assigned markers.    |
+--------------+-------------+--------------------------------------------------------------------+
| *attributes* | Plot        | Will plot the figure according to the polygons attributes from the |
|              |             | table.                                                             |
+--------------+-------------+--------------------------------------------------------------------+
| |refresh|    | Refresh     | Reads the table and plot option and builds the polygon again.      |
+--------------+-------------+--------------------------------------------------------------------+
| |save|       | Save        | Saves the polygon as ``*.poly``.                                   |
+--------------+-------------+--------------------------------------------------------------------+


Mesh Options
------------
The second tab on the left holds options for mesh generation. This aims at GIMLI's `createMesh <http://pygimli.org/pygimliapi/_generated/pygimli.meshtools.html?highlight=createmesh#pygimli.meshtools.createMesh>`_.


Plotting Area
-------------
The plotting area is the standard matplotlib plot with its toolbar...
