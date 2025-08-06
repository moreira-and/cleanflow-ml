O que essa base precisa ter, em termos de **propriedades de domínio**, para ser suficiente e extensível pra ML/SLM sem acoplar infra:

[base_data_entity](/src/domain/entities/base_data_entity.py)

### 1. Identidade e versionamento

* `identity: str` — UUID ou hash derivado do conteúdo + schema. Permite lineage, cache, deduplicação.
* `version: str` — semântica (p.ex. `schema.v1+hash`, ou contador) para comparar snapshots.

### 2. Schema expandido

* `schema: DatasetSchema` com complementos possíveis:

  * `feature_types: dict[str, str]` (numérico, categórico, texto, datetime etc.) — ajuda regras de pré-processamento.
  * `targets: Optional[List[str]]` já tem, mas deixar claro se é supervisionado/regressão/classificação multiclasses.
  * `constraints` (ex: not null, ranges esperados) — invariantes esperadas.

### 3. Provenance / origem

* `provenance` (value object):

  * `source`: origem lógica (nome do stream, arquivo, API).
  * `extraction_time`: timestamp do colhimento.
  * `transforms`: lista imutável de transformações aplicadas (nome + params).

### 4. Qualidade / validação

* `validation_status` ou `quality_report`:

  * Se passou/erros de schema.
  * Missing rate por coluna.
  * Drift detection baseline vs atual (pode ser meta).
  * Distribuições resumidas (opcionales, lazy).

### 5. Particionamento e contexto de uso

* `partition_info`: marca se é treino/validação/teste, fold, slice lógico.
* `lineage_id` ou `parent_ids`: para reconstruir derivação de versões anteriores.

### 6. Meta/adicionais úteis para ML avançado (e SLMs)

* `embeddings`: representação vetorial derivada (pode ser `None` até ser gerado).
* `feedback`: sinais de correção ou label feedback (ex: “esta predição estava errada”).
* `confidence` / `weight`: peso do exemplo ou confiança da fonte.
* `timestamp` de observação (quando o dado foi gerado no mundo real), separado de extraction\_time.

### 7. Metadata arbitrária (você já tem) — manter imutável

Use para tagueamento, experimento, usuário, etc.

---

### Comportamentos (métodos de domínio) que fazem sentido junto:

* `validate_against_schema() -> ValidationStatus`
* `is_compatible_with(other: BaseDataEntity) -> bool`
* `merge(other: BaseDataEntity) -> BaseDataEntity` (com checagem de invariantes)
* `split(rules) -> tuple[BaseDataEntity, ...]` (treino/teste/folds)
* `with_updated_metadata(...)` mantendo imutabilidade

---

### Justificativa resumida

* **Imutabilidade + identidade/versionamento**: garante reprodutibilidade e rastreabilidade sem estado escondido.
* **Schema rico**: domínio entende tipo e restrições antes de usar.
* **Provenance + split/lineage**: suporta pipelines complexos e aprendizado contínuo.
* **Validation/quality**: evita que modelo rode com dados quebrados sem checar invariantes.
* **Embeddings/feedback**: prepara para SLMs e loops de correção adaptativa.