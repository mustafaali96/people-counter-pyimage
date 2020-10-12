"""
This module contains bounding box classes. A Bounding Box allows you
to calculate the overall bounds of a point cloud - but does not store
the point cloud itself, it simply expands to match the outer most limits
of the point cloud data.

There are three Bounding Box classes:

Bounds: This is an N-Dimensional bounding box, allowing your points to
be of any dimensional length. This is useful if working in one dimension
or in a dimensional space greater than three dimensions.

Bounds2D: This inherits from Bounds - so gives all the same funcitonaltiy
except it has some convenience functions with an assumption of width
and height.

Bounds3D: Much like Bounds2D, Bounds3D is a Bounds object which exposes
functionality with the assumption of Width, Height and Depth.

In this example we create two three dimensional bounding boxes
and test wether they intersect

```python
# -- Test bound intersections
points_a = [
    [0, 0, 0],
    [1, 1, 1],
]

points_b = [
    [5, 5, -5],
    [3, 3, 3],
]

bounds_a = spatial.Bounds3D(points_a)
bounds_b = spatial.Bounds3D(points_b)

print('Does bounds A intersect with bounds B : %s' % ('Yes' if bounds_b.intersects(bounds_a) else 'No'))
```


In the following example we create a bounding box and test whether
the given point is inside the bounds:

```python
bounds = spatial.Bounds2D()

# -- Create a point cloud
points = [
    [-2, -2],
    [2, 2],
]

# -- Add all our points
bounds.add_points(points)

# -- Test whether a point is inside the bounds
outside_point = [3, 5]
print('Bound contains %s : %s' % (outside_point, bounds.contains(outside_point)))

# -- Same test giving a point inside the bounds
inside_point = [1, 1]
print('Bound contains %s : %s' % (inside_point, bounds.contains(inside_point)))
```

"""


# ------------------------------------------------------------------------------
class Bounds(object):
    """
    An N-Dimensional bounding box which can be expanded by 
    adding points into the bounds. 
    """
    _MIN = 0
    _MAX = 1

    # --------------------------------------------------------------------------
    def __init__(self, points=None):

        # -- This is what we store the max and min values
        # -- of each dimension
        self._bounds = list()

        # -- For performance we cache the number of dimensions
        # -- rather than calculate it
        self._num_dimensions = 0

        # -- If we're given points during instancing, add them
        # -- now
        if points:
            self.add_points(points)

    # --------------------------------------------------------------------------
    def _initialise_bounds(self, dimensions):
        """
        To ensure we're always operating with the right amount of values
        we add 'dummy' values into our bounding list to ensure we can 
        always perform min/max logic without testing list lengths.
        
        :param dimensions: Number of dimensions to initialise with
         
        :return: None 
        """
        self._num_dimensions = dimensions

        for idx in range(dimensions):
            self._bounds.append(
                [
                    _UndefinedBoundValue(),  # -- Min
                    _UndefinedBoundValue(),  # -- Max
                ],
            )

    # --------------------------------------------------------------------------
    def add_point(self, point):
        """
        Adds a single point to the bounds. If that point is outside
        the current bounds the bounds will grow to accomodate it.

        :param point: List of length equal to the bounds dimension. If this
            is the first point being added that will define the dimensions
            of the Bounds.

        :return: None 
        """
        # -- If this is the first initialisation of the dimensions we
        # -- populate them with undefined values
        if not self._bounds:
            self._initialise_bounds(len(point))

        # -- point is a list of values
        for dimension, value in enumerate(point):
            self._bounds[dimension][self._MIN] = min(
                self._bounds[dimension][self._MIN],
                value,
            )

            self._bounds[dimension][self._MAX] = max(
                self._bounds[dimension][self._MAX],
                value,
            )

    # --------------------------------------------------------------------------
    # noinspection PyUnresolvedReferences
    def add_points(self, points):
        """
        Convenience function for adding a list of points in a single
        call.
        
        ..code-block: python
            
            >>> bounds.add_points(
            ...     [
            ...         [0, 0],
            ...         [6, 5],
            ...         [2, 9],
            ...     ]
            ... )
        
        :param points: list([], [], [], ...) 
        :return: None
        """
        for point in points:
            self.add_point(point)

    # --------------------------------------------------------------------------
    def center(self):
        """
        Returns the center point of the bounding box
        
        :return: Point of length matching the dimension of the bounds
        """
        center_point = list()

        for dimension in range(self.num_dimensions()):
            center_point.append(
                self.min(dimension) + (self.length(dimension) * 0.5)
            )

        return center_point

    # --------------------------------------------------------------------------
    def contains(self, point):
        """
        Tests whether the given point is within the bounding box
        
        :param point: List of length equal to the bounding dimension
         
        :return: bool 
        """
        for dimension in range(self.num_dimensions()):
            if point[dimension] < self._bounds[dimension][self._MIN]:
                return False

            if point[dimension] > self._bounds[dimension][self._MAX]:
                return False

        return True

    # --------------------------------------------------------------------------
    def num_dimensions(self):
        """
        Returns the number of dimensions this bounding box represents
        
        :return: int 
        """
        return self._num_dimensions

    # --------------------------------------------------------------------------
    def clear(self):
        """
        Resets the bounding data to a null state. 
        
        :return: None 
        """
        self._bounds = list()

    # --------------------------------------------------------------------------
    def min(self, dimension):
        """
        Returns the minimum bound limit of the given dimension
        
        :param dimension: Dimension index to access
         
        :return: number 
        """
        return self._bounds[dimension][self._MIN]

    # --------------------------------------------------------------------------
    def max(self, dimension):
        """
        Returns the maximum bound limit of the given dimension
        
        :param dimension: Dimension index to access
         
        :return: number 
        """
        return self._bounds[dimension][self._MAX]

    # --------------------------------------------------------------------------
    def length(self, dimension):
        """
        Returns the length of the bounds for the given dimension.
        
        :param dimension: Dimension index to access
         
        :return: number 
        """
        return self.max(dimension) - self.min(dimension)

    # --------------------------------------------------------------------------
    def area(self):
        """
        Calculates the area of the bounds. 
        
        :return: float
        """
        total_area = 0
        for dimension in range(len(self._bounds)):
            if not total_area:
                total_area = self.length(dimension)

            else:
                total_area *= self.length(dimension) or 1.0

        return total_area

    # --------------------------------------------------------------------------
    def intersects(self, bounds):
        """
        Tests whether this bounding box and the given bounding box
        intersect one-another.

        :param bounds: spatial.Bounds

        :return: bool 
        """
        for dimension in range(bounds.num_dimensions()):
            if dimension > self.num_dimensions():
                return False

            if bounds.min(dimension) >= self.min(dimension) and bounds.min(
                    dimension) <= self.max(dimension):
                return True

            if bounds.max(dimension) >= self.min(dimension) and bounds.max(
                    dimension) <= self.max(dimension):
                return True

        return False


# ------------------------------------------------------------------------------
class Bounds2D(Bounds):
    """
    A 2 Dimensional bounding box
    """
    _WIDTH = 0
    _HEIGHT = 1

    # --------------------------------------------------------------------------
    def _initialise_bounds(self, dimensions):
        """
        Re-implement this function to ensure the data coming into the bounds
        matches the expected data for two dimensions.
        
        :param dimensions: Number of dimensions.
         
        :return: 
        """
        if dimensions != 2:
            raise Exception(
                (
                    'You cannot initialise a 2d bounds with point data of '
                    '%s dimensions. Please use spatial.Bounds instead.'
                ) % self.num_dimensions()
            )

        # -- Allow the initialisation to go through
        super(Bounds2D, self)._initialise_bounds(dimensions)

    # --------------------------------------------------------------------------
    def width(self):
        return self.length(self._WIDTH)

    # --------------------------------------------------------------------------
    def height(self):
        return self.length(self._HEIGHT)

    # --------------------------------------------------------------------------
    def bottom(self):
        return self._bounds[self._HEIGHT][self._MIN]

    # --------------------------------------------------------------------------
    def top(self):
        return self._bounds[self._HEIGHT][self._MAX]

    # --------------------------------------------------------------------------
    def left(self):
        return self._bounds[self._WIDTH][self._MIN]

    # --------------------------------------------------------------------------
    def right(self):
        return self._bounds[self._WIDTH][self._MAX]


# ------------------------------------------------------------------------------
class Bounds3D(Bounds2D):
    """
    A 2 Dimensional bounding box
    """
    # -- Extending the 2d bounds means we only need
    # -- to add in the details for depth, as we get width
    # -- and height for free
    _DEPTH = 2

    # --------------------------------------------------------------------------
    def _initialise_bounds(self, dimensions):
        """
        Re-implement this function to ensure the data coming into the bounds
        matches the expected data for two dimensions.
        
        :param dimensions: Number of dimensions.
         
        :return: 
        """
        if dimensions != 3:
            raise Exception(
                (
                    'You cannot initialise a 3d bounds with point data of '
                    '%s dimensions. Please use spatial.Bounds instead.'
                ) % self.num_dimensions()
            )

        # -- Allow the initialisation to go through
        Bounds._initialise_bounds(self, dimensions)

    # --------------------------------------------------------------------------
    def depth(self):
        return self.length(self._DEPTH)

    # --------------------------------------------------------------------------
    def front(self):
        return self._bounds[self._DEPTH][self._MIN]

    # --------------------------------------------------------------------------
    def back(self):
        return self._bounds[self._DEPTH][self._MAX]


# ------------------------------------------------------------------------------
class _UndefinedBoundValue(object):
    """
    This represents a dummy value used by bounds when initialising which
    always test consistently during min/max calls.
    """

    # --------------------------------------------------------------------------
    def __lt__(self, value):
        return True

    # --------------------------------------------------------------------------
    def __gt__(self, value):
        return True
