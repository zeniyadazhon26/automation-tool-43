from typing import TypeVar, Iterable, Generator, Union, Callable

T = TypeVar('T')
U = TypeVar('U')
R = TypeVar('R')

def alternate_weave(
    left: Iterable[T],
    right: Iterable[U],
    transform: Callable[[Union[T, U]], R]
) -> Generator[R, None, None]:
    """
    Interleave two iterables in a checkerboard fashion, applying a transformer.

    This utility alternates elements from 'left' and 'right' inputs. If one
    iterable is exhausted, it drains the remaining elements from the active one.
    Highly versatile for combining dynamic parameter grids or log interleaving.

    Args:
        left: The primary sequence of elements.
        right: The secondary sequence of elements.
        transform: A mapping function to unify the different types T and U into R.

    Yields:
        A single generator producing elements of type R.
    """
    left_iter = iter(left)
    right_iter = iter(right)
    
    left_active, right_active = True, True
    
    while left_active or right_active:
        if left_active:
            try:
                yield transform(next(left_iter))
            except StopIteration:
                left_active = False
        if right_active:
            try:
                yield transform(next(right_iter))
            except StopIteration:
                right_active = False


def payload_flatten(
    nested_data: Iterable[Union[T, Iterable[T]]]
) -> Generator[T, None, None]:
    """
    Flattens lists and sub-iterables of mixed depth by exactly one level.

    Strings and bytes are deliberately treated as scalar units instead of iterables
    to prevent recursive character explosion in automation payload parameters.

    Args:
        nested_data: Sequence potentially containing nested sequences.

    Yields:
        Elements unpacked by one level of nesting.
    """
    for item in nested_data:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            for sub_item in item:
                yield sub_item
        else:
            yield item  # type: ignore