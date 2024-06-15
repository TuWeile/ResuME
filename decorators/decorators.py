class Singleton:
    """
    A decorator class to implement the Singleton design pattern.

    This decorator ensures that a class has only one instance and provides a global point of access to it.
    """
    _instances = {}

    def __init__(self, cls):
        """
        Initializes the SingletonDecorator with the class to be decorated.
        :param cls: The class to be decorated as a singleton.
        """
        self.cls = cls

    def __call__(self, *args, **kwargs):
        """
        Returns the single instance of the decorated class, creating it if it doesn't already exist.
        :param args: Variable length argument list passed to the class constructor.
        :param kwargs: Arbitrary keyword arguments passed to the class constructor.
        :return: object: The single instance of the decorated class.
        """
        if self.cls not in self._instances:
            self._instances[self.cls] = self.cls(*args, **kwargs)

        return self._instances[self.cls]
