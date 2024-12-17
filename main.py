from typing import Any, Iterator


def convert_to_bytearray(*args: Any) -> bytearray:
    result = bytearray()

    def convert_item(item: Any) -> None:
        if isinstance(item, str):
            result.extend(item.encode('utf-8'))
        elif isinstance(item, (int, float)):
            result.extend(bytearray(str(item), 'utf-8'))
        elif isinstance(item, bytes):
            result.extend(item)
        elif isinstance(item, (list, tuple, set)):
            for elem in item:
                convert_item(elem)
        elif isinstance(item, dict):
            for key, value in item.items():
                convert_item(key)
                convert_item(value)
        else:
            raise TypeError(f"Unsupported type: {type(item)}")

    for arg in args:
        convert_item(arg)

    return result


def convert_from_bytearray(bytearray_: bytearray) -> list:
    result = []
    current_item = bytearray()
    is_key = True
    key = None

    for byte in bytearray_:
        if byte == 0:
            if is_key:
                key = current_item.decode('utf-8')
                is_key = False
            else:
                value = current_item.decode('utf-8')
                result.append((key, value))
                is_key = True
                current_item = bytearray()
        else:
            current_item.append(byte)

    if current_item:
        if is_key:
            key = current_item.decode('utf-8')
            result.append(key)
        else:
            value = current_item.decode('utf-8')
            result.append((key, value))

    return result


class Link:
    def __init__(self, *args: Any) -> None:
        """
        Initializes the Link object.

        :param args: Variable number of arguments.
        """
        self.objects = list(args)

    def __str__(self) -> str:
        """
        Returns a string representation of the Link object.

        :return: String representation of the list of objects.
        """
        return f"{self.objects}"

    def __len__(self) -> int:
        return len(self.objects)

    def __sizeof__(self) -> int:
        """
        Returns the size of the list of objects in bytes.

        :return: Size of the list of objects in bytes.
        """
        from sys import getsizeof
        return getsizeof(self) + getsizeof(self.objects)

    def __format__(self, format_spec) -> str:
        from sys import getsizeof
        """
        Formats the Link object according to the format specifier.

        :param format_spec: Format specifier.
        :return: Formatted representation of the Link object.
        """
        if format_spec in ["*", "all"]:
            return f"Size: {getsizeof(self.objects)}\nElements: {' '.join(map(str, self.objects))}"
        elif format_spec in ["!", "object"]:
            return ' '.join(map(str, self.objects))
        elif format_spec in ["@", "size"]:
            return str(getsizeof(self.objects))

    def __eq__(self, other: "Link") -> bool:
        """
        Checks if two Link objects have equal list lengths.

        :param other: Another Link object.
        :return: True if list lengths are equal, False otherwise.
        """
        return len(self.objects) == len(other.objects)

    def __ne__(self, other: "Link") -> bool:
        """
        Checks if two Link objects have unequal list lengths.

        :param other: Another Link object.
        :return: True if list lengths are unequal, False otherwise.
        """
        return len(self.objects) != len(other.objects)

    def __lt__(self, other: "Link") -> bool:
        """
        Checks if the length of the list of objects is less than another list.

        :param other: Another Link object.
        :return: True if the length is less, False otherwise.
        """
        return len(self.objects) < len(other.objects)

    def __gt__(self, other: "Link") -> bool:
        """
        Checks if the length of the list of objects is greater than another list.

        :param other: Another Link object.
        :return: True if the length is greater, False otherwise.
        """
        return len(self.objects) > len(other.objects)

    def __le__(self, other: "Link") -> bool:
        """
        Checks if the length of the list of objects is less than or equal to another list.

        :param other: Another Link object.
        :return: True if the length is less than or equal, False otherwise.
        """
        return len(self.objects) <= len(other.objects)

    def __ge__(self, other: "Link") -> bool:
        """
        Checks if the length of the list of objects is greater than or equal to another list.

        :param other: Another Link object.
        :return: True if the length is greater than or equal, False otherwise.
        """
        return len(self.objects) >= len(other.objects)

    def __iadd__(self, other) -> "Link":
        """
        Adds elements from another list to the end of the current list.

        :param other: List of elements to add.
        :return: Link object with the updated list.
        """
        self.objects.extend(other)
        return self

    def __isub__(self, other) -> "Link":
        """
        Removes an element from the current list.

        :param other: Element to remove.
        :return: Link object with the updated list.
        """
        try:
            self.objects.remove(other)
        except ValueError:
            raise ValueError("Element not found in the list")
        return self

    def __getitem__(self, index: int) -> Any:
        """
        Returns an element at the specified index.

        :param index: Index of the element.
        :return: Element at the specified index.
        """
        try:
            return self.objects[index]
        except IndexError:
            raise IndexError("Incorrect index!")

    def __setitem__(self, index: int, value: Any) -> None:
        """
        Sets a value at the specified index.

        :param index: Index of the element.
        :param value: New value of the element.
        """
        try:
            self.objects[index] = value
        except IndexError:
            raise IndexError("Incorrect index!")

    def __delitem__(self, index: int) -> None:
        """
        Deletes an element at the specified index.

        :param index: Index of the element to delete.
        """
        try:
            del self.objects[index]
        except IndexError:
            raise IndexError("Incorrect index!")

    def __iter__(self) -> Iterator:
        """
        Returns an iterator for the list of objects.

        :return: Iterator for the list of objects.
        """
        return iter(self.objects)

    def __contains__(self, item) -> bool:
        """
        Returns True if the item is in self.objects, False otherwise.

        :return: bool - True if the item is in self.objects, False otherwise.
        """
        return item in self.objects

    def add(self, value: Any) -> None:
        """
        Adds an element to the end of the list.

        :param value: Element to add.
        """
        try:
            self.objects.append(value)
        except IndexError:
            raise IndexError("Incorrect index!")

    def insert(self, value: Any, index: int) -> None:
        """
        Inserts an element at the specified index.

        :param value: Element to insert.
        :param index: Index for inserting the element.
        """
        self.objects.insert(index, value)

    def cell_size(self, index: int, unit: str = "bytes") -> float:
        from sys import getsizeof
        """
        Returns the size of an element at the specified index in bytes or other units.

        :param index: Index of the element.
        :param unit: Unit of measurement (default is "bytes", add param: kb, mb, gb, tb).
        :return: Size of the element in the specified unit.
        """
        if index < 0 or index >= len(self.objects):
            raise IndexError("Incorrect index!")
        size_in_bytes = getsizeof(self.objects[index])

        if unit.lower() == "bytes":
            return size_in_bytes
        elif unit.lower() == "kb":
            return size_in_bytes / 1024
        elif unit.lower() == "mb":
            return size_in_bytes / (1024 ** 2)
        elif unit.lower() == "gb":
            return size_in_bytes / (1024 ** 3)
        elif unit.lower() == "tb":
            return size_in_bytes / (1024 ** 4)
        else:
            raise ValueError("Invalid unit. Supported units are 'bytes', 'kb', 'mb', 'gb', 'tb'.")

    def get(self, index: int) -> Any:
        """
        Returns an element at the specified index.

        :param index: Index of the element.
        :return: Element at the specified index.
        """
        return self.objects[index]

    def delete(self, index: int) -> None:
        """
        Deletes an element at the specified index.

        :param index: Index of the element to delete.
        """
        try:
            del self.objects[index]
        except IndexError:
            raise IndexError("Incorrect index!")


class Path:
    def __init__(self, path: str) -> None:
        """
        Initializes a Path object with the given path string.

        :param path: The file path as a string.
        :raises FileNotFoundError: If the path contains a space.
        """
        if " " in path:
            raise FileNotFoundError("Incorrect format File path cannot contain spaces!")
        self.path = path.replace("\\", "/")

    def __sizeof__(self) -> float:
        """
        Returns the size of the Path object in bytes.

        :return: The size of the Path object.
        """
        from sys import getsizeof
        return getsizeof(self.path)

    def __eq__(self, other: "Path", unit: str = "bytes") -> bool:
        """
        Compares the size of two Path objects.

        :param other: The other Path object to compare with.
        :param unit: The unit of measurement (default is 'bytes').
        :return: True if the sizes are equal, False otherwise.
        """
        return self.size(unit) == other.size(unit)

    def __ne__(self, other: "Path", unit: str = "bytes") -> bool:
        """
        Checks if the size of two Path objects is not equal.

        :param other: The other Path object to compare with.
        :param unit: The unit of measurement (default is 'bytes').
        :return: True if the sizes are not equal, False otherwise.
        """
        return self.size(unit) != other.size(unit)

    def __lt__(self, other: "Path", unit: str = "bytes") -> bool:
        """
        Checks if the size of this Path object is less than the size of another Path object.

        :param other: The other Path object to compare with.
        :param unit: The unit of measurement (default is 'bytes').
        :return: True if this size is less than the other size, False otherwise.
        """
        return self.size(unit) < other.size(unit)

    def __gt__(self, other: "Path", unit: str = "bytes") -> bool:
        """
        Checks if the size of this Path object is greater than the size of another Path object.

        :param other: The other Path object to compare with.
        :param unit: The unit of measurement (default is 'bytes').
        :return: True if this size is greater than the other size, False otherwise.
        """
        return self.size(unit) > other.size(unit)

    def __le__(self, other: "Path", unit: str = "bytes") -> bool:
        """
        Checks if the size of this Path object is less than or equal to the size of another Path object.

        :param other: The other Path object to compare with.
        :param unit: The unit of measurement (default is 'bytes').
        :return: True if this size is less than or equal to the other size, False otherwise.
        """
        return self.size(unit) <= other.size(unit)

    def __ge__(self, other: "Path", unit: str = "bytes") -> bool:
        """
        Checks if the size of this Path object is greater than or equal to the size of another Path object.

        :param other: The other Path object to compare with.
        :param unit: The unit of measurement (default is 'bytes').
        :return: True if this size is greater than or equal to the other size, False otherwise.
        """
        return self.size(unit) >= other.size(unit)

    def __iadd__(self, other: Any) -> "Path":
        """
        Appends the given content to the file at the specified path.

        :param other: The content to append to the file.
        :return: The Path object itself.
        """
        try:
            with open(self.path, "a") as file_:
                file_.write(other)
        except Exception as e:
            print(f"Error writing to file: {e}")
        return self

    def __contains__(self, item) -> bool:
        """
        Checks if the given item is in the path string.

        :param item: The item to check for in the path.
        :return: True if the item is in the path, False otherwise.
        """
        return item in self.path

    def __len__(self) -> float:
        """
        Returns the size of the file at the specified path in bytes.

        :return: The size of the file.
        """
        from os.path import getsize
        return getsize(self.path)

    def __iter__(self):
        """
        Iterates over the components of the path.

        :return: An iterator over the path components.
        """
        return iter(self.path.split("/"))

    def open(self) -> None:
        """
        Opens the file at the specified path using the default application.

        :raises Exception: If an error occurs during opening.
        """
        from os import startfile
        try:
            if self.path.startswith('"') and self.path.endswith('"'):
                self.path = self.path[1:-1]
            startfile(self.path)
        except Exception as e:
            print(f"Error opening file: {e}")

    def size(self, unit: str = "bytes") -> float:
        """
        Returns the size of the file at the specified path in the given unit.

        :param unit: The unit of measurement (default is 'bytes').
        :return: The size of the file in the specified unit.
        :raises ValueError: If the unit is not recognized.
        """
        from os.path import getsize
        if unit.lower() == "bytes":
            return getsize(self.path)
        elif unit.lower() == "kb":
            return getsize(self.path) / 1024
        elif unit.lower() == "mb":
            return getsize(self.path) / (1024 ** 2)
        elif unit.lower() == "gb":
            return getsize(self.path) / (1024 ** 3)
        elif unit.lower() == "tb":
            return getsize(self.path) / (1024 ** 4)
        else:
            raise ValueError("Invalid unit. Use 'bytes', 'kb', 'mb', 'gb', or 'tb'.")

    def delete(self) -> None:
        """
        Deletes the directory at the specified path.

        :raises Exception: If an error occurs during deletion.
        """
        from os import rmdir
        rmdir(self.path)

    def read(self, mode: str = "r", encoding: str = "utf-8") -> list:
        """
        Reads the content of the file at the specified path.

        :param encoding for file
        :param mode: The mode in which to open the file (default is 'r').
        :return: A list of lines from the file.
        :raises Exception: If an error occurs during reading.
        """
        try:
            with open(self.path, mode, encoding=encoding) as file_:
                return file_.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

    def in_file(self, item: str, mode: str = "r", encoding: str = "utf-8") -> bool:
        """
        Checks if the given item is in the content of the file at the specified path.

        :param item: The item to check for in the file content.
        :param mode: The mode in which to open the file (default is 'r').
        :param encoding: The encoding for the file (default is 'utf-8').
        :return: True if the item is in the file content, False otherwise.
        :raises Exception: If an error occurs during reading.
        """

        try:
            with open(self.path, mode, encoding=encoding) as file_:
                content = file_.read()
                return item in content
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return False
        except Exception as e:
            print(f"Error reading file: {e}")
            return False


# class ByteLink:
#     def __init__(self, *args: Any) -> None:

