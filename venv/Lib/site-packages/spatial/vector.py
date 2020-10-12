import math
import doctest
import operator


# ------------------------------------------------------------------------------
class Vector3(object):
    """
    This class represents a vector which exposes the typically used
    methods of a 3d vector such as cross and dot products as well as 
    length/magnitude.
    
        ..code-block:: python 
            >>> import spatial
            >>> 
            >>> # -- Create two vectors
            >>> v1 = spatial.Vector3(1.0, 0.0, 0.0)
            >>> v2 = spatial.Vector3(0.0, 1.0, 0.0)
            >>> 
            >>> # -- Calculate the angle between the two vectors
            >>> v1.angle(v2)
            1.57079632679...
        
    The Vector supports basic in-place operations such as 
    Add, Subtract, Multiply and Divide.
    
    ..code-block:: python
        >>> import spatial
        >>> 
        >>> # -- Create two vectors
        >>> v1 = spatial.Vector3(1.0, 2.0, 3.0)
        >>> v2 = spatial.Vector3(1.0, 2.0, 3.0)
        >>> 
        >>> # -- Add the two vectors
        >>> print(v1 + v2)
        Vector3(2.0, 4.0, 6.0)
        >>> 
        >>> # -- Subtract the two vectors
        >>> print(v1 - v2)
        Vector3(0.0, 0.0, 0.0)
        >>> 
        >>> # -- Multiply the two vectors
        >>> print(v1 * v2)
        Vector3(1.0, 4.0, 9.0)
        >>> 
        >>> # -- Divide the two vectos
        >>> print(v1 / v2)
        Vector3(1.0, 1.0, 1.0)

    """
    _DEGREES_TO_RADIANS = 0.0174533
    _RADIANS_TO_DEGREES = 1.5708

    # --------------------------------------------------------------------------
    def __init__(self, x=0, y=0, z=0, point=None):

        # -- Populate our given variables
        self._x = point[0] if point else x
        self._y = point[1] if point else y
        self._z = point[2] if point else z

    # --------------------------------------------------------------------------
    def __repr__(self):
        return 'Vector3(%s, %s, %s)' % (
            self._x,
            self._y,
            self._z,
        )

    # --------------------------------------------------------------------------
    def __add__(self, value):
        return self._perform_operator(value, operator.add)

    # --------------------------------------------------------------------------
    def __sub__(self, value):
        return self._perform_operator(value, operator.sub)

    # --------------------------------------------------------------------------
    def __mul__(self, value):
        return self._perform_operator(value, operator.mul)

    # --------------------------------------------------------------------------
    def __div__(self, value):
        return self._perform_operator(value, operator.div)

    # --------------------------------------------------------------------------
    def __eq__(self, other):
        """ == """
        if not isinstance(other, Vector3):
            return False

        if self.x() != other.x() or self.y() != other.y() or self.z() != other.z():
            return False

        return True

    # --------------------------------------------------------------------------
    def __iter__(self):
        yield self._x
        yield self._y
        yield self._z

    # --------------------------------------------------------------------------
    def _perform_operator(self, value, operation):
        """
        Performs an function between the two values. If the given
        value is a Vector3 each component will be calculated, otherwise
        each component will be calculated against the single value.
        
        :param value: Vector3, float or int
        :param operation: function taking two arguments and returning a number
        
        :return: Vector3
        """
        is_vector = isinstance(value, Vector3)

        _x = value.x() if is_vector else value
        _y = value.y() if is_vector else value
        _z = value.z() if is_vector else value

        return Vector3(
            x=operation(self.x(), _x),
            y=operation(self.y(), _y),
            z=operation(self.z(), _z),
        )

    # --------------------------------------------------------------------------
    def x(self):
        """
        Returns the Y component of the vector
        
        ..code-block:: python
            >>> import spatial
            >>> 
            >>> # -- Create two vectors
            >>> v1 = spatial.Vector3(1.0, 2.0, 3.0)
            >>> 
            >>> # -- Extract the Z channel
            >>> v1.x()
            1.0
            
        :return: Number
        """
        return self._x

    # --------------------------------------------------------------------------
    def y(self):
        """
        Returns the Y component of the vector
        
        ..code-block:: python
            >>> import spatial
            >>> 
            >>> # -- Create two vectors
            >>> v1 = spatial.Vector3(1.0, 2.0, 3.0)
            >>> 
            >>> # -- Extract the Z channel
            >>> v1.y()
            2.0
            
        :return: Number
        """
        return self._y

    # --------------------------------------------------------------------------
    def z(self):
        """
        Returns the Z component of the vector
        
        ..code-block:: python
            >>> import spatial
            >>> 
            >>> # -- Create two vectors
            >>> v1 = spatial.Vector3(1.0, 2.0, 3.0)
            >>> 
            >>> # -- Extract the Z channel
            >>> v1.z()
            3.0
            
        :return: Number
        """
        return self._z

    # --------------------------------------------------------------------------
    def angle(self, other):
        """
        Returns the angle between this vector and the other vector in 
        radians.
        
        ..code-block:: python 
            >>> import spatial
            >>> 
            >>> # -- Create two vectors
            >>> v1 = spatial.Vector3(1.0, 0.0, 0.0)
            >>> v2 = spatial.Vector3(0.0, 1.0, 0.0)
            >>> 
            >>> # -- Calculate the angle between the two vectors
            >>> v1.angle(v2)
            1.57079632679...
            
        :param other: Vector3 object
        
        :return: Angle in radians
        """
        return math.acos(self.dot(other) / (self.length() * other.length()))

    # --------------------------------------------------------------------------
    def cross(self, other):
        """
        Calculates the cross product between this vector and the other
        vector.
        
        ..code-block:: python
            >>> import spatial
            >>> 
            >>> # -- Create two vectors
            >>> v1 = spatial.Vector3(1.0, 1.0, 1.0)
            >>> v2 = spatial.Vector3(3.0, 2.0, 0.0)
            >>> 
            >>> # -- Calculate the cross product
            >>> v1.cross(v2)
            Vector3(-2.0, 3.0, -1.0)

        :param other: Vector3 object
        
        :return: Vector3
        """
        return Vector3(
                x=self.y()*other.z() - self.z()*other.y(),
                y=self.z()*other.x() - self.x()*other.z(),
                z=self.x()*other.y() - self.y()*other.x()
        )

    # --------------------------------------------------------------------------
    def dot(self, other):
        """
        Returns teh dot product between this vector and the other 
        vector.
        
        ..code-block:: python
            >>> import spatial
            >>> 
            >>> # -- Create two vectors
            >>> v1 = spatial.Vector3(1.0, 1.0, 1.0)
            >>> v2 = spatial.Vector3(3.0, 2.0, 0.0)
            >>> 
            >>> # -- Calculate the dot product
            >>> v1.dot(v2)
            5.0
            
        :param other: Vector3 object 
        
        :return: float
        """
        return (self.x() * other.x()) + (self.y() * other.y()) + (self.z() * other.z())

    # --------------------------------------------------------------------------
    def distance(self, other):
        """
        Calculates the distnace between this vector and another
        vector object. 
        
        ..code-block:: pythonimport spatial
            
            >>> import spatial
            >>> 
            >>> # -- Create two vectors
            >>> v1 = spatial.Vector3(1.0, 0.0, 0.0)
            >>> v2 = spatial.Vector3(0.0, 1.0, 0.0)
            >>> 
            >>> # -- Calculate the distance between the two
            >>> result = v1.distance(v2)
            >>> 
            >>> print(result)
            1.41421356237
        
        :param other: Vector3 object
        
        :return: Distance between the two vectors as a float 
        """
        return (self - other).length()

    # --------------------------------------------------------------------------
    def is_parallel(self, other, radian_tolerance=None, degree_tolerance=None):
        """
        Tests whether this agnle is parallel to the other vector and 
        allows for tolerance values to be defined.
        
        ..code-block:: python
            >>> import spatial
            >>> 
            >>> # -- Create two vectors, almost parallel
            >>> v1 = spatial.Vector3(1.0, 0.0, 0.0)
            >>> v2 = spatial.Vector3(3.0, 0.0001, 0.0)
            >>> 
            >>> # -- Test whether they are parallel, but giving a tolerance
            >>> # -- of one degree
            >>> v1.is_parallel(v2, degree_tolerance=1)
            True
            
        :param other: Vector3 to test against
        :param radian_tolerance: How much variance we allow in radians
        :param degree_tolerance: How much variance we allow in degrees
        
        :return: bool
        """
        angle = abs(self.angle(other))

        # -- We'll only test in radians, so if we're not given any
        # -- tolerance values we set it to zero
        radian_tolerance = radian_tolerance or 0

        # -- If we're given degrees, convert that to radians
        if degree_tolerance:
            radian_tolerance = degree_tolerance * self._DEGREES_TO_RADIANS

        if angle <= radian_tolerance:
            return True

        return False

    # --------------------------------------------------------------------------
    def is_perpendicular(self, other, radian_tolerance=None, degree_tolerance=None):
        """
        Tests whether this agnle is perpendicular to the other vector and 
        allows for tolerance values to be defined.

        ..code-block:: python
            >>> import spatial
            >>> 
            >>> # -- Create two vectors, almost parallel
            >>> v1 = spatial.Vector3(1.0, 0.0, 0.0)
            >>> v2 = spatial.Vector3(0.0, 1.0, 0.0)
            >>> 
            >>> # -- Test whether they are parallel, but giving a tolerance
            >>> # -- of one degree
            >>> v1.is_perpendicular(v2, degree_tolerance=0.01)
            True

        :param other: Vector3 to test against
        :param radian_tolerance: How much variance we allow in radians
        :param degree_tolerance: How much variance we allow in degrees

        :return: bool
        """
        angle = 1.5708 - abs(self.angle(other))

        # -- We'll only test in radians, so if we're not given any
        # -- tolerance values we set it to zero
        radian_tolerance = radian_tolerance or 0

        # -- If we're given degrees, convert that to radians
        if degree_tolerance:
            radian_tolerance = degree_tolerance * self._DEGREES_TO_RADIANS

        if angle <= radian_tolerance:
            return True

        return False

    # --------------------------------------------------------------------------
    def length(self):
        """
        Returns the length (magnitude) of this vector.
        
        ..code-block:: python
            >>> import spatial
            >>> 
            >>> # -- Create two vectors, almost parallel
            >>> v1 = spatial.Vector3(1.0, 1.0, 0.0)
            >>> 
            >>> v1.length()
            1.41421356237...
            
        :return: float
        """
        return math.sqrt(self.x()**2 + self.y()**2 + self.z()**2)

    # --------------------------------------------------------------------------
    def normalised(self):
        """
        Returns a normalised version of this vector. 
        
        ..code-block:: python
            >>> import spatial
            >>> 
            >>> # -- Create two vectors, almost parallel
            >>> v1 = spatial.Vector3(1.0, 1.0, 0.0)
            >>> 
            >>> v1.normalised()
            Vector3(0.5, 0.5, 0.0)
            
        :return: Vector3
        """
        total = sum(self)

        return Vector3(
            *[
                n / total
                for n in self
            ]
        )


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    doctest.testmod(optionflags=doctest.ELLIPSIS)
