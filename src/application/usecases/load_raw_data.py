from src.infrastructure.repositories.i_query.raw import (
    YfinanceLoader,
    BcbLoader,
    DataReaderLoader,
)

# application/pipeline/stages.py
from typing import Dict, Any, Mapping


def fetch_from_yfinance(ctx: Dict[str, Any], loader: YfinanceLoader) -> Dict[str, Any]:
    ids = ctx.get("ids")  # ex.: ["PETR4", "VALE3"]
    ctx.setdefault("raw", {})
    ctx["raw"]["yfinance"] = loader.get_by_id(ids)
    return ctx


def fetch_from_bcb(ids: list[str]):
    loader = BcbLoader()
    return loader.load(ids)


def fetch_from_datareader(ids: list[str]):
    loader = DataReaderLoader()
    return loader.load(ids)


def normalize(results: list[Mapping[str, Any]]):
    # consolida os resultados de diferentes fontes
    consolidated = {}
    for dataset in results:
        consolidated.update(dataset)
    return consolidated


# --- Exemplo de uso ---
ids = ["PETR4", "VALE3", "IPCA"]

pipeline = (
    Pipeline()
    .add_stage(lambda _: fetch_from_yfinance(ids))
    .add_stage(lambda _: fetch_from_bcb(ids))
    .add_stage(lambda _: fetch_from_datareader(ids))
    .add_stage(
        lambda results: normalize(results if isinstance(results, list) else [results])
    )
)

final_result = pipeline.run(ids)
print(final_result)
