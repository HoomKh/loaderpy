from typing import Literal, Union, Callable, Sequence, Any
from pathlib import Path

import fitz
import matplotlib.patches as patches
import matplotlib.pylab as plt
from PIL import Image

from langchain_core.documents import Document
from utils._pypdf import pypdf_loader
from utils._unstructured import unstructured_loader
from utils.print_plot import (
    print_unstructured_page,
    print_pypdf_page,
    plot_pdf_with_boxes,
)


def choose_method(
    path: Union[str, Path, list[str], list[Path]],
    method: Literal["pypdf", "unstructured"],
    strategy: Literal["hi_res", "fast"],
    mode: Literal["single", "elements", "paged"],
    partition_via_api: bool,
    post_processors: Union[list[Callable[[str], str]], Callable[[str], str], None],
    api_key: str,
) -> list[Document]:

    if method == "pypdf":
        return pypdf_loader(path=path)
    elif method == "unstructured":
        return unstructured_loader(
            path=path,
            strategy=strategy,
            mode=mode,
            partition_via_api=partition_via_api,
            post_processors=post_processors,
            api_key=api_key,
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


# Unstructured Render and Print Specific Page
def render_page(
    file_paths: Union[str, Path, list[Path], list[str]],
    doc_list: list[Document],
    page_number: int,
    print_text: bool = False,
    show_metadata: bool = None,
):
    all_pages = load_all_pages(file_paths=file_paths)
    pdf_page = all_pages[page_number - 1]
    page_docs = [
        doc for doc in doc_list if doc.metadata.get("page_number") == page_number
    ]
    segments = [doc.metadata for doc in page_docs]
    plot_pdf_with_boxes(pdf_page=pdf_page, segments=segments)
    if print_text:
        print_unstructured_page(
            docs=doc_list,
            pages=page_number,
            show_metadata=show_metadata,
        )


def load_all_pages(
    file_paths: Union[str, Path, list[str], list[Path]],
) -> list[fitz.Page]:
    if isinstance(file_paths, (str, Path)):
        file_paths = [file_paths]
    all_pages = []
    for path in file_paths:
        doc = fitz.open(str(path))
        pages = [doc.load_page(i) for i in range(len(doc))]
        all_pages.extend(pages)
    return all_pages
