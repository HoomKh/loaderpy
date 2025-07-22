from langchain_unstructured import UnstructuredLoader
from langchain_core.documents import Document
from typing import Union, Literal, Callable
from pathlib import Path


def unstructured_loader(
    path: Union[str, Path, list[str], list[Path]],
    strategy: Literal["hi_res", "fast"] ,
    mode: Literal["single", "elements", "paged"] ,
    partition_via_api: bool = None,
    post_processors: Union[
        list[Callable[[str], str]], Callable[[str], str], None
    ] = None,
    api_key: str = None,   
) -> list[Document]:

    loader = UnstructuredLoader(
        file_path=path,
        strategy=strategy,
        mode=mode,
        partition_via_api=partition_via_api,
        api_key=api_key,
        post_processors=post_processors,
    )

    return list(loader.lazy_load())