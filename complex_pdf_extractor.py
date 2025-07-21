from pathlib import Path
from typing import Literal, Union, Callable
from langchain_core.documents import Document
from utils import choose_method, print_pages


def pdf_loader(
    path: Union[str, Path, list[str], list[Path]] = None,
    method: Literal["pypdf", "unstructured"] = None,
    strategy: Literal["hi_res", "fast"] = "fast",
    mode: Literal["single", "elements", "paged"] = None,
    partition_via_api: bool = None,
    coordinates: bool = None,
    post_processors: Union[
        list[Callable[[str], str]], Callable[[str], str], None
    ] = None,
    api_key: str = None,
) -> list[Document]:

    return choose_method(
        path=path,
        method=method,
        strategy=strategy,
        mode=mode,
        partition_via_api=partition_via_api,
        coordinates=coordinates,
        post_processors=post_processors,
        api_key=api_key,
    )

# file_path = "/Users/hoom_kh/Downloads/layout-parser-paper.pdf"

if __name__ == "__main__":
    file_path = ["/Users/hoom_kh/Downloads/layout-parser-paper.pdf",
                 "/Users/hoom_kh/Downloads/2307.06435v10.pdf"
                 ]
    docs = pdf_loader(path=file_path, method="unstructured")
    print_pages(
            docs=docs, loader_method="unstructured", pages=[1,10,4], show_metadata=True
        )
