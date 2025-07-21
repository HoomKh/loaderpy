from typing import Literal, Union, Callable, Sequence, Any
from pathlib import Path
from collections.abc import Iterable
from langchain_core.documents import Document
from utils._pypdf import pypdf_loader
from utils._unstructured import unstructured_loader_api, unstructured_loader_local
from utils.print import print_unstructured_page, print_pypdf_page


def choose_method(
    path: Union[str, Path, list[str], list[Path]],
    method: Literal["pypdf", "unstructured"],
    strategy: Literal["hi_res", "fast"],
    mode: Literal["single", "elements", "paged"],
    partition_via_api: bool,
    coordinates: bool,
    post_processors: Union[list[Callable[[str], str]], Callable[[str], str], None],
    api_key: str,
) -> list[Document]:

    if method == "pypdf":
        return pypdf_loader(path=path)
    elif method == "unstructured":
        if partition_via_api == True or api_key != None:
            return unstructured_loader_api(
                path=path,
                strategy=strategy,
                mode=mode,
                partition_via_api=partition_via_api,
                coordinates=coordinates,
                post_processors=post_processors,
                api_key=api_key,
            )
        else:
            return unstructured_loader_local(
                path=path,
                strategy=strategy,
                mode=mode,
                post_processors=post_processors,
            )


def print_pages(
    docs: list[Document],
    loader_method: Literal["unstructured", "pypdf"],
    *,
    pages: Union[int, Sequence[int], None] = None,
    start_page: int | None = None,
    end_page: int | None = None,
    show_metadata: bool = False,
    ignore_metadata_keys: Sequence[str] | None = ("coordinates", "bbox"),
) -> None:

    if loader_method == "unstructured":
        print_unstructured_page(
            docs=docs,
            pages=pages,
            start_page=start_page,
            end_page=end_page,
            show_metadata=show_metadata,
            ignore_metadata_keys=ignore_metadata_keys,
        )
    elif loader_method == "pypdf":
        print_pypdf_page(
            docs=docs,
            pages=pages,
            start_page=start_page,
            end_page=end_page,
            show_metadata=show_metadata,
        )
